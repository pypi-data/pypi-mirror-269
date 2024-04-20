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
    'GetReplicationTaskResult',
    'AwaitableGetReplicationTaskResult',
    'get_replication_task',
    'get_replication_task_output',
]

@pulumi.output_type
class GetReplicationTaskResult:
    """
    A collection of values returned by getReplicationTask.
    """
    def __init__(__self__, cdc_start_position=None, cdc_start_time=None, id=None, migration_type=None, replication_instance_arn=None, replication_task_arn=None, replication_task_id=None, replication_task_settings=None, source_endpoint_arn=None, start_replication_task=None, status=None, table_mappings=None, tags=None, target_endpoint_arn=None):
        if cdc_start_position and not isinstance(cdc_start_position, str):
            raise TypeError("Expected argument 'cdc_start_position' to be a str")
        pulumi.set(__self__, "cdc_start_position", cdc_start_position)
        if cdc_start_time and not isinstance(cdc_start_time, str):
            raise TypeError("Expected argument 'cdc_start_time' to be a str")
        pulumi.set(__self__, "cdc_start_time", cdc_start_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if migration_type and not isinstance(migration_type, str):
            raise TypeError("Expected argument 'migration_type' to be a str")
        pulumi.set(__self__, "migration_type", migration_type)
        if replication_instance_arn and not isinstance(replication_instance_arn, str):
            raise TypeError("Expected argument 'replication_instance_arn' to be a str")
        pulumi.set(__self__, "replication_instance_arn", replication_instance_arn)
        if replication_task_arn and not isinstance(replication_task_arn, str):
            raise TypeError("Expected argument 'replication_task_arn' to be a str")
        pulumi.set(__self__, "replication_task_arn", replication_task_arn)
        if replication_task_id and not isinstance(replication_task_id, str):
            raise TypeError("Expected argument 'replication_task_id' to be a str")
        pulumi.set(__self__, "replication_task_id", replication_task_id)
        if replication_task_settings and not isinstance(replication_task_settings, str):
            raise TypeError("Expected argument 'replication_task_settings' to be a str")
        pulumi.set(__self__, "replication_task_settings", replication_task_settings)
        if source_endpoint_arn and not isinstance(source_endpoint_arn, str):
            raise TypeError("Expected argument 'source_endpoint_arn' to be a str")
        pulumi.set(__self__, "source_endpoint_arn", source_endpoint_arn)
        if start_replication_task and not isinstance(start_replication_task, bool):
            raise TypeError("Expected argument 'start_replication_task' to be a bool")
        pulumi.set(__self__, "start_replication_task", start_replication_task)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if table_mappings and not isinstance(table_mappings, str):
            raise TypeError("Expected argument 'table_mappings' to be a str")
        pulumi.set(__self__, "table_mappings", table_mappings)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_endpoint_arn and not isinstance(target_endpoint_arn, str):
            raise TypeError("Expected argument 'target_endpoint_arn' to be a str")
        pulumi.set(__self__, "target_endpoint_arn", target_endpoint_arn)

    @property
    @pulumi.getter(name="cdcStartPosition")
    def cdc_start_position(self) -> str:
        """
        (Conflicts with `cdc_start_time`) Indicates when you want a change data capture (CDC) operation to start. The value can be in date, checkpoint, or LSN/SCN format depending on the source engine. For more information, see [Determining a CDC native start point](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html#CHAP_Task.CDC.StartPoint.Native).
        """
        return pulumi.get(self, "cdc_start_position")

    @property
    @pulumi.getter(name="cdcStartTime")
    def cdc_start_time(self) -> str:
        """
        (Conflicts with `cdc_start_position`) The Unix timestamp integer for the start of the Change Data Capture (CDC) operation.
        """
        return pulumi.get(self, "cdc_start_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="migrationType")
    def migration_type(self) -> str:
        """
        The migration type. Can be one of `full-load | cdc | full-load-and-cdc`.
        """
        return pulumi.get(self, "migration_type")

    @property
    @pulumi.getter(name="replicationInstanceArn")
    def replication_instance_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the replication instance.
        """
        return pulumi.get(self, "replication_instance_arn")

    @property
    @pulumi.getter(name="replicationTaskArn")
    def replication_task_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) for the replication task.
        """
        return pulumi.get(self, "replication_task_arn")

    @property
    @pulumi.getter(name="replicationTaskId")
    def replication_task_id(self) -> str:
        return pulumi.get(self, "replication_task_id")

    @property
    @pulumi.getter(name="replicationTaskSettings")
    def replication_task_settings(self) -> str:
        """
        An escaped JSON string that contains the task settings. For a complete list of task settings, see [Task Settings for AWS Database Migration Service Tasks](http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.html).
        """
        return pulumi.get(self, "replication_task_settings")

    @property
    @pulumi.getter(name="sourceEndpointArn")
    def source_endpoint_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) string that uniquely identifies the source endpoint.
        """
        return pulumi.get(self, "source_endpoint_arn")

    @property
    @pulumi.getter(name="startReplicationTask")
    def start_replication_task(self) -> bool:
        """
        Whether to run or stop the replication task.
        """
        return pulumi.get(self, "start_replication_task")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Replication Task status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="tableMappings")
    def table_mappings(self) -> str:
        """
        An escaped JSON string that contains the table mappings. For information on table mapping see [Using Table Mapping with an AWS Database Migration Service Task to Select and Filter Data](http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html)
        """
        return pulumi.get(self, "table_mappings")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetEndpointArn")
    def target_endpoint_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) string that uniquely identifies the target endpoint.
        """
        return pulumi.get(self, "target_endpoint_arn")


class AwaitableGetReplicationTaskResult(GetReplicationTaskResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReplicationTaskResult(
            cdc_start_position=self.cdc_start_position,
            cdc_start_time=self.cdc_start_time,
            id=self.id,
            migration_type=self.migration_type,
            replication_instance_arn=self.replication_instance_arn,
            replication_task_arn=self.replication_task_arn,
            replication_task_id=self.replication_task_id,
            replication_task_settings=self.replication_task_settings,
            source_endpoint_arn=self.source_endpoint_arn,
            start_replication_task=self.start_replication_task,
            status=self.status,
            table_mappings=self.table_mappings,
            tags=self.tags,
            target_endpoint_arn=self.target_endpoint_arn)


def get_replication_task(replication_task_id: Optional[str] = None,
                         tags: Optional[Mapping[str, str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReplicationTaskResult:
    """
    Data source for managing an AWS DMS (Database Migration) Replication Task.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.dms.get_replication_task(replication_task_id=test_aws_dms_replication_task["replicationTaskId"])
    ```
    <!--End PulumiCodeChooser -->


    :param str replication_task_id: The replication task identifier.
           
           - Must contain from 1 to 255 alphanumeric characters or hyphens.
           - First character must be a letter.
           - Cannot end with a hyphen.
           - Cannot contain two consecutive hyphens.
    """
    __args__ = dict()
    __args__['replicationTaskId'] = replication_task_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:dms/getReplicationTask:getReplicationTask', __args__, opts=opts, typ=GetReplicationTaskResult).value

    return AwaitableGetReplicationTaskResult(
        cdc_start_position=pulumi.get(__ret__, 'cdc_start_position'),
        cdc_start_time=pulumi.get(__ret__, 'cdc_start_time'),
        id=pulumi.get(__ret__, 'id'),
        migration_type=pulumi.get(__ret__, 'migration_type'),
        replication_instance_arn=pulumi.get(__ret__, 'replication_instance_arn'),
        replication_task_arn=pulumi.get(__ret__, 'replication_task_arn'),
        replication_task_id=pulumi.get(__ret__, 'replication_task_id'),
        replication_task_settings=pulumi.get(__ret__, 'replication_task_settings'),
        source_endpoint_arn=pulumi.get(__ret__, 'source_endpoint_arn'),
        start_replication_task=pulumi.get(__ret__, 'start_replication_task'),
        status=pulumi.get(__ret__, 'status'),
        table_mappings=pulumi.get(__ret__, 'table_mappings'),
        tags=pulumi.get(__ret__, 'tags'),
        target_endpoint_arn=pulumi.get(__ret__, 'target_endpoint_arn'))


@_utilities.lift_output_func(get_replication_task)
def get_replication_task_output(replication_task_id: Optional[pulumi.Input[str]] = None,
                                tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetReplicationTaskResult]:
    """
    Data source for managing an AWS DMS (Database Migration) Replication Task.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.dms.get_replication_task(replication_task_id=test_aws_dms_replication_task["replicationTaskId"])
    ```
    <!--End PulumiCodeChooser -->


    :param str replication_task_id: The replication task identifier.
           
           - Must contain from 1 to 255 alphanumeric characters or hyphens.
           - First character must be a letter.
           - Cannot end with a hyphen.
           - Cannot contain two consecutive hyphens.
    """
    ...
