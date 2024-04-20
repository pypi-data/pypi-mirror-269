# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GroupMembershipArgs', 'GroupMembership']

@pulumi.input_type
class GroupMembershipArgs:
    def __init__(__self__, *,
                 group: pulumi.Input[str],
                 users: pulumi.Input[Sequence[pulumi.Input[str]]],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a GroupMembership resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: A list of IAM User names to associate with the Group
        :param pulumi.Input[str] name: The name to identify the Group Membership
        """
        pulumi.set(__self__, "group", group)
        pulumi.set(__self__, "users", users)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def group(self) -> pulumi.Input[str]:
        """
        The IAM Group name to attach the list of `users` to
        """
        return pulumi.get(self, "group")

    @group.setter
    def group(self, value: pulumi.Input[str]):
        pulumi.set(self, "group", value)

    @property
    @pulumi.getter
    def users(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of IAM User names to associate with the Group
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "users", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name to identify the Group Membership
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _GroupMembershipState:
    def __init__(__self__, *,
                 group: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering GroupMembership resources.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: A list of IAM User names to associate with the Group
        """
        if group is not None:
            pulumi.set(__self__, "group", group)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def group(self) -> Optional[pulumi.Input[str]]:
        """
        The IAM Group name to attach the list of `users` to
        """
        return pulumi.get(self, "group")

    @group.setter
    def group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name to identify the Group Membership
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IAM User names to associate with the Group
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users", value)


class GroupMembership(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        > **WARNING:** Multiple iam.GroupMembership resources with the same group name will produce inconsistent behavior!

        Provides a top level resource to manage IAM Group membership for IAM Users. For
        more information on managing IAM Groups or IAM Users, see IAM Groups or
        IAM Users

        > **Note:** `iam.GroupMembership` will conflict with itself if used more than once with the same group. To non-exclusively manage the users in a group, see the
        `iam.UserGroupMembership` resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        group = aws.iam.Group("group", name="test-group")
        user_one = aws.iam.User("user_one", name="test-user")
        user_two = aws.iam.User("user_two", name="test-user-two")
        team = aws.iam.GroupMembership("team",
            name="tf-testing-group-membership",
            users=[
                user_one.name,
                user_two.name,
            ],
            group=group.name)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: A list of IAM User names to associate with the Group
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GroupMembershipArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **WARNING:** Multiple iam.GroupMembership resources with the same group name will produce inconsistent behavior!

        Provides a top level resource to manage IAM Group membership for IAM Users. For
        more information on managing IAM Groups or IAM Users, see IAM Groups or
        IAM Users

        > **Note:** `iam.GroupMembership` will conflict with itself if used more than once with the same group. To non-exclusively manage the users in a group, see the
        `iam.UserGroupMembership` resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        group = aws.iam.Group("group", name="test-group")
        user_one = aws.iam.User("user_one", name="test-user")
        user_two = aws.iam.User("user_two", name="test-user-two")
        team = aws.iam.GroupMembership("team",
            name="tf-testing-group-membership",
            users=[
                user_one.name,
                user_two.name,
            ],
            group=group.name)
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param GroupMembershipArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupMembershipArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupMembershipArgs.__new__(GroupMembershipArgs)

            if group is None and not opts.urn:
                raise TypeError("Missing required property 'group'")
            __props__.__dict__["group"] = group
            __props__.__dict__["name"] = name
            if users is None and not opts.urn:
                raise TypeError("Missing required property 'users'")
            __props__.__dict__["users"] = users
        super(GroupMembership, __self__).__init__(
            'aws:iam/groupMembership:GroupMembership',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            group: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'GroupMembership':
        """
        Get an existing GroupMembership resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: A list of IAM User names to associate with the Group
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupMembershipState.__new__(_GroupMembershipState)

        __props__.__dict__["group"] = group
        __props__.__dict__["name"] = name
        __props__.__dict__["users"] = users
        return GroupMembership(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def group(self) -> pulumi.Output[str]:
        """
        The IAM Group name to attach the list of `users` to
        """
        return pulumi.get(self, "group")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name to identify the Group Membership
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def users(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of IAM User names to associate with the Group
        """
        return pulumi.get(self, "users")

