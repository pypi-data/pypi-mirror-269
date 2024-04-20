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
    'CloudFormationTypeLoggingConfig',
    'StackSetAutoDeployment',
    'StackSetInstanceDeploymentTargets',
    'StackSetInstanceOperationPreferences',
    'StackSetInstanceStackInstanceSummary',
    'StackSetManagedExecution',
    'StackSetOperationPreferences',
    'GetCloudFormationTypeLoggingConfigResult',
]

@pulumi.output_type
class CloudFormationTypeLoggingConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroupName":
            suggest = "log_group_name"
        elif key == "logRoleArn":
            suggest = "log_role_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CloudFormationTypeLoggingConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CloudFormationTypeLoggingConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CloudFormationTypeLoggingConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group_name: str,
                 log_role_arn: str):
        """
        :param str log_group_name: Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        :param str log_role_arn: Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> str:
        """
        Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        return pulumi.get(self, "log_role_arn")


@pulumi.output_type
class StackSetAutoDeployment(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "retainStacksOnAccountRemoval":
            suggest = "retain_stacks_on_account_removal"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StackSetAutoDeployment. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StackSetAutoDeployment.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StackSetAutoDeployment.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 enabled: Optional[bool] = None,
                 retain_stacks_on_account_removal: Optional[bool] = None):
        """
        :param bool enabled: Whether or not auto-deployment is enabled.
        :param bool retain_stacks_on_account_removal: Whether or not to retain stacks when the account is removed.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retain_stacks_on_account_removal is not None:
            pulumi.set(__self__, "retain_stacks_on_account_removal", retain_stacks_on_account_removal)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Whether or not auto-deployment is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="retainStacksOnAccountRemoval")
    def retain_stacks_on_account_removal(self) -> Optional[bool]:
        """
        Whether or not to retain stacks when the account is removed.
        """
        return pulumi.get(self, "retain_stacks_on_account_removal")


@pulumi.output_type
class StackSetInstanceDeploymentTargets(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "organizationalUnitIds":
            suggest = "organizational_unit_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StackSetInstanceDeploymentTargets. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StackSetInstanceDeploymentTargets.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StackSetInstanceDeploymentTargets.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 organizational_unit_ids: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] organizational_unit_ids: The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        if organizational_unit_ids is not None:
            pulumi.set(__self__, "organizational_unit_ids", organizational_unit_ids)

    @property
    @pulumi.getter(name="organizationalUnitIds")
    def organizational_unit_ids(self) -> Optional[Sequence[str]]:
        """
        The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        return pulumi.get(self, "organizational_unit_ids")


@pulumi.output_type
class StackSetInstanceOperationPreferences(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failureToleranceCount":
            suggest = "failure_tolerance_count"
        elif key == "failureTolerancePercentage":
            suggest = "failure_tolerance_percentage"
        elif key == "maxConcurrentCount":
            suggest = "max_concurrent_count"
        elif key == "maxConcurrentPercentage":
            suggest = "max_concurrent_percentage"
        elif key == "regionConcurrencyType":
            suggest = "region_concurrency_type"
        elif key == "regionOrders":
            suggest = "region_orders"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StackSetInstanceOperationPreferences. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StackSetInstanceOperationPreferences.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StackSetInstanceOperationPreferences.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 failure_tolerance_count: Optional[int] = None,
                 failure_tolerance_percentage: Optional[int] = None,
                 max_concurrent_count: Optional[int] = None,
                 max_concurrent_percentage: Optional[int] = None,
                 region_concurrency_type: Optional[str] = None,
                 region_orders: Optional[Sequence[str]] = None):
        """
        :param int failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        :param int failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        :param int max_concurrent_count: The maximum number of accounts in which to perform this operation at one time.
        :param int max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time.
        :param str region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time. Valid values are `SEQUENTIAL` and `PARALLEL`.
        :param Sequence[str] region_orders: The order of the Regions in where you want to perform the stack operation.
        """
        if failure_tolerance_count is not None:
            pulumi.set(__self__, "failure_tolerance_count", failure_tolerance_count)
        if failure_tolerance_percentage is not None:
            pulumi.set(__self__, "failure_tolerance_percentage", failure_tolerance_percentage)
        if max_concurrent_count is not None:
            pulumi.set(__self__, "max_concurrent_count", max_concurrent_count)
        if max_concurrent_percentage is not None:
            pulumi.set(__self__, "max_concurrent_percentage", max_concurrent_percentage)
        if region_concurrency_type is not None:
            pulumi.set(__self__, "region_concurrency_type", region_concurrency_type)
        if region_orders is not None:
            pulumi.set(__self__, "region_orders", region_orders)

    @property
    @pulumi.getter(name="failureToleranceCount")
    def failure_tolerance_count(self) -> Optional[int]:
        """
        The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_count")

    @property
    @pulumi.getter(name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> Optional[int]:
        """
        The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_percentage")

    @property
    @pulumi.getter(name="maxConcurrentCount")
    def max_concurrent_count(self) -> Optional[int]:
        """
        The maximum number of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_count")

    @property
    @pulumi.getter(name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> Optional[int]:
        """
        The maximum percentage of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_percentage")

    @property
    @pulumi.getter(name="regionConcurrencyType")
    def region_concurrency_type(self) -> Optional[str]:
        """
        The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time. Valid values are `SEQUENTIAL` and `PARALLEL`.
        """
        return pulumi.get(self, "region_concurrency_type")

    @property
    @pulumi.getter(name="regionOrders")
    def region_orders(self) -> Optional[Sequence[str]]:
        """
        The order of the Regions in where you want to perform the stack operation.
        """
        return pulumi.get(self, "region_orders")


@pulumi.output_type
class StackSetInstanceStackInstanceSummary(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accountId":
            suggest = "account_id"
        elif key == "organizationalUnitId":
            suggest = "organizational_unit_id"
        elif key == "stackId":
            suggest = "stack_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StackSetInstanceStackInstanceSummary. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StackSetInstanceStackInstanceSummary.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StackSetInstanceStackInstanceSummary.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 account_id: Optional[str] = None,
                 organizational_unit_id: Optional[str] = None,
                 stack_id: Optional[str] = None):
        """
        :param str account_id: Target AWS Account ID to create a Stack based on the StackSet. Defaults to current account.
        :param str organizational_unit_id: Organizational unit ID in which the stack is deployed.
        :param str stack_id: Stack identifier.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if organizational_unit_id is not None:
            pulumi.set(__self__, "organizational_unit_id", organizational_unit_id)
        if stack_id is not None:
            pulumi.set(__self__, "stack_id", stack_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        """
        Target AWS Account ID to create a Stack based on the StackSet. Defaults to current account.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="organizationalUnitId")
    def organizational_unit_id(self) -> Optional[str]:
        """
        Organizational unit ID in which the stack is deployed.
        """
        return pulumi.get(self, "organizational_unit_id")

    @property
    @pulumi.getter(name="stackId")
    def stack_id(self) -> Optional[str]:
        """
        Stack identifier.
        """
        return pulumi.get(self, "stack_id")


@pulumi.output_type
class StackSetManagedExecution(dict):
    def __init__(__self__, *,
                 active: Optional[bool] = None):
        """
        :param bool active: When set to true, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. Default is false.
        """
        if active is not None:
            pulumi.set(__self__, "active", active)

    @property
    @pulumi.getter
    def active(self) -> Optional[bool]:
        """
        When set to true, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. Default is false.
        """
        return pulumi.get(self, "active")


@pulumi.output_type
class StackSetOperationPreferences(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failureToleranceCount":
            suggest = "failure_tolerance_count"
        elif key == "failureTolerancePercentage":
            suggest = "failure_tolerance_percentage"
        elif key == "maxConcurrentCount":
            suggest = "max_concurrent_count"
        elif key == "maxConcurrentPercentage":
            suggest = "max_concurrent_percentage"
        elif key == "regionConcurrencyType":
            suggest = "region_concurrency_type"
        elif key == "regionOrders":
            suggest = "region_orders"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StackSetOperationPreferences. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StackSetOperationPreferences.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StackSetOperationPreferences.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 failure_tolerance_count: Optional[int] = None,
                 failure_tolerance_percentage: Optional[int] = None,
                 max_concurrent_count: Optional[int] = None,
                 max_concurrent_percentage: Optional[int] = None,
                 region_concurrency_type: Optional[str] = None,
                 region_orders: Optional[Sequence[str]] = None):
        """
        :param int failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        :param int failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        :param int max_concurrent_count: The maximum number of accounts in which to perform this operation at one time.
        :param int max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time.
        :param str region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.
        :param Sequence[str] region_orders: The order of the Regions in where you want to perform the stack operation.
        """
        if failure_tolerance_count is not None:
            pulumi.set(__self__, "failure_tolerance_count", failure_tolerance_count)
        if failure_tolerance_percentage is not None:
            pulumi.set(__self__, "failure_tolerance_percentage", failure_tolerance_percentage)
        if max_concurrent_count is not None:
            pulumi.set(__self__, "max_concurrent_count", max_concurrent_count)
        if max_concurrent_percentage is not None:
            pulumi.set(__self__, "max_concurrent_percentage", max_concurrent_percentage)
        if region_concurrency_type is not None:
            pulumi.set(__self__, "region_concurrency_type", region_concurrency_type)
        if region_orders is not None:
            pulumi.set(__self__, "region_orders", region_orders)

    @property
    @pulumi.getter(name="failureToleranceCount")
    def failure_tolerance_count(self) -> Optional[int]:
        """
        The number of accounts, per Region, for which this operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_count")

    @property
    @pulumi.getter(name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> Optional[int]:
        """
        The percentage of accounts, per Region, for which this stack operation can fail before AWS CloudFormation stops the operation in that Region.
        """
        return pulumi.get(self, "failure_tolerance_percentage")

    @property
    @pulumi.getter(name="maxConcurrentCount")
    def max_concurrent_count(self) -> Optional[int]:
        """
        The maximum number of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_count")

    @property
    @pulumi.getter(name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> Optional[int]:
        """
        The maximum percentage of accounts in which to perform this operation at one time.
        """
        return pulumi.get(self, "max_concurrent_percentage")

    @property
    @pulumi.getter(name="regionConcurrencyType")
    def region_concurrency_type(self) -> Optional[str]:
        """
        The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.
        """
        return pulumi.get(self, "region_concurrency_type")

    @property
    @pulumi.getter(name="regionOrders")
    def region_orders(self) -> Optional[Sequence[str]]:
        """
        The order of the Regions in where you want to perform the stack operation.
        """
        return pulumi.get(self, "region_orders")


@pulumi.output_type
class GetCloudFormationTypeLoggingConfigResult(dict):
    def __init__(__self__, *,
                 log_group_name: str,
                 log_role_arn: str):
        """
        :param str log_group_name: Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        :param str log_role_arn: ARN of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> str:
        """
        Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> str:
        """
        ARN of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        return pulumi.get(self, "log_role_arn")


