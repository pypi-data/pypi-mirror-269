# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetReplicationGroupResult',
    'AwaitableGetReplicationGroupResult',
    'get_replication_group',
    'get_replication_group_output',
]

@pulumi.output_type
class GetReplicationGroupResult:
    """
    A collection of values returned by getReplicationGroup.
    """
    def __init__(__self__, arn=None, auth_token_enabled=None, automatic_failover_enabled=None, configuration_endpoint_address=None, description=None, id=None, log_delivery_configurations=None, member_clusters=None, multi_az_enabled=None, node_type=None, num_cache_clusters=None, num_node_groups=None, port=None, primary_endpoint_address=None, reader_endpoint_address=None, replicas_per_node_group=None, replication_group_id=None, snapshot_retention_limit=None, snapshot_window=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auth_token_enabled and not isinstance(auth_token_enabled, bool):
            raise TypeError("Expected argument 'auth_token_enabled' to be a bool")
        pulumi.set(__self__, "auth_token_enabled", auth_token_enabled)
        if automatic_failover_enabled and not isinstance(automatic_failover_enabled, bool):
            raise TypeError("Expected argument 'automatic_failover_enabled' to be a bool")
        pulumi.set(__self__, "automatic_failover_enabled", automatic_failover_enabled)
        if configuration_endpoint_address and not isinstance(configuration_endpoint_address, str):
            raise TypeError("Expected argument 'configuration_endpoint_address' to be a str")
        pulumi.set(__self__, "configuration_endpoint_address", configuration_endpoint_address)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if log_delivery_configurations and not isinstance(log_delivery_configurations, list):
            raise TypeError("Expected argument 'log_delivery_configurations' to be a list")
        pulumi.set(__self__, "log_delivery_configurations", log_delivery_configurations)
        if member_clusters and not isinstance(member_clusters, list):
            raise TypeError("Expected argument 'member_clusters' to be a list")
        pulumi.set(__self__, "member_clusters", member_clusters)
        if multi_az_enabled and not isinstance(multi_az_enabled, bool):
            raise TypeError("Expected argument 'multi_az_enabled' to be a bool")
        pulumi.set(__self__, "multi_az_enabled", multi_az_enabled)
        if node_type and not isinstance(node_type, str):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, "node_type", node_type)
        if num_cache_clusters and not isinstance(num_cache_clusters, int):
            raise TypeError("Expected argument 'num_cache_clusters' to be a int")
        pulumi.set(__self__, "num_cache_clusters", num_cache_clusters)
        if num_node_groups and not isinstance(num_node_groups, int):
            raise TypeError("Expected argument 'num_node_groups' to be a int")
        pulumi.set(__self__, "num_node_groups", num_node_groups)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if primary_endpoint_address and not isinstance(primary_endpoint_address, str):
            raise TypeError("Expected argument 'primary_endpoint_address' to be a str")
        pulumi.set(__self__, "primary_endpoint_address", primary_endpoint_address)
        if reader_endpoint_address and not isinstance(reader_endpoint_address, str):
            raise TypeError("Expected argument 'reader_endpoint_address' to be a str")
        pulumi.set(__self__, "reader_endpoint_address", reader_endpoint_address)
        if replicas_per_node_group and not isinstance(replicas_per_node_group, int):
            raise TypeError("Expected argument 'replicas_per_node_group' to be a int")
        pulumi.set(__self__, "replicas_per_node_group", replicas_per_node_group)
        if replication_group_id and not isinstance(replication_group_id, str):
            raise TypeError("Expected argument 'replication_group_id' to be a str")
        pulumi.set(__self__, "replication_group_id", replication_group_id)
        if snapshot_retention_limit and not isinstance(snapshot_retention_limit, int):
            raise TypeError("Expected argument 'snapshot_retention_limit' to be a int")
        pulumi.set(__self__, "snapshot_retention_limit", snapshot_retention_limit)
        if snapshot_window and not isinstance(snapshot_window, str):
            raise TypeError("Expected argument 'snapshot_window' to be a str")
        pulumi.set(__self__, "snapshot_window", snapshot_window)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the created ElastiCache Replication Group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authTokenEnabled")
    def auth_token_enabled(self) -> bool:
        """
        Whether an AuthToken (password) is enabled.
        """
        return pulumi.get(self, "auth_token_enabled")

    @property
    @pulumi.getter(name="automaticFailoverEnabled")
    def automatic_failover_enabled(self) -> bool:
        """
        A flag whether a read-only replica will be automatically promoted to read/write primary if the existing primary fails.
        """
        return pulumi.get(self, "automatic_failover_enabled")

    @property
    @pulumi.getter(name="configurationEndpointAddress")
    def configuration_endpoint_address(self) -> str:
        """
        The configuration endpoint address to allow host discovery.
        """
        return pulumi.get(self, "configuration_endpoint_address")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the replication group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="logDeliveryConfigurations")
    def log_delivery_configurations(self) -> Sequence['outputs.GetReplicationGroupLogDeliveryConfigurationResult']:
        """
        Redis [SLOWLOG](https://redis.io/commands/slowlog) or Redis [Engine Log](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Log_Delivery.html#Log_contents-engine-log) delivery settings.
        """
        return pulumi.get(self, "log_delivery_configurations")

    @property
    @pulumi.getter(name="memberClusters")
    def member_clusters(self) -> Sequence[str]:
        """
        Identifiers of all the nodes that are part of this replication group.
        """
        return pulumi.get(self, "member_clusters")

    @property
    @pulumi.getter(name="multiAzEnabled")
    def multi_az_enabled(self) -> bool:
        """
        Whether Multi-AZ Support is enabled for the replication group.
        """
        return pulumi.get(self, "multi_az_enabled")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> str:
        """
        The cluster node type.
        """
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="numCacheClusters")
    def num_cache_clusters(self) -> int:
        """
        The number of cache clusters that the replication group has.
        """
        return pulumi.get(self, "num_cache_clusters")

    @property
    @pulumi.getter(name="numNodeGroups")
    def num_node_groups(self) -> int:
        """
        Number of node groups (shards) for the replication group.
        """
        return pulumi.get(self, "num_node_groups")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number on which the configuration endpoint will accept connections.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="primaryEndpointAddress")
    def primary_endpoint_address(self) -> str:
        """
        The endpoint of the primary node in this node group (shard).
        """
        return pulumi.get(self, "primary_endpoint_address")

    @property
    @pulumi.getter(name="readerEndpointAddress")
    def reader_endpoint_address(self) -> str:
        """
        The endpoint of the reader node in this node group (shard).
        """
        return pulumi.get(self, "reader_endpoint_address")

    @property
    @pulumi.getter(name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> int:
        """
        Number of replica nodes in each node group.
        """
        return pulumi.get(self, "replicas_per_node_group")

    @property
    @pulumi.getter(name="replicationGroupId")
    def replication_group_id(self) -> str:
        return pulumi.get(self, "replication_group_id")

    @property
    @pulumi.getter(name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> int:
        """
        The number of days for which ElastiCache retains automatic cache cluster snapshots before deleting them.
        """
        return pulumi.get(self, "snapshot_retention_limit")

    @property
    @pulumi.getter(name="snapshotWindow")
    def snapshot_window(self) -> str:
        """
        Daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).
        """
        return pulumi.get(self, "snapshot_window")


class AwaitableGetReplicationGroupResult(GetReplicationGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReplicationGroupResult(
            arn=self.arn,
            auth_token_enabled=self.auth_token_enabled,
            automatic_failover_enabled=self.automatic_failover_enabled,
            configuration_endpoint_address=self.configuration_endpoint_address,
            description=self.description,
            id=self.id,
            log_delivery_configurations=self.log_delivery_configurations,
            member_clusters=self.member_clusters,
            multi_az_enabled=self.multi_az_enabled,
            node_type=self.node_type,
            num_cache_clusters=self.num_cache_clusters,
            num_node_groups=self.num_node_groups,
            port=self.port,
            primary_endpoint_address=self.primary_endpoint_address,
            reader_endpoint_address=self.reader_endpoint_address,
            replicas_per_node_group=self.replicas_per_node_group,
            replication_group_id=self.replication_group_id,
            snapshot_retention_limit=self.snapshot_retention_limit,
            snapshot_window=self.snapshot_window)


def get_replication_group(replication_group_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReplicationGroupResult:
    """
    Use this data source to get information about an ElastiCache Replication Group.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    bar = aws.elasticache.get_replication_group(replication_group_id="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str replication_group_id: Identifier for the replication group.
    """
    __args__ = dict()
    __args__['replicationGroupId'] = replication_group_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:elasticache/getReplicationGroup:getReplicationGroup', __args__, opts=opts, typ=GetReplicationGroupResult).value

    return AwaitableGetReplicationGroupResult(
        arn=pulumi.get(__ret__, 'arn'),
        auth_token_enabled=pulumi.get(__ret__, 'auth_token_enabled'),
        automatic_failover_enabled=pulumi.get(__ret__, 'automatic_failover_enabled'),
        configuration_endpoint_address=pulumi.get(__ret__, 'configuration_endpoint_address'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        log_delivery_configurations=pulumi.get(__ret__, 'log_delivery_configurations'),
        member_clusters=pulumi.get(__ret__, 'member_clusters'),
        multi_az_enabled=pulumi.get(__ret__, 'multi_az_enabled'),
        node_type=pulumi.get(__ret__, 'node_type'),
        num_cache_clusters=pulumi.get(__ret__, 'num_cache_clusters'),
        num_node_groups=pulumi.get(__ret__, 'num_node_groups'),
        port=pulumi.get(__ret__, 'port'),
        primary_endpoint_address=pulumi.get(__ret__, 'primary_endpoint_address'),
        reader_endpoint_address=pulumi.get(__ret__, 'reader_endpoint_address'),
        replicas_per_node_group=pulumi.get(__ret__, 'replicas_per_node_group'),
        replication_group_id=pulumi.get(__ret__, 'replication_group_id'),
        snapshot_retention_limit=pulumi.get(__ret__, 'snapshot_retention_limit'),
        snapshot_window=pulumi.get(__ret__, 'snapshot_window'))


@_utilities.lift_output_func(get_replication_group)
def get_replication_group_output(replication_group_id: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetReplicationGroupResult]:
    """
    Use this data source to get information about an ElastiCache Replication Group.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    bar = aws.elasticache.get_replication_group(replication_group_id="example")
    ```
    <!--End PulumiCodeChooser -->


    :param str replication_group_id: Identifier for the replication group.
    """
    ...
