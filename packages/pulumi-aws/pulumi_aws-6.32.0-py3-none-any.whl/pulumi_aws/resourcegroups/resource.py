# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResourceArgs', 'Resource']

@pulumi.input_type
class ResourceArgs:
    def __init__(__self__, *,
                 group_arn: pulumi.Input[str],
                 resource_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a Resource resource.
        :param pulumi.Input[str] group_arn: The name or the ARN of the resource group to add resources to.
               
               The following arguments are optional:
        :param pulumi.Input[str] resource_arn: The ARN of the resource to be added to the group.
        """
        pulumi.set(__self__, "group_arn", group_arn)
        pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> pulumi.Input[str]:
        """
        The name or the ARN of the resource group to add resources to.

        The following arguments are optional:
        """
        return pulumi.get(self, "group_arn")

    @group_arn.setter
    def group_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_arn", value)

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the resource to be added to the group.
        """
        return pulumi.get(self, "resource_arn")

    @resource_arn.setter
    def resource_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_arn", value)


@pulumi.input_type
class _ResourceState:
    def __init__(__self__, *,
                 group_arn: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Resource resources.
        :param pulumi.Input[str] group_arn: The name or the ARN of the resource group to add resources to.
               
               The following arguments are optional:
        :param pulumi.Input[str] resource_arn: The ARN of the resource to be added to the group.
        :param pulumi.Input[str] resource_type: The resource type of a resource, such as `AWS::EC2::Instance`.
        """
        if group_arn is not None:
            pulumi.set(__self__, "group_arn", group_arn)
        if resource_arn is not None:
            pulumi.set(__self__, "resource_arn", resource_arn)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The name or the ARN of the resource group to add resources to.

        The following arguments are optional:
        """
        return pulumi.get(self, "group_arn")

    @group_arn.setter
    def group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_arn", value)

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the resource to be added to the group.
        """
        return pulumi.get(self, "resource_arn")

    @resource_arn.setter
    def resource_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_arn", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The resource type of a resource, such as `AWS::EC2::Instance`.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)


class Resource(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_arn: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS Resource Groups Resource.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.DedicatedHost("example",
            instance_family="t3",
            availability_zone="us-east-1a",
            host_recovery="off",
            auto_placement="on")
        example_group = aws.resourcegroups.Group("example", name="example")
        example_resource = aws.resourcegroups.Resource("example",
            group_arn=example_group.arn,
            resource_arn=example.arn)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_arn: The name or the ARN of the resource group to add resources to.
               
               The following arguments are optional:
        :param pulumi.Input[str] resource_arn: The ARN of the resource to be added to the group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS Resource Groups Resource.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.DedicatedHost("example",
            instance_family="t3",
            availability_zone="us-east-1a",
            host_recovery="off",
            auto_placement="on")
        example_group = aws.resourcegroups.Group("example", name="example")
        example_resource = aws.resourcegroups.Resource("example",
            group_arn=example_group.arn,
            resource_arn=example.arn)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param ResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_arn: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceArgs.__new__(ResourceArgs)

            if group_arn is None and not opts.urn:
                raise TypeError("Missing required property 'group_arn'")
            __props__.__dict__["group_arn"] = group_arn
            if resource_arn is None and not opts.urn:
                raise TypeError("Missing required property 'resource_arn'")
            __props__.__dict__["resource_arn"] = resource_arn
            __props__.__dict__["resource_type"] = None
        super(Resource, __self__).__init__(
            'aws:resourcegroups/resource:Resource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            group_arn: Optional[pulumi.Input[str]] = None,
            resource_arn: Optional[pulumi.Input[str]] = None,
            resource_type: Optional[pulumi.Input[str]] = None) -> 'Resource':
        """
        Get an existing Resource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_arn: The name or the ARN of the resource group to add resources to.
               
               The following arguments are optional:
        :param pulumi.Input[str] resource_arn: The ARN of the resource to be added to the group.
        :param pulumi.Input[str] resource_type: The resource type of a resource, such as `AWS::EC2::Instance`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceState.__new__(_ResourceState)

        __props__.__dict__["group_arn"] = group_arn
        __props__.__dict__["resource_arn"] = resource_arn
        __props__.__dict__["resource_type"] = resource_type
        return Resource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> pulumi.Output[str]:
        """
        The name or the ARN of the resource group to add resources to.

        The following arguments are optional:
        """
        return pulumi.get(self, "group_arn")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the resource to be added to the group.
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[str]:
        """
        The resource type of a resource, such as `AWS::EC2::Instance`.
        """
        return pulumi.get(self, "resource_type")

