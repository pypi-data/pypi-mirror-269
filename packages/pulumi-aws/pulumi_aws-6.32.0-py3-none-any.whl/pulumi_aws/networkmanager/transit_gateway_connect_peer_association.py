# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TransitGatewayConnectPeerAssociationArgs', 'TransitGatewayConnectPeerAssociation']

@pulumi.input_type
class TransitGatewayConnectPeerAssociationArgs:
    def __init__(__self__, *,
                 device_id: pulumi.Input[str],
                 global_network_id: pulumi.Input[str],
                 transit_gateway_connect_peer_arn: pulumi.Input[str],
                 link_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TransitGatewayConnectPeerAssociation resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] transit_gateway_connect_peer_arn: The Amazon Resource Name (ARN) of the Connect peer.
        :param pulumi.Input[str] link_id: The ID of the link.
        """
        pulumi.set(__self__, "device_id", device_id)
        pulumi.set(__self__, "global_network_id", global_network_id)
        pulumi.set(__self__, "transit_gateway_connect_peer_arn", transit_gateway_connect_peer_arn)
        if link_id is not None:
            pulumi.set(__self__, "link_id", link_id)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> pulumi.Input[str]:
        """
        The ID of the device.
        """
        return pulumi.get(self, "device_id")

    @device_id.setter
    def device_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_id", value)

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> pulumi.Input[str]:
        """
        The ID of the global network.
        """
        return pulumi.get(self, "global_network_id")

    @global_network_id.setter
    def global_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "global_network_id", value)

    @property
    @pulumi.getter(name="transitGatewayConnectPeerArn")
    def transit_gateway_connect_peer_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the Connect peer.
        """
        return pulumi.get(self, "transit_gateway_connect_peer_arn")

    @transit_gateway_connect_peer_arn.setter
    def transit_gateway_connect_peer_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_gateway_connect_peer_arn", value)

    @property
    @pulumi.getter(name="linkId")
    def link_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

    @link_id.setter
    def link_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "link_id", value)


@pulumi.input_type
class _TransitGatewayConnectPeerAssociationState:
    def __init__(__self__, *,
                 device_id: Optional[pulumi.Input[str]] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 link_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_connect_peer_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TransitGatewayConnectPeerAssociation resources.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        :param pulumi.Input[str] transit_gateway_connect_peer_arn: The Amazon Resource Name (ARN) of the Connect peer.
        """
        if device_id is not None:
            pulumi.set(__self__, "device_id", device_id)
        if global_network_id is not None:
            pulumi.set(__self__, "global_network_id", global_network_id)
        if link_id is not None:
            pulumi.set(__self__, "link_id", link_id)
        if transit_gateway_connect_peer_arn is not None:
            pulumi.set(__self__, "transit_gateway_connect_peer_arn", transit_gateway_connect_peer_arn)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the device.
        """
        return pulumi.get(self, "device_id")

    @device_id.setter
    def device_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device_id", value)

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the global network.
        """
        return pulumi.get(self, "global_network_id")

    @global_network_id.setter
    def global_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "global_network_id", value)

    @property
    @pulumi.getter(name="linkId")
    def link_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

    @link_id.setter
    def link_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "link_id", value)

    @property
    @pulumi.getter(name="transitGatewayConnectPeerArn")
    def transit_gateway_connect_peer_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Connect peer.
        """
        return pulumi.get(self, "transit_gateway_connect_peer_arn")

    @transit_gateway_connect_peer_arn.setter
    def transit_gateway_connect_peer_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_gateway_connect_peer_arn", value)


class TransitGatewayConnectPeerAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_id: Optional[pulumi.Input[str]] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 link_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_connect_peer_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a transit gateway Connect peer with a device, and optionally, with a link.
        If you specify a link, it must be associated with the specified device.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkmanager.TransitGatewayConnectPeerAssociation("example",
            global_network_id=example_aws_networkmanager_global_network["id"],
            device_id=example_aws_networkmanager_device["id"],
            transit_gateway_connect_peer_arn=example_aws_ec2_transit_gateway_connect_peer["arn"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_networkmanager_transit_gateway_connect_peer_association` using the global network ID and customer gateway ARN. For example:

        ```sh
        $ pulumi import aws:networkmanager/transitGatewayConnectPeerAssociation:TransitGatewayConnectPeerAssociation example global-network-0d47f6t230mz46dy4,arn:aws:ec2:us-west-2:123456789012:transit-gateway-connect-peer/tgw-connect-peer-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        :param pulumi.Input[str] transit_gateway_connect_peer_arn: The Amazon Resource Name (ARN) of the Connect peer.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransitGatewayConnectPeerAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a transit gateway Connect peer with a device, and optionally, with a link.
        If you specify a link, it must be associated with the specified device.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkmanager.TransitGatewayConnectPeerAssociation("example",
            global_network_id=example_aws_networkmanager_global_network["id"],
            device_id=example_aws_networkmanager_device["id"],
            transit_gateway_connect_peer_arn=example_aws_ec2_transit_gateway_connect_peer["arn"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_networkmanager_transit_gateway_connect_peer_association` using the global network ID and customer gateway ARN. For example:

        ```sh
        $ pulumi import aws:networkmanager/transitGatewayConnectPeerAssociation:TransitGatewayConnectPeerAssociation example global-network-0d47f6t230mz46dy4,arn:aws:ec2:us-west-2:123456789012:transit-gateway-connect-peer/tgw-connect-peer-12345678
        ```

        :param str resource_name: The name of the resource.
        :param TransitGatewayConnectPeerAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransitGatewayConnectPeerAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_id: Optional[pulumi.Input[str]] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 link_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_connect_peer_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TransitGatewayConnectPeerAssociationArgs.__new__(TransitGatewayConnectPeerAssociationArgs)

            if device_id is None and not opts.urn:
                raise TypeError("Missing required property 'device_id'")
            __props__.__dict__["device_id"] = device_id
            if global_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'global_network_id'")
            __props__.__dict__["global_network_id"] = global_network_id
            __props__.__dict__["link_id"] = link_id
            if transit_gateway_connect_peer_arn is None and not opts.urn:
                raise TypeError("Missing required property 'transit_gateway_connect_peer_arn'")
            __props__.__dict__["transit_gateway_connect_peer_arn"] = transit_gateway_connect_peer_arn
        super(TransitGatewayConnectPeerAssociation, __self__).__init__(
            'aws:networkmanager/transitGatewayConnectPeerAssociation:TransitGatewayConnectPeerAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            device_id: Optional[pulumi.Input[str]] = None,
            global_network_id: Optional[pulumi.Input[str]] = None,
            link_id: Optional[pulumi.Input[str]] = None,
            transit_gateway_connect_peer_arn: Optional[pulumi.Input[str]] = None) -> 'TransitGatewayConnectPeerAssociation':
        """
        Get an existing TransitGatewayConnectPeerAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        :param pulumi.Input[str] transit_gateway_connect_peer_arn: The Amazon Resource Name (ARN) of the Connect peer.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TransitGatewayConnectPeerAssociationState.__new__(_TransitGatewayConnectPeerAssociationState)

        __props__.__dict__["device_id"] = device_id
        __props__.__dict__["global_network_id"] = global_network_id
        __props__.__dict__["link_id"] = link_id
        __props__.__dict__["transit_gateway_connect_peer_arn"] = transit_gateway_connect_peer_arn
        return TransitGatewayConnectPeerAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> pulumi.Output[str]:
        """
        The ID of the device.
        """
        return pulumi.get(self, "device_id")

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> pulumi.Output[str]:
        """
        The ID of the global network.
        """
        return pulumi.get(self, "global_network_id")

    @property
    @pulumi.getter(name="linkId")
    def link_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

    @property
    @pulumi.getter(name="transitGatewayConnectPeerArn")
    def transit_gateway_connect_peer_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Connect peer.
        """
        return pulumi.get(self, "transit_gateway_connect_peer_arn")

