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

__all__ = ['PermissionsBoundaryAttachmentArgs', 'PermissionsBoundaryAttachment']

@pulumi.input_type
class PermissionsBoundaryAttachmentArgs:
    def __init__(__self__, *,
                 instance_arn: pulumi.Input[str],
                 permission_set_arn: pulumi.Input[str],
                 permissions_boundary: pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']):
        """
        The set of arguments for constructing a PermissionsBoundaryAttachment resource.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        :param pulumi.Input[str] permission_set_arn: The Amazon Resource Name (ARN) of the Permission Set.
        :param pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs'] permissions_boundary: The permissions boundary policy. See below.
        """
        pulumi.set(__self__, "instance_arn", instance_arn)
        pulumi.set(__self__, "permission_set_arn", permission_set_arn)
        pulumi.set(__self__, "permissions_boundary", permissions_boundary)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter(name="permissionSetArn")
    def permission_set_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the Permission Set.
        """
        return pulumi.get(self, "permission_set_arn")

    @permission_set_arn.setter
    def permission_set_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "permission_set_arn", value)

    @property
    @pulumi.getter(name="permissionsBoundary")
    def permissions_boundary(self) -> pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']:
        """
        The permissions boundary policy. See below.
        """
        return pulumi.get(self, "permissions_boundary")

    @permissions_boundary.setter
    def permissions_boundary(self, value: pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']):
        pulumi.set(self, "permissions_boundary", value)


@pulumi.input_type
class _PermissionsBoundaryAttachmentState:
    def __init__(__self__, *,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 permission_set_arn: Optional[pulumi.Input[str]] = None,
                 permissions_boundary: Optional[pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']] = None):
        """
        Input properties used for looking up and filtering PermissionsBoundaryAttachment resources.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        :param pulumi.Input[str] permission_set_arn: The Amazon Resource Name (ARN) of the Permission Set.
        :param pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs'] permissions_boundary: The permissions boundary policy. See below.
        """
        if instance_arn is not None:
            pulumi.set(__self__, "instance_arn", instance_arn)
        if permission_set_arn is not None:
            pulumi.set(__self__, "permission_set_arn", permission_set_arn)
        if permissions_boundary is not None:
            pulumi.set(__self__, "permissions_boundary", permissions_boundary)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        """
        return pulumi.get(self, "instance_arn")

    @instance_arn.setter
    def instance_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_arn", value)

    @property
    @pulumi.getter(name="permissionSetArn")
    def permission_set_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Permission Set.
        """
        return pulumi.get(self, "permission_set_arn")

    @permission_set_arn.setter
    def permission_set_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "permission_set_arn", value)

    @property
    @pulumi.getter(name="permissionsBoundary")
    def permissions_boundary(self) -> Optional[pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']]:
        """
        The permissions boundary policy. See below.
        """
        return pulumi.get(self, "permissions_boundary")

    @permissions_boundary.setter
    def permissions_boundary(self, value: Optional[pulumi.Input['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']]):
        pulumi.set(self, "permissions_boundary", value)


class PermissionsBoundaryAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 permission_set_arn: Optional[pulumi.Input[str]] = None,
                 permissions_boundary: Optional[pulumi.Input[pulumi.InputType['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']]] = None,
                 __props__=None):
        """
        Attaches a permissions boundary policy to a Single Sign-On (SSO) Permission Set resource.

        > **NOTE:** A permission set can have at most one permissions boundary attached; using more than one `ssoadmin.PermissionsBoundaryAttachment` references the same permission set will show a permanent difference.

        ## Example Usage

        ### Attaching an AWS-managed policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ssoadmin.PermissionsBoundaryAttachment("example",
            instance_arn=example_aws_ssoadmin_permission_set["instanceArn"],
            permission_set_arn=example_aws_ssoadmin_permission_set["arn"],
            permissions_boundary=aws.ssoadmin.PermissionsBoundaryAttachmentPermissionsBoundaryArgs(
                managed_policy_arn="arn:aws:iam::aws:policy/ReadOnlyAccess",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SSO Admin Permissions Boundary Attachments using the `permission_set_arn` and `instance_arn`, separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:ssoadmin/permissionsBoundaryAttachment:PermissionsBoundaryAttachment example arn:aws:sso:::permissionSet/ssoins-2938j0x8920sbj72/ps-80383020jr9302rk,arn:aws:sso:::instance/ssoins-2938j0x8920sbj72
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        :param pulumi.Input[str] permission_set_arn: The Amazon Resource Name (ARN) of the Permission Set.
        :param pulumi.Input[pulumi.InputType['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']] permissions_boundary: The permissions boundary policy. See below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PermissionsBoundaryAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a permissions boundary policy to a Single Sign-On (SSO) Permission Set resource.

        > **NOTE:** A permission set can have at most one permissions boundary attached; using more than one `ssoadmin.PermissionsBoundaryAttachment` references the same permission set will show a permanent difference.

        ## Example Usage

        ### Attaching an AWS-managed policy

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ssoadmin.PermissionsBoundaryAttachment("example",
            instance_arn=example_aws_ssoadmin_permission_set["instanceArn"],
            permission_set_arn=example_aws_ssoadmin_permission_set["arn"],
            permissions_boundary=aws.ssoadmin.PermissionsBoundaryAttachmentPermissionsBoundaryArgs(
                managed_policy_arn="arn:aws:iam::aws:policy/ReadOnlyAccess",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import SSO Admin Permissions Boundary Attachments using the `permission_set_arn` and `instance_arn`, separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:ssoadmin/permissionsBoundaryAttachment:PermissionsBoundaryAttachment example arn:aws:sso:::permissionSet/ssoins-2938j0x8920sbj72/ps-80383020jr9302rk,arn:aws:sso:::instance/ssoins-2938j0x8920sbj72
        ```

        :param str resource_name: The name of the resource.
        :param PermissionsBoundaryAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PermissionsBoundaryAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_arn: Optional[pulumi.Input[str]] = None,
                 permission_set_arn: Optional[pulumi.Input[str]] = None,
                 permissions_boundary: Optional[pulumi.Input[pulumi.InputType['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PermissionsBoundaryAttachmentArgs.__new__(PermissionsBoundaryAttachmentArgs)

            if instance_arn is None and not opts.urn:
                raise TypeError("Missing required property 'instance_arn'")
            __props__.__dict__["instance_arn"] = instance_arn
            if permission_set_arn is None and not opts.urn:
                raise TypeError("Missing required property 'permission_set_arn'")
            __props__.__dict__["permission_set_arn"] = permission_set_arn
            if permissions_boundary is None and not opts.urn:
                raise TypeError("Missing required property 'permissions_boundary'")
            __props__.__dict__["permissions_boundary"] = permissions_boundary
        super(PermissionsBoundaryAttachment, __self__).__init__(
            'aws:ssoadmin/permissionsBoundaryAttachment:PermissionsBoundaryAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_arn: Optional[pulumi.Input[str]] = None,
            permission_set_arn: Optional[pulumi.Input[str]] = None,
            permissions_boundary: Optional[pulumi.Input[pulumi.InputType['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']]] = None) -> 'PermissionsBoundaryAttachment':
        """
        Get an existing PermissionsBoundaryAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_arn: The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        :param pulumi.Input[str] permission_set_arn: The Amazon Resource Name (ARN) of the Permission Set.
        :param pulumi.Input[pulumi.InputType['PermissionsBoundaryAttachmentPermissionsBoundaryArgs']] permissions_boundary: The permissions boundary policy. See below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PermissionsBoundaryAttachmentState.__new__(_PermissionsBoundaryAttachmentState)

        __props__.__dict__["instance_arn"] = instance_arn
        __props__.__dict__["permission_set_arn"] = permission_set_arn
        __props__.__dict__["permissions_boundary"] = permissions_boundary
        return PermissionsBoundaryAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceArn")
    def instance_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the SSO Instance under which the operation will be executed.
        """
        return pulumi.get(self, "instance_arn")

    @property
    @pulumi.getter(name="permissionSetArn")
    def permission_set_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Permission Set.
        """
        return pulumi.get(self, "permission_set_arn")

    @property
    @pulumi.getter(name="permissionsBoundary")
    def permissions_boundary(self) -> pulumi.Output['outputs.PermissionsBoundaryAttachmentPermissionsBoundary']:
        """
        The permissions boundary policy. See below.
        """
        return pulumi.get(self, "permissions_boundary")

