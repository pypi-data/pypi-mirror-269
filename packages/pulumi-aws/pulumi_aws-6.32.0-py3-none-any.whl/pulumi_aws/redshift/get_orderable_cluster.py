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
    'GetOrderableClusterResult',
    'AwaitableGetOrderableClusterResult',
    'get_orderable_cluster',
    'get_orderable_cluster_output',
]

@pulumi.output_type
class GetOrderableClusterResult:
    """
    A collection of values returned by getOrderableCluster.
    """
    def __init__(__self__, availability_zones=None, cluster_type=None, cluster_version=None, id=None, node_type=None, preferred_node_types=None):
        if availability_zones and not isinstance(availability_zones, list):
            raise TypeError("Expected argument 'availability_zones' to be a list")
        pulumi.set(__self__, "availability_zones", availability_zones)
        if cluster_type and not isinstance(cluster_type, str):
            raise TypeError("Expected argument 'cluster_type' to be a str")
        pulumi.set(__self__, "cluster_type", cluster_type)
        if cluster_version and not isinstance(cluster_version, str):
            raise TypeError("Expected argument 'cluster_version' to be a str")
        pulumi.set(__self__, "cluster_version", cluster_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if node_type and not isinstance(node_type, str):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, "node_type", node_type)
        if preferred_node_types and not isinstance(preferred_node_types, list):
            raise TypeError("Expected argument 'preferred_node_types' to be a list")
        pulumi.set(__self__, "preferred_node_types", preferred_node_types)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Sequence[str]:
        """
        List of Availability Zone names where the Redshift Cluster is available.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> str:
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="clusterVersion")
    def cluster_version(self) -> str:
        return pulumi.get(self, "cluster_version")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="nodeType")
    def node_type(self) -> str:
        return pulumi.get(self, "node_type")

    @property
    @pulumi.getter(name="preferredNodeTypes")
    def preferred_node_types(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_node_types")


class AwaitableGetOrderableClusterResult(GetOrderableClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrderableClusterResult(
            availability_zones=self.availability_zones,
            cluster_type=self.cluster_type,
            cluster_version=self.cluster_version,
            id=self.id,
            node_type=self.node_type,
            preferred_node_types=self.preferred_node_types)


def get_orderable_cluster(cluster_type: Optional[str] = None,
                          cluster_version: Optional[str] = None,
                          node_type: Optional[str] = None,
                          preferred_node_types: Optional[Sequence[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrderableClusterResult:
    """
    Information about Redshift Orderable Clusters and valid parameter combinations.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.redshift.get_orderable_cluster(cluster_type="multi-node",
        preferred_node_types=[
            "dc2.large",
            "ds2.xlarge",
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param str cluster_type: Reshift Cluster typeE.g., `multi-node` or `single-node`
    :param str cluster_version: Redshift Cluster versionE.g., `1.0`
    :param str node_type: Redshift Cluster node typeE.g., `dc2.8xlarge`
    :param Sequence[str] preferred_node_types: Ordered list of preferred Redshift Cluster node types. The first match in this list will be returned. If no preferred matches are found and the original search returned more than one result, an error is returned.
    """
    __args__ = dict()
    __args__['clusterType'] = cluster_type
    __args__['clusterVersion'] = cluster_version
    __args__['nodeType'] = node_type
    __args__['preferredNodeTypes'] = preferred_node_types
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:redshift/getOrderableCluster:getOrderableCluster', __args__, opts=opts, typ=GetOrderableClusterResult).value

    return AwaitableGetOrderableClusterResult(
        availability_zones=pulumi.get(__ret__, 'availability_zones'),
        cluster_type=pulumi.get(__ret__, 'cluster_type'),
        cluster_version=pulumi.get(__ret__, 'cluster_version'),
        id=pulumi.get(__ret__, 'id'),
        node_type=pulumi.get(__ret__, 'node_type'),
        preferred_node_types=pulumi.get(__ret__, 'preferred_node_types'))


@_utilities.lift_output_func(get_orderable_cluster)
def get_orderable_cluster_output(cluster_type: Optional[pulumi.Input[Optional[str]]] = None,
                                 cluster_version: Optional[pulumi.Input[Optional[str]]] = None,
                                 node_type: Optional[pulumi.Input[Optional[str]]] = None,
                                 preferred_node_types: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrderableClusterResult]:
    """
    Information about Redshift Orderable Clusters and valid parameter combinations.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.redshift.get_orderable_cluster(cluster_type="multi-node",
        preferred_node_types=[
            "dc2.large",
            "ds2.xlarge",
        ])
    ```
    <!--End PulumiCodeChooser -->


    :param str cluster_type: Reshift Cluster typeE.g., `multi-node` or `single-node`
    :param str cluster_version: Redshift Cluster versionE.g., `1.0`
    :param str node_type: Redshift Cluster node typeE.g., `dc2.8xlarge`
    :param Sequence[str] preferred_node_types: Ordered list of preferred Redshift Cluster node types. The first match in this list will be returned. If no preferred matches are found and the original search returned more than one result, an error is returned.
    """
    ...
