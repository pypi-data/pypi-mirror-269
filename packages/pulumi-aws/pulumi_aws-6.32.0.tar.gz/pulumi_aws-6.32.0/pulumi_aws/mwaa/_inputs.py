# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'EnvironmentLastUpdatedArgs',
    'EnvironmentLastUpdatedErrorArgs',
    'EnvironmentLoggingConfigurationArgs',
    'EnvironmentLoggingConfigurationDagProcessingLogsArgs',
    'EnvironmentLoggingConfigurationSchedulerLogsArgs',
    'EnvironmentLoggingConfigurationTaskLogsArgs',
    'EnvironmentLoggingConfigurationWebserverLogsArgs',
    'EnvironmentLoggingConfigurationWorkerLogsArgs',
    'EnvironmentNetworkConfigurationArgs',
]

@pulumi.input_type
class EnvironmentLastUpdatedArgs:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 errors: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentLastUpdatedErrorArgs']]]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] created_at: The Created At date of the MWAA Environment
        :param pulumi.Input[str] status: The status of the Amazon MWAA Environment
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if errors is not None:
            pulumi.set(__self__, "errors", errors)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The Created At date of the MWAA Environment
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def errors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentLastUpdatedErrorArgs']]]]:
        return pulumi.get(self, "errors")

    @errors.setter
    def errors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentLastUpdatedErrorArgs']]]]):
        pulumi.set(self, "errors", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Amazon MWAA Environment
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class EnvironmentLastUpdatedErrorArgs:
    def __init__(__self__, *,
                 error_code: Optional[pulumi.Input[str]] = None,
                 error_message: Optional[pulumi.Input[str]] = None):
        if error_code is not None:
            pulumi.set(__self__, "error_code", error_code)
        if error_message is not None:
            pulumi.set(__self__, "error_message", error_message)

    @property
    @pulumi.getter(name="errorCode")
    def error_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "error_code")

    @error_code.setter
    def error_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "error_code", value)

    @property
    @pulumi.getter(name="errorMessage")
    def error_message(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "error_message")

    @error_message.setter
    def error_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "error_message", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationArgs:
    def __init__(__self__, *,
                 dag_processing_logs: Optional[pulumi.Input['EnvironmentLoggingConfigurationDagProcessingLogsArgs']] = None,
                 scheduler_logs: Optional[pulumi.Input['EnvironmentLoggingConfigurationSchedulerLogsArgs']] = None,
                 task_logs: Optional[pulumi.Input['EnvironmentLoggingConfigurationTaskLogsArgs']] = None,
                 webserver_logs: Optional[pulumi.Input['EnvironmentLoggingConfigurationWebserverLogsArgs']] = None,
                 worker_logs: Optional[pulumi.Input['EnvironmentLoggingConfigurationWorkerLogsArgs']] = None):
        """
        :param pulumi.Input['EnvironmentLoggingConfigurationDagProcessingLogsArgs'] dag_processing_logs: (Optional) Log configuration options for processing DAGs. See Module logging configuration for more information. Disabled by default.
        :param pulumi.Input['EnvironmentLoggingConfigurationSchedulerLogsArgs'] scheduler_logs: Log configuration options for the schedulers. See Module logging configuration for more information. Disabled by default.
        :param pulumi.Input['EnvironmentLoggingConfigurationTaskLogsArgs'] task_logs: Log configuration options for DAG tasks. See Module logging configuration for more information. Enabled by default with `INFO` log level.
        :param pulumi.Input['EnvironmentLoggingConfigurationWebserverLogsArgs'] webserver_logs: Log configuration options for the webservers. See Module logging configuration for more information. Disabled by default.
        :param pulumi.Input['EnvironmentLoggingConfigurationWorkerLogsArgs'] worker_logs: Log configuration options for the workers. See Module logging configuration for more information. Disabled by default.
        """
        if dag_processing_logs is not None:
            pulumi.set(__self__, "dag_processing_logs", dag_processing_logs)
        if scheduler_logs is not None:
            pulumi.set(__self__, "scheduler_logs", scheduler_logs)
        if task_logs is not None:
            pulumi.set(__self__, "task_logs", task_logs)
        if webserver_logs is not None:
            pulumi.set(__self__, "webserver_logs", webserver_logs)
        if worker_logs is not None:
            pulumi.set(__self__, "worker_logs", worker_logs)

    @property
    @pulumi.getter(name="dagProcessingLogs")
    def dag_processing_logs(self) -> Optional[pulumi.Input['EnvironmentLoggingConfigurationDagProcessingLogsArgs']]:
        """
        (Optional) Log configuration options for processing DAGs. See Module logging configuration for more information. Disabled by default.
        """
        return pulumi.get(self, "dag_processing_logs")

    @dag_processing_logs.setter
    def dag_processing_logs(self, value: Optional[pulumi.Input['EnvironmentLoggingConfigurationDagProcessingLogsArgs']]):
        pulumi.set(self, "dag_processing_logs", value)

    @property
    @pulumi.getter(name="schedulerLogs")
    def scheduler_logs(self) -> Optional[pulumi.Input['EnvironmentLoggingConfigurationSchedulerLogsArgs']]:
        """
        Log configuration options for the schedulers. See Module logging configuration for more information. Disabled by default.
        """
        return pulumi.get(self, "scheduler_logs")

    @scheduler_logs.setter
    def scheduler_logs(self, value: Optional[pulumi.Input['EnvironmentLoggingConfigurationSchedulerLogsArgs']]):
        pulumi.set(self, "scheduler_logs", value)

    @property
    @pulumi.getter(name="taskLogs")
    def task_logs(self) -> Optional[pulumi.Input['EnvironmentLoggingConfigurationTaskLogsArgs']]:
        """
        Log configuration options for DAG tasks. See Module logging configuration for more information. Enabled by default with `INFO` log level.
        """
        return pulumi.get(self, "task_logs")

    @task_logs.setter
    def task_logs(self, value: Optional[pulumi.Input['EnvironmentLoggingConfigurationTaskLogsArgs']]):
        pulumi.set(self, "task_logs", value)

    @property
    @pulumi.getter(name="webserverLogs")
    def webserver_logs(self) -> Optional[pulumi.Input['EnvironmentLoggingConfigurationWebserverLogsArgs']]:
        """
        Log configuration options for the webservers. See Module logging configuration for more information. Disabled by default.
        """
        return pulumi.get(self, "webserver_logs")

    @webserver_logs.setter
    def webserver_logs(self, value: Optional[pulumi.Input['EnvironmentLoggingConfigurationWebserverLogsArgs']]):
        pulumi.set(self, "webserver_logs", value)

    @property
    @pulumi.getter(name="workerLogs")
    def worker_logs(self) -> Optional[pulumi.Input['EnvironmentLoggingConfigurationWorkerLogsArgs']]:
        """
        Log configuration options for the workers. See Module logging configuration for more information. Disabled by default.
        """
        return pulumi.get(self, "worker_logs")

    @worker_logs.setter
    def worker_logs(self, value: Optional[pulumi.Input['EnvironmentLoggingConfigurationWorkerLogsArgs']]):
        pulumi.set(self, "worker_logs", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationDagProcessingLogsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_group_arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Enabling or disabling the collection of logs
        :param pulumi.Input[str] log_level: Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        if cloud_watch_log_group_arn is not None:
            pulumi.set(__self__, "cloud_watch_log_group_arn", cloud_watch_log_group_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)

    @property
    @pulumi.getter(name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cloud_watch_log_group_arn")

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_watch_log_group_arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enabling or disabling the collection of logs
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationSchedulerLogsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_group_arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Enabling or disabling the collection of logs
        :param pulumi.Input[str] log_level: Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        if cloud_watch_log_group_arn is not None:
            pulumi.set(__self__, "cloud_watch_log_group_arn", cloud_watch_log_group_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)

    @property
    @pulumi.getter(name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cloud_watch_log_group_arn")

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_watch_log_group_arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enabling or disabling the collection of logs
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationTaskLogsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_group_arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Enabling or disabling the collection of logs
        :param pulumi.Input[str] log_level: Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        if cloud_watch_log_group_arn is not None:
            pulumi.set(__self__, "cloud_watch_log_group_arn", cloud_watch_log_group_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)

    @property
    @pulumi.getter(name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cloud_watch_log_group_arn")

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_watch_log_group_arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enabling or disabling the collection of logs
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationWebserverLogsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_group_arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Enabling or disabling the collection of logs
        :param pulumi.Input[str] log_level: Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        if cloud_watch_log_group_arn is not None:
            pulumi.set(__self__, "cloud_watch_log_group_arn", cloud_watch_log_group_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)

    @property
    @pulumi.getter(name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cloud_watch_log_group_arn")

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_watch_log_group_arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enabling or disabling the collection of logs
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)


@pulumi.input_type
class EnvironmentLoggingConfigurationWorkerLogsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_group_arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 log_level: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] enabled: Enabling or disabling the collection of logs
        :param pulumi.Input[str] log_level: Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        if cloud_watch_log_group_arn is not None:
            pulumi.set(__self__, "cloud_watch_log_group_arn", cloud_watch_log_group_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)

    @property
    @pulumi.getter(name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cloud_watch_log_group_arn")

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_watch_log_group_arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enabling or disabling the collection of logs
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Logging level. Valid values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Will be `INFO` by default.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)


@pulumi.input_type
class EnvironmentNetworkConfigurationArgs:
    def __init__(__self__, *,
                 security_group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: Security groups IDs for the environment. At least one of the security group needs to allow MWAA resources to talk to each other, otherwise MWAA cannot be provisioned.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The private subnet IDs in which the environment should be created. MWAA requires two subnets.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Security groups IDs for the environment. At least one of the security group needs to allow MWAA resources to talk to each other, otherwise MWAA cannot be provisioned.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The private subnet IDs in which the environment should be created. MWAA requires two subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)


