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
from ._inputs import *

__all__ = [
    'GetTransitGatewayRouteTablesResult',
    'AwaitableGetTransitGatewayRouteTablesResult',
    'get_transit_gateway_route_tables',
    'get_transit_gateway_route_tables_output',
]

@pulumi.output_type
class GetTransitGatewayRouteTablesResult:
    """
    A collection of values returned by getTransitGatewayRouteTables.
    """
    def __init__(__self__, filters=None, id=None, ids=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetTransitGatewayRouteTablesFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        Set of Transit Gateway Route Table identifiers.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetTransitGatewayRouteTablesResult(GetTransitGatewayRouteTablesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTransitGatewayRouteTablesResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags)


def get_transit_gateway_route_tables(filters: Optional[Sequence[pulumi.InputType['GetTransitGatewayRouteTablesFilterArgs']]] = None,
                                     tags: Optional[Mapping[str, str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTransitGatewayRouteTablesResult:
    """
    Provides information for multiple EC2 Transit Gateway Route Tables, such as their identifiers.

    ## Example Usage

    The following shows outputting all Transit Gateway Route Table Ids.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_transit_gateway_route_tables()
    pulumi.export("example", example.ids)
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetTransitGatewayRouteTablesFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired transit gateway route table.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getTransitGatewayRouteTables:getTransitGatewayRouteTables', __args__, opts=opts, typ=GetTransitGatewayRouteTablesResult).value

    return AwaitableGetTransitGatewayRouteTablesResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_transit_gateway_route_tables)
def get_transit_gateway_route_tables_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetTransitGatewayRouteTablesFilterArgs']]]]] = None,
                                            tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTransitGatewayRouteTablesResult]:
    """
    Provides information for multiple EC2 Transit Gateway Route Tables, such as their identifiers.

    ## Example Usage

    The following shows outputting all Transit Gateway Route Table Ids.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_transit_gateway_route_tables()
    pulumi.export("example", example.ids)
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetTransitGatewayRouteTablesFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired transit gateway route table.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    ...
