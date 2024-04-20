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
    'GetAttachmentResult',
    'AwaitableGetAttachmentResult',
    'get_attachment',
    'get_attachment_output',
]

@pulumi.output_type
class GetAttachmentResult:
    """
    A collection of values returned by getAttachment.
    """
    def __init__(__self__, arn=None, association_state=None, association_transit_gateway_route_table_id=None, filters=None, id=None, resource_id=None, resource_owner_id=None, resource_type=None, state=None, tags=None, transit_gateway_attachment_id=None, transit_gateway_id=None, transit_gateway_owner_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if association_state and not isinstance(association_state, str):
            raise TypeError("Expected argument 'association_state' to be a str")
        pulumi.set(__self__, "association_state", association_state)
        if association_transit_gateway_route_table_id and not isinstance(association_transit_gateway_route_table_id, str):
            raise TypeError("Expected argument 'association_transit_gateway_route_table_id' to be a str")
        pulumi.set(__self__, "association_transit_gateway_route_table_id", association_transit_gateway_route_table_id)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if resource_owner_id and not isinstance(resource_owner_id, str):
            raise TypeError("Expected argument 'resource_owner_id' to be a str")
        pulumi.set(__self__, "resource_owner_id", resource_owner_id)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if transit_gateway_attachment_id and not isinstance(transit_gateway_attachment_id, str):
            raise TypeError("Expected argument 'transit_gateway_attachment_id' to be a str")
        pulumi.set(__self__, "transit_gateway_attachment_id", transit_gateway_attachment_id)
        if transit_gateway_id and not isinstance(transit_gateway_id, str):
            raise TypeError("Expected argument 'transit_gateway_id' to be a str")
        pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        if transit_gateway_owner_id and not isinstance(transit_gateway_owner_id, str):
            raise TypeError("Expected argument 'transit_gateway_owner_id' to be a str")
        pulumi.set(__self__, "transit_gateway_owner_id", transit_gateway_owner_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the attachment.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="associationState")
    def association_state(self) -> str:
        """
        The state of the association (see [the underlying AWS API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_TransitGatewayAttachmentAssociation.html) for valid values).
        """
        return pulumi.get(self, "association_state")

    @property
    @pulumi.getter(name="associationTransitGatewayRouteTableId")
    def association_transit_gateway_route_table_id(self) -> str:
        """
        The ID of the route table for the transit gateway.
        """
        return pulumi.get(self, "association_transit_gateway_route_table_id")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAttachmentFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        ID of the resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="resourceOwnerId")
    def resource_owner_id(self) -> str:
        """
        ID of the AWS account that owns the resource.
        """
        return pulumi.get(self, "resource_owner_id")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Attachment state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Key-value tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> str:
        return pulumi.get(self, "transit_gateway_attachment_id")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> str:
        """
        ID of the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @property
    @pulumi.getter(name="transitGatewayOwnerId")
    def transit_gateway_owner_id(self) -> str:
        """
        The ID of the AWS account that owns the transit gateway.
        """
        return pulumi.get(self, "transit_gateway_owner_id")


class AwaitableGetAttachmentResult(GetAttachmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttachmentResult(
            arn=self.arn,
            association_state=self.association_state,
            association_transit_gateway_route_table_id=self.association_transit_gateway_route_table_id,
            filters=self.filters,
            id=self.id,
            resource_id=self.resource_id,
            resource_owner_id=self.resource_owner_id,
            resource_type=self.resource_type,
            state=self.state,
            tags=self.tags,
            transit_gateway_attachment_id=self.transit_gateway_attachment_id,
            transit_gateway_id=self.transit_gateway_id,
            transit_gateway_owner_id=self.transit_gateway_owner_id)


def get_attachment(filters: Optional[Sequence[pulumi.InputType['GetAttachmentFilterArgs']]] = None,
                   tags: Optional[Mapping[str, str]] = None,
                   transit_gateway_attachment_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttachmentResult:
    """
    Get information on an EC2 Transit Gateway's attachment to a resource.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2transitgateway.get_attachment(filters=[
        aws.ec2transitgateway.GetAttachmentFilterArgs(
            name="transit-gateway-id",
            values=[example_aws_ec2_transit_gateway["id"]],
        ),
        aws.ec2transitgateway.GetAttachmentFilterArgs(
            name="resource-type",
            values=["peering"],
        ),
    ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetAttachmentFilterArgs']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    :param Mapping[str, str] tags: Key-value tags for the attachment.
    :param str transit_gateway_attachment_id: ID of the attachment.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    __args__['transitGatewayAttachmentId'] = transit_gateway_attachment_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2transitgateway/getAttachment:getAttachment', __args__, opts=opts, typ=GetAttachmentResult).value

    return AwaitableGetAttachmentResult(
        arn=pulumi.get(__ret__, 'arn'),
        association_state=pulumi.get(__ret__, 'association_state'),
        association_transit_gateway_route_table_id=pulumi.get(__ret__, 'association_transit_gateway_route_table_id'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        resource_id=pulumi.get(__ret__, 'resource_id'),
        resource_owner_id=pulumi.get(__ret__, 'resource_owner_id'),
        resource_type=pulumi.get(__ret__, 'resource_type'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        transit_gateway_attachment_id=pulumi.get(__ret__, 'transit_gateway_attachment_id'),
        transit_gateway_id=pulumi.get(__ret__, 'transit_gateway_id'),
        transit_gateway_owner_id=pulumi.get(__ret__, 'transit_gateway_owner_id'))


@_utilities.lift_output_func(get_attachment)
def get_attachment_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAttachmentFilterArgs']]]]] = None,
                          tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                          transit_gateway_attachment_id: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttachmentResult]:
    """
    Get information on an EC2 Transit Gateway's attachment to a resource.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2transitgateway.get_attachment(filters=[
        aws.ec2transitgateway.GetAttachmentFilterArgs(
            name="transit-gateway-id",
            values=[example_aws_ec2_transit_gateway["id"]],
        ),
        aws.ec2transitgateway.GetAttachmentFilterArgs(
            name="resource-type",
            values=["peering"],
        ),
    ])
    ```
    <!--End PulumiCodeChooser -->


    :param Sequence[pulumi.InputType['GetAttachmentFilterArgs']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    :param Mapping[str, str] tags: Key-value tags for the attachment.
    :param str transit_gateway_attachment_id: ID of the attachment.
    """
    ...
