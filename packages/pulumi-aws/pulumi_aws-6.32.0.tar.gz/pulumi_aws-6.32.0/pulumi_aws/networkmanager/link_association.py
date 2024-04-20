# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LinkAssociationArgs', 'LinkAssociation']

@pulumi.input_type
class LinkAssociationArgs:
    def __init__(__self__, *,
                 device_id: pulumi.Input[str],
                 global_network_id: pulumi.Input[str],
                 link_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a LinkAssociation resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        """
        pulumi.set(__self__, "device_id", device_id)
        pulumi.set(__self__, "global_network_id", global_network_id)
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
    @pulumi.getter(name="linkId")
    def link_id(self) -> pulumi.Input[str]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

    @link_id.setter
    def link_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "link_id", value)


@pulumi.input_type
class _LinkAssociationState:
    def __init__(__self__, *,
                 device_id: Optional[pulumi.Input[str]] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 link_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LinkAssociation resources.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        """
        if device_id is not None:
            pulumi.set(__self__, "device_id", device_id)
        if global_network_id is not None:
            pulumi.set(__self__, "global_network_id", global_network_id)
        if link_id is not None:
            pulumi.set(__self__, "link_id", link_id)

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


class LinkAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_id: Optional[pulumi.Input[str]] = None,
                 global_network_id: Optional[pulumi.Input[str]] = None,
                 link_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a link to a device.
        A device can be associated to multiple links and a link can be associated to multiple devices.
        The device and link must be in the same global network and the same site.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkmanager.LinkAssociation("example",
            global_network_id=example_aws_networkmanager_global_network["id"],
            link_id=example_aws_networkmanager_link["id"],
            device_id=example_aws_networkmanager_device["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_networkmanager_link_association` using the global network ID, link ID and device ID. For example:

        ```sh
        $ pulumi import aws:networkmanager/linkAssociation:LinkAssociation example global-network-0d47f6t230mz46dy4,link-444555aaabbb11223,device-07f6fd08867abc123
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LinkAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a link to a device.
        A device can be associated to multiple links and a link can be associated to multiple devices.
        The device and link must be in the same global network and the same site.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkmanager.LinkAssociation("example",
            global_network_id=example_aws_networkmanager_global_network["id"],
            link_id=example_aws_networkmanager_link["id"],
            device_id=example_aws_networkmanager_device["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_networkmanager_link_association` using the global network ID, link ID and device ID. For example:

        ```sh
        $ pulumi import aws:networkmanager/linkAssociation:LinkAssociation example global-network-0d47f6t230mz46dy4,link-444555aaabbb11223,device-07f6fd08867abc123
        ```

        :param str resource_name: The name of the resource.
        :param LinkAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LinkAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
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
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LinkAssociationArgs.__new__(LinkAssociationArgs)

            if device_id is None and not opts.urn:
                raise TypeError("Missing required property 'device_id'")
            __props__.__dict__["device_id"] = device_id
            if global_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'global_network_id'")
            __props__.__dict__["global_network_id"] = global_network_id
            if link_id is None and not opts.urn:
                raise TypeError("Missing required property 'link_id'")
            __props__.__dict__["link_id"] = link_id
        super(LinkAssociation, __self__).__init__(
            'aws:networkmanager/linkAssociation:LinkAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            device_id: Optional[pulumi.Input[str]] = None,
            global_network_id: Optional[pulumi.Input[str]] = None,
            link_id: Optional[pulumi.Input[str]] = None) -> 'LinkAssociation':
        """
        Get an existing LinkAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_id: The ID of the device.
        :param pulumi.Input[str] global_network_id: The ID of the global network.
        :param pulumi.Input[str] link_id: The ID of the link.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LinkAssociationState.__new__(_LinkAssociationState)

        __props__.__dict__["device_id"] = device_id
        __props__.__dict__["global_network_id"] = global_network_id
        __props__.__dict__["link_id"] = link_id
        return LinkAssociation(resource_name, opts=opts, __props__=__props__)

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
    def link_id(self) -> pulumi.Output[str]:
        """
        The ID of the link.
        """
        return pulumi.get(self, "link_id")

