from __future__ import annotations

import dataclasses
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from numbers import Number
from textwrap import indent
from typing import Dict, List

from soda.cloud.soda_cloud import SodaCloud
from soda.common import logs as soda_core_logs
from soda.scan import Scan
from soda.scan import logger as scan_logger

from soda.contracts import soda_cloud as contract_soda_cloud
from soda.contracts.connection import SodaException
from soda.contracts.impl.logs import Location, Log, LogLevel, Logs
from soda.contracts.impl.yaml import YamlObject, YamlWriter

logger = logging.getLogger(__name__)


class Contract:

    @classmethod
    def from_yaml_str(
        cls, contract_yaml_str: str, variables: dict[str, str] | None = None, schedule: str | None = None
    ) -> Contract:
        """
        Build a contract from a YAML string
        """
        from soda.contracts.impl.contract_parser import ContractParser

        contract_parser: ContractParser = ContractParser()
        return contract_parser.parse_contract(
            contract_yaml_str=contract_yaml_str, variables=variables, schedule=schedule
        )

    @classmethod
    def from_yaml_file(
        cls, file_path: str, variables: dict[str, str] | None = None, schedule: str | None = None
    ) -> Contract:
        """
        Build a contract from a YAML file.
        Raises OSError in case the file_path cannot be opened like e.g.
        FileNotFoundError or PermissionError
        """
        with open(file_path) as f:
            contract_yaml_str = f.read()
            return cls.from_yaml_str(contract_yaml_str=contract_yaml_str, variables=variables, schedule=schedule)

    def __init__(
        self,
        schedule: str | None,
        dataset: str,
        sql_filter: str | None,
        schema: str | None,
        checks: List[Check],
        contract_yaml_str: str,
        variables: dict[str, str] | None,
        logs: Logs,
    ):
        """
        Consider using Contract.from_yaml_str(contract_yaml_str) instead as that is more stable API.
        """
        self.schedule: str | None = schedule
        self.dataset: str = dataset
        self.sql_filter: str | None = sql_filter
        self.schema: str | None = schema
        self.checks: List[Check] = checks
        self.contract_yaml_str: str = contract_yaml_str
        self.variables: dict[str, str] | None = variables
        # The initial logs will contain the logs of contract parser.  If there are error logs, these error logs
        # will cause a SodaException to be raised at the end of the Contract.verify method
        # See also adr/03_exceptions_vs_error_logs.md
        self.logs: Logs = logs
        self.sodacl_yaml_str: str | None = None

    def verify(self, connection: Connection, soda_cloud: contract_soda_cloud.SodaCloud | None = None) -> ContractResult:
        """
        Verifies if the data in the dataset matches the contract.
        """

        scan = Scan()

        scan_logs = soda_core_logs.Logs(logger=scan_logger)
        scan_logs.verbose = True

        sodacl_yaml_str: str | None = None
        try:
            sodacl_yaml_str = self.generate_sodacl_yaml_str(self.logs)
            logger.debug(sodacl_yaml_str)

            if sodacl_yaml_str and hasattr(connection, "data_source"):
                scan._logs = scan_logs

                # This assumes the connection is a DataSourceConnection
                data_source = connection.data_source
                # Execute the contract SodaCL in a scan
                scan.set_data_source_name(data_source.data_source_name)
                scan_definition_name = (
                    f"dataset://{connection.name}/{self.schema}/{self.dataset}"
                    if self.schema
                    else f"dataset://{connection.name}/{self.dataset}"
                )
                scan._data_source_manager.data_sources[data_source.data_source_name] = data_source

                if soda_cloud:
                    scan.set_scan_definition_name(scan_definition_name)
                    scan._configuration.soda_cloud = SodaCloud(
                        host=soda_cloud.host,
                        api_key_id=soda_cloud.api_key_id,
                        api_key_secret=soda_cloud.api_key_secret,
                        token=soda_cloud.token,
                        port=soda_cloud.port,
                        logs=scan_logs,
                        scheme=soda_cloud.scheme,
                    )

                if self.variables:
                    scan.add_variables(self.variables)

                # noinspection PyProtectedMember
                scan.add_sodacl_yaml_str(sodacl_yaml_str)
                scan.execute()

        except Exception as e:
            self.logs.error(f"Data contract verification error: {e}", exception=e)

        if soda_cloud:
            # If SodaCloud is configured, the logs are copied into the contract result and
            # at the end of this method, a SodaException is raised if there are error logs.
            self.logs.logs.extend(soda_cloud.logs.logs)
        if connection:
            # The connection logs are copied into the contract result and at the end of this
            # method, a SodaException is raised if there are error logs.
            self.logs.logs.extend(connection.logs.logs)
        # The scan warning and error logs are copied into self.logs and at the end of this
        # method, a SodaException is raised if there are error logs.
        self.append_scan_warning_and_error_logs(scan_logs)

        contract_result: ContractResult = ContractResult(
            contract=self, sodacl_yaml_str=sodacl_yaml_str, logs=self.logs, scan=scan
        )
        if contract_result.failed():
            raise SodaException(contract_result=contract_result)

        return contract_result

    def append_scan_warning_and_error_logs(self, scan_logs: soda_core_logs.Logs) -> None:
        level_map = {
            soda_core_logs.LogLevel.ERROR: LogLevel.ERROR,
            soda_core_logs.LogLevel.WARNING: LogLevel.WARNING,
            soda_core_logs.LogLevel.INFO: LogLevel.INFO,
            soda_core_logs.LogLevel.DEBUG: LogLevel.DEBUG,
        }
        for scan_log in scan_logs.logs:
            if scan_log.level in [soda_core_logs.LogLevel.ERROR, soda_core_logs.LogLevel.WARNING]:
                contracts_location: Location = (
                    Location(line=scan_log.location.line, column=scan_log.location.col)
                    if scan_log.location is not None
                    else None
                )
                contracts_level: LogLevel = level_map[scan_log.level]
                self.logs._log(
                    Log(
                        level=contracts_level,
                        message=f"SodaCL: {scan_log.message}",
                        location=contracts_location,
                        exception=scan_log.exception,
                    )
                )

    def generate_sodacl_yaml_str(self, logs: Logs) -> str:
        # Serialize the SodaCL YAML object to a YAML string
        sodacl_checks: list = []
        sodacl_yaml_object: dict = (
            {
                f"filter {self.dataset} [filter]": {"where": self.sql_filter},
                f"checks for {self.dataset} [filter]": sodacl_checks,
            }
            if self.sql_filter
            else {f"checks for {self.dataset}": sodacl_checks}
        )

        for check in self.checks:
            sodacl_check = check.to_sodacl_check()
            if sodacl_check is not None:
                sodacl_checks.append(sodacl_check)
        yaml_writer: YamlWriter = YamlWriter(logs)
        return yaml_writer.write_to_yaml_str(sodacl_yaml_object)


@dataclass
class ContractResult:
    """
    This is the immutable data structure containing all the results from a single contract verification.
    This includes any potential execution errors as well as the results of all the checks performed.
    """

    contract: Contract
    sodacl_yaml_str: str | None
    # self.logs combines all the logs of the contract verification with the logs of the Connection parsing,
    # connection usage, SodaCloud parsing and usage (if used) and contract parsing.
    # At the end of the verify method a SodaException is raised if there are any error logs or check failures.
    # See also adr/03_exceptions_vs_error_logs.md
    logs: Logs
    check_results: List[CheckResult]

    def __init__(self, contract: Contract, sodacl_yaml_str: str | None, logs: Logs, scan: Scan):
        self.contract = contract
        self.sodacl_yaml_str = sodacl_yaml_str
        # See also adr/03_exceptions_vs_error_logs.md
        self.logs: Logs = Logs(logs)
        self.check_results: List[CheckResult] = []

        contract_checks_by_id: dict[str, Check] = {check.identity: check for check in contract.checks}

        schema_check: SchemaCheck | None = next((c for c in contract.checks if isinstance(c, SchemaCheck)), None)

        scan_metrics_by_id: dict[str, dict] = {
            scan_metric["identity"]: scan_metric for scan_metric in scan.scan_results.get("metrics", [])
        }

        scan_checks = scan.scan_results.get("checks")
        if isinstance(scan_checks, list):
            for scan_check in scan_checks:
                contract_check: Check | None = None
                if scan_check.get("name") == "Schema Check" and scan_check.get("type") == "generic":
                    contract_check = schema_check
                else:
                    contract_check_id = scan_check.get("contract_check_id")
                    if isinstance(contract_check_id, str):
                        contract_check = contract_checks_by_id[contract_check_id]

                assert contract_check is not None, "Contract scan check matching failed :("

                scan_check_metric_ids = scan_check.get("metrics")
                scan_check_metrics = [
                    scan_metrics_by_id.get(check_metric_id) for check_metric_id in scan_check_metric_ids
                ]
                scan_check_metrics_by_name = {
                    scan_check_metric.get("metricName"): scan_check_metric for scan_check_metric in scan_check_metrics
                }
                check_result = contract_check.create_check_result(
                    scan_check=scan_check, scan_check_metrics_by_name=scan_check_metrics_by_name, scan=scan
                )
                self.check_results.append(check_result)

    def failed(self) -> bool:
        return self.has_execution_errors() or self.has_check_failures()

    def passed(self) -> bool:
        return not self.failed()

    def has_execution_errors(self):
        return self.logs.has_errors()

    def has_check_failures(self):
        return any(check.outcome == CheckOutcome.FAIL for check in self.check_results)

    def __str__(self) -> str:
        error_texts_list: List[str] = [str(error) for error in self.logs.get_errors()]

        check_failure_message_list: list[str] = []
        for check_result in self.check_results:
            if check_result.outcome == CheckOutcome.FAIL:
                result_str_lines = check_result.get_contract_result_str_lines()
                check_failure_message_list.extend(result_str_lines)

        if not error_texts_list and not check_failure_message_list:
            return "All is good. No checks failed. No contract execution errors."

        errors_summary_text = f"{len(error_texts_list)} execution error"
        if len(error_texts_list) != 1:
            errors_summary_text = f"{errors_summary_text}s"

        checks_summary_text = f"{len(check_failure_message_list)} check failure"
        if len(check_failure_message_list) != 1:
            checks_summary_text = f"{checks_summary_text}s"

        parts = [f"{checks_summary_text} and {errors_summary_text}"]
        if error_texts_list:
            error_lines_text: str = indent("\n".join(error_texts_list), "  ")
            parts.append(f"Errors: \n{error_lines_text}")

        if check_failure_message_list:
            parts.append("\n".join(check_failure_message_list))

        return "\n".join(parts)


@dataclass
class Check(ABC):

    schedule: str | None
    dataset: str
    column: str | None
    type: str

    # User defined name as in the contract.  None if not specified in the contract.
    name: str | None

    # Check identifier used to correlate the sodacl check results with this contract check object when parsing
    # scan results.  Also used as correlation id in Soda Cloud to match subsequent results for the same check.
    # Composite key created from schedule, dataset, column, type and identity_suffix.
    identity: str | None

    location: Location | None

    @abstractmethod
    def to_sodacl_check(self) -> str | dict | None:
        pass

    @abstractmethod
    def create_check_result(
        self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan
    ) -> CheckResult:
        pass

    @classmethod
    def create_check_identity(
        cls,
        schedule: str | None,
        dataset: str,
        column: str | None,
        check_type: str,
        check_identity_suffix: str | None,
        check_location: Location | None,
        checks: dict[str, Check],
        logs: Logs,
    ) -> str:
        opt_schedule_part = f"//{schedule}" if schedule else ""
        opt_column_part = f"/{column}" if column else ""
        opt_check_identity_suffix_part = f"/{check_identity_suffix}" if check_identity_suffix else ""
        check_identity = f"{opt_schedule_part}/{dataset}{opt_column_part}/{check_type}{opt_check_identity_suffix_part}"

        other_check: Check = checks.get(check_identity)
        if other_check:
            logs.error(f"Duplicate check identity '{check_identity}': {other_check.location} and {check_location}")
            suffix_index: int = 2
            while check_identity in checks:
                opt_check_identity_suffix_part = (
                    f"/{check_identity_suffix}_{suffix_index}" if check_identity_suffix else f"/{suffix_index}"
                )
                check_identity = (
                    f"{opt_schedule_part}/{dataset}{opt_column_part}/{check_type}{opt_check_identity_suffix_part}"
                )
                suffix_index = suffix_index + 1
        return check_identity


@dataclass
class CheckResult:
    check: Check
    outcome: CheckOutcome

    def __str__(self) -> str:
        return "\n".join(self.get_contract_result_str_lines())

    @abstractmethod
    def get_contract_result_str_lines(self) -> list[str]:
        """
        Provides the summary for the contract result logs, as well as the __str__ impl of this check result.
        Method implementations can use self._get_outcome_line(self)
        """

    def get_outcome_and_name_line(self) -> str:
        name_str: str = f" [{self.check.name}]" if self.check.name else ""
        return f"Check {self.get_outcome_str()}{name_str}"

    def get_outcome_str(self) -> str:
        if self.outcome == CheckOutcome.FAIL:
            return "FAILED"
        if self.outcome == CheckOutcome.PASS:
            return "passed"
        return "unverified"


@dataclass
class SchemaCheck(Check):

    columns: dict[str, str | None]
    optional_columns: list[str]

    def to_sodacl_check(self) -> str | dict | None:
        schema_fail_dict = {"when mismatching columns": self.columns}
        if self.optional_columns:
            schema_fail_dict["with optional columns"] = self.optional_columns
        return {"schema": {"fail": schema_fail_dict}}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        scan_measured_schema: list[dict] = scan_check_metrics_by_name.get("schema").get("value")
        measured_schema = {c.get("columnName"): c.get("sourceDataType") for c in scan_measured_schema}

        diagnostics = scan_check.get("diagnostics", {})

        columns_not_allowed_and_present: list[str] = diagnostics.get("present_column_names", [])
        columns_required_and_not_present: list[str] = diagnostics.get("missing_column_names", [])

        columns_having_wrong_type: list[DataTypeMismatch] = []
        scan_column_type_mismatches = diagnostics.get("column_type_mismatches", {})
        if scan_column_type_mismatches:
            for column_name, column_type_mismatch in scan_column_type_mismatches.items():
                expected_type = column_type_mismatch.get("expected_type")
                actual_type = column_type_mismatch.get("actual_type")
                columns_having_wrong_type.append(
                    DataTypeMismatch(column=column_name, expected_data_type=expected_type, actual_data_type=actual_type)
                )

        return SchemaCheckResult(
            check=self,
            outcome=CheckOutcome.from_scan_check(scan_check),
            measured_schema=measured_schema,
            columns_not_allowed_and_present=columns_not_allowed_and_present,
            columns_required_and_not_present=columns_required_and_not_present,
            columns_having_wrong_type=columns_having_wrong_type,
        )


@dataclass
class SchemaCheckResult(CheckResult):

    measured_schema: Dict[str, str]
    columns_not_allowed_and_present: list[str] | None
    columns_required_and_not_present: list[str] | None
    columns_having_wrong_type: list[DataTypeMismatch] | None

    def get_contract_result_str_lines(self) -> list[str]:
        schema_check: SchemaCheck = self.check
        expected_schema: str = ",".join(
            [
                f"{c.get('name')}{c.get('optional')}{c.get('type')}"
                for c in [
                    {
                        "name": column_name,
                        "optional": "(optional)" if column_name in schema_check.optional_columns else "",
                        "type": f"={data_type}" if data_type else "",
                    }
                    for column_name, data_type in schema_check.columns.items()
                ]
            ]
        )

        lines: list[str] = [
            f"Schema check {self.get_outcome_str()}",
            f"  Expected schema: {expected_schema}",
            f"  Actual schema: {self.measured_schema}",
        ]
        lines.extend(
            [f"  Column '{column}' was present and not allowed" for column in self.columns_not_allowed_and_present]
        )
        lines.extend([f"  Column '{column}' was missing" for column in self.columns_required_and_not_present])
        lines.extend(
            [
                (
                    f"  Column '{data_type_mismatch.column}': Expected type '{data_type_mismatch.expected_data_type}', "
                    f"but was '{data_type_mismatch.actual_data_type}'"
                )
                for data_type_mismatch in self.columns_having_wrong_type
            ]
        )
        return lines


@dataclass
class NumericMetricCheck(Check):

    metric: str
    check_yaml_object: YamlObject
    missing_configurations: MissingConfigurations | None
    valid_configurations: ValidConfigurations | None
    threshold: NumericThreshold | None

    def to_sodacl_check(self) -> str | dict | None:
        sodacl_check_line = self.get_sodacl_check_line()

        sodacl_check_configs = {"contract check id": self.identity}

        if self.name:
            sodacl_check_configs["name"] = self.name

        if self.valid_configurations:
            sodacl_check_configs.update(self.valid_configurations.to_sodacl_check_configs_dict())
        if self.missing_configurations:
            sodacl_check_configs.update(self.missing_configurations.to_sodacl_check_configs_dict())

        return {sodacl_check_line: sodacl_check_configs}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        scan_metric_dict: dict
        if "(" in self.metric:
            scan_metric_name = self.metric[: self.metric.index("(")]
            scan_metric_dict = scan_check_metrics_by_name.get(scan_metric_name, None)
        else:
            scan_metric_dict = scan_check_metrics_by_name.get(self.metric, None)
        metric_value: Number = scan_metric_dict.get("value") if scan_metric_dict else None
        return NumericMetricCheckResult(
            check=self, outcome=CheckOutcome.from_scan_check(scan_check), metric_value=metric_value
        )

    def get_sodacl_check_line(self) -> str:
        sodacl_metric = self.get_sodacl_metric()
        sodacl_threshold: str = self.threshold.get_sodacl_threshold() if self.threshold else ""
        return f"{sodacl_metric} {sodacl_threshold}"

    def get_sodacl_metric(self) -> str:
        return f"{self.metric}({self.column})" if self.column else self.metric

    def get_sodacl_threshold(self) -> str:
        return self.threshold.get_sodacl_threshold() if self.threshold else "?"

    def get_metric_str(self) -> str:
        return self.get_sodacl_metric()

    def get_expected_str(self) -> str:
        return f"{self.get_metric_str()} {self.get_sodacl_threshold()}"


@dataclass
class NumericMetricCheckResult(CheckResult):
    metric_value: Number

    def get_contract_result_str_lines(self) -> list[str]:
        return [
            self.get_outcome_and_name_line(),
            f"  Expected {self.check.get_expected_str()}",
            f"  Actual {self.check.get_metric_str() } was {self.metric_value}",
        ]


@dataclass
class DuplicateCheck(NumericMetricCheck):
    columns: list[str]

    def get_sodacl_metric(self) -> str:
        column_str = self.column if self.column else ", ".join(self.columns)
        return f"{self.metric}({column_str})"


@dataclass
class InvalidReferenceCheck(NumericMetricCheck):

    valid_values_reference_data: ValidValuesReferenceData

    def to_sodacl_check(self) -> str | dict | None:
        sodacl_check_configs = {"contract check id": self.identity}

        if self.name:
            sodacl_check_configs["name"] = self.name

        if self.valid_configurations:
            sodacl_check_configs.update(self.valid_configurations.to_sodacl_check_configs_dict())
        if self.missing_configurations:
            sodacl_check_configs.update(self.missing_configurations.to_sodacl_check_configs_dict())

        sodacl_check_line: str = (
            f"values in ({self.column}) must exist in {self.valid_values_reference_data.dataset} ({self.valid_values_reference_data.column})"
        )

        return {sodacl_check_line: sodacl_check_configs}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        scan_metric_dict = scan_check_metrics_by_name.get("reference", {})
        value: Number = scan_metric_dict.get("value")
        return NumericMetricCheckResult(
            check=self, outcome=CheckOutcome.from_scan_check(scan_check), metric_value=value
        )


@dataclass
class FreshnessCheck(Check):

    column: str | None
    check_yaml_object: YamlObject
    threshold: NumericThreshold | None

    def get_definition_line(self) -> str:
        return f"freshness({self.column}) {self.threshold.get_sodacl_threshold()}{self.get_sodacl_time_unit()}"

    def get_sodacl_time_unit(self) -> str:
        sodacl_time_unit_by_check_type = {
            "freshness_in_days": "d",
            "freshness_in_hours": "h",
            "freshness_in_minutes": "m",
        }
        return sodacl_time_unit_by_check_type.get(self.type)

    def to_sodacl_check(self) -> str | dict | None:
        sodacl_check_configs = {
            "contract check id": self.identity,
        }
        if self.name:
            sodacl_check_configs["name"] = self.name

        sodacl_check_line: str = self.get_definition_line()
        return {sodacl_check_line: sodacl_check_configs}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        diagnostics: dict = scan_check["diagnostics"]
        freshness = diagnostics["freshness"]
        freshness_column_max_value = diagnostics["maxColumnTimestamp"]
        freshness_column_max_value_utc = diagnostics["maxColumnTimestampUtc"]
        now = diagnostics["nowTimestamp"]
        now_utc = diagnostics["nowTimestampUtc"]

        return FreshnessCheckResult(
            check=self,
            outcome=CheckOutcome.from_scan_check(scan_check),
            freshness=freshness,
            freshness_column_max_value=freshness_column_max_value,
            freshness_column_max_value_utc=freshness_column_max_value_utc,
            now=now,
            now_utc=now_utc,
        )


@dataclass
class FreshnessCheckResult(CheckResult):
    freshness: str
    freshness_column_max_value: str
    freshness_column_max_value_utc: str
    now: str
    now_utc: str

    def get_contract_result_str_lines(self) -> list[str]:
        assert isinstance(self.check, FreshnessCheck)
        return [
            self.get_outcome_and_name_line(),
            f"  Expected {self.check.get_definition_line()}",
            f"  Actual freshness({self.check.column}) was {self.freshness}",
            f"  Max value in column was ...... {self.freshness_column_max_value}",
            f"  Max value in column in UTC was {self.freshness_column_max_value_utc}",
            f"  Now was ...................... {self.now}",
            f"  Now in UTC was ............... {self.now_utc}",
        ]


@dataclass
class UserDefinedMetricSqlExpressionCheck(NumericMetricCheck):

    metric_sql_expression: str

    def to_sodacl_check(self) -> str | dict | None:

        sodacl_check_configs = {
            "contract check id": self.identity,
            f"{self.metric} expression": self.metric_sql_expression,
        }
        if self.name:
            sodacl_check_configs["name"] = self.name

        sodacl_checkline_threshold = self.threshold.get_sodacl_threshold()
        sodacl_check_line = f"{self.get_sodacl_metric()} {sodacl_checkline_threshold}"

        return {sodacl_check_line: sodacl_check_configs}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        scan_metric_dict: dict = scan_check_metrics_by_name.get(self.metric, None)
        metric_value: Number = scan_metric_dict.get("value") if scan_metric_dict else None
        return NumericMetricCheckResult(
            check=self, outcome=CheckOutcome.from_scan_check(scan_check), metric_value=metric_value
        )


@dataclass
class UserDefinedMetricSqlQueryCheck(NumericMetricCheck):

    metric_sql_query: str

    def to_sodacl_check(self) -> str | dict | None:
        sodacl_check_configs = {
            "contract check id": self.identity,
            f"{self.metric} query": self.metric_sql_query,
        }
        if self.name:
            sodacl_check_configs["name"] = self.name

        sodacl_check_line: str = self.get_sodacl_check_line()

        return {sodacl_check_line: sodacl_check_configs}

    def create_check_result(self, scan_check: dict[str, dict], scan_check_metrics_by_name: dict[str, dict], scan: Scan):
        scan_metric_dict: dict = scan_check_metrics_by_name.get(self.get_sodacl_check_line(), None)
        metric_value: Number = scan_metric_dict.get("value") if scan_metric_dict else None

        return NumericMetricCheckResult(
            check=self, outcome=CheckOutcome.from_scan_check(scan_check), metric_value=metric_value
        )


class CheckOutcome(Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"

    @classmethod
    def from_scan_check(cls, scan_check: Dict[str, object]) -> CheckOutcome:
        scan_check_outcome = scan_check.get("outcome")
        if scan_check_outcome == "pass":
            return CheckOutcome.PASS
        elif scan_check_outcome == "fail":
            return CheckOutcome.FAIL
        return CheckOutcome.UNKNOWN


@dataclass
class DataTypeMismatch:
    column: str
    expected_data_type: str
    actual_data_type: str


def dataclass_object_to_sodacl_dict(dataclass_object: object) -> dict:
    def translate_to_sodacl_key(key: str) -> str:
        if "sql_" in key:
            key = key.replace("sql_", "")
        return key.replace("_", " ")

    dict_factory = lambda x: {translate_to_sodacl_key(k): v for (k, v) in x if v is not None}
    return dataclasses.asdict(dataclass_object, dict_factory=dict_factory)


@dataclass
class MissingConfigurations:
    missing_values: list[str] | list[Number] | None
    missing_sql_regex: str | None

    def to_sodacl_check_configs_dict(self) -> dict:
        return dataclass_object_to_sodacl_dict(self)


@dataclass
class ValidConfigurations:
    invalid_values: list[str] | list[Number] | None
    invalid_format: str | None
    invalid_sql_regex: str | None
    valid_values: list[str] | list[Number] | None
    valid_format: str | None
    valid_sql_regex: str | None
    valid_min: Number | None
    valid_max: Number | None
    valid_length: int | None
    valid_min_length: int | None
    valid_max_length: int | None
    valid_values_reference_data: ValidValuesReferenceData | None

    def to_sodacl_check_configs_dict(self) -> dict:
        sodacl_check_configs_dict = dataclass_object_to_sodacl_dict(self)
        sodacl_check_configs_dict.pop("valid values reference data", None)
        return sodacl_check_configs_dict

    def has_non_reference_data_configs(self) -> bool:
        return (
            self.invalid_values is not None
            or self.invalid_format is not None
            or self.invalid_sql_regex is not None
            or self.valid_values is not None
            or self.valid_format is not None
            or self.valid_sql_regex is not None
            or self.valid_min is not None
            or self.valid_max is not None
            or self.valid_length is not None
            or self.valid_min_length is not None
            or self.valid_max_length is not None
        )


@dataclass
class ValidValuesReferenceData:
    dataset: str
    column: str


@dataclass
class NumericThreshold:
    """
    The threshold is exceeded when any of the member field conditions is True.
    To be interpreted as a check fails when the metric value is ...greater_than or ...less_than etc...
    """

    greater_than: Number | None = None
    greater_than_or_equal: Number | None = None
    less_than: Number | None = None
    less_than_or_equal: Number | None = None
    equal: Number | None = None
    not_equal: Number | None = None
    between: Range | None = None
    not_between: Range | None = None

    def get_sodacl_threshold(self) -> str:
        greater_bound: Number | None = (
            self.greater_than if self.greater_than is not None else self.greater_than_or_equal
        )
        less_bound: Number | None = self.less_than if self.less_than is not None else self.less_than_or_equal
        if greater_bound is not None and less_bound is not None:
            if greater_bound > less_bound:
                return self.sodacl_threshold(
                    is_not_between=True,
                    lower_bound=less_bound,
                    lower_bound_included=self.less_than is not None,
                    upper_bound=greater_bound,
                    upper_bound_included=self.greater_than is not None,
                )
            else:
                return self.sodacl_threshold(
                    is_not_between=False,
                    lower_bound=greater_bound,
                    lower_bound_included=self.greater_than_or_equal is not None,
                    upper_bound=less_bound,
                    upper_bound_included=self.less_than_or_equal is not None,
                )
        elif isinstance(self.between, Range):
            return self.sodacl_threshold(
                is_not_between=False,
                lower_bound=self.between.lower_bound,
                lower_bound_included=True,
                upper_bound=self.between.upper_bound,
                upper_bound_included=True,
            )
        elif isinstance(self.not_between, Range):
            return self.sodacl_threshold(
                is_not_between=True,
                lower_bound=self.not_between.lower_bound,
                lower_bound_included=True,
                upper_bound=self.not_between.upper_bound,
                upper_bound_included=True,
            )
        elif self.greater_than is not None:
            return f"> {self.greater_than}"
        elif self.greater_than_or_equal is not None:
            return f">= {self.greater_than_or_equal}"
        elif self.less_than is not None:
            return f"< {self.less_than}"
        elif self.less_than_or_equal is not None:
            return f"<= {self.less_than_or_equal}"
        elif self.equal is not None:
            return f"= {self.equal}"
        elif self.not_equal is not None:
            return f"!= {self.not_equal}"

    @classmethod
    def sodacl_threshold(
        cls,
        is_not_between: bool,
        lower_bound: Number,
        lower_bound_included: bool,
        upper_bound: Number,
        upper_bound_included: bool,
    ) -> str:
        optional_not = "not " if is_not_between else ""
        lower_bound_bracket = "" if lower_bound_included else "("
        upper_bound_bracket = "" if upper_bound_included else ")"
        return f"{optional_not}between {lower_bound_bracket}{lower_bound} and {upper_bound}{upper_bound_bracket}"

    def is_empty(self) -> bool:
        return (
            self.greater_than is None
            and self.greater_than_or_equal is None
            and self.less_than is None
            and self.less_than_or_equal is None
            and self.equal is None
            and self.not_equal is None
            and self.between is None
            and self.not_between is None
        )


@dataclass
class Range:
    """
    Boundary values are inclusive
    """

    lower_bound: Number | None
    upper_bound: Number | None
