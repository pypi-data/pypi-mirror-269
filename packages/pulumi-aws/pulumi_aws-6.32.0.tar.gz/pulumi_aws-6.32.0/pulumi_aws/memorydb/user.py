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

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 access_string: pulumi.Input[str],
                 authentication_mode: pulumi.Input['UserAuthenticationModeArgs'],
                 user_name: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] access_string: The access permissions string used for this user.
        :param pulumi.Input['UserAuthenticationModeArgs'] authentication_mode: Denotes the user's authentication properties. Detailed below.
        :param pulumi.Input[str] user_name: Name of the MemoryDB user. Up to 40 characters.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "access_string", access_string)
        pulumi.set(__self__, "authentication_mode", authentication_mode)
        pulumi.set(__self__, "user_name", user_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="accessString")
    def access_string(self) -> pulumi.Input[str]:
        """
        The access permissions string used for this user.
        """
        return pulumi.get(self, "access_string")

    @access_string.setter
    def access_string(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_string", value)

    @property
    @pulumi.getter(name="authenticationMode")
    def authentication_mode(self) -> pulumi.Input['UserAuthenticationModeArgs']:
        """
        Denotes the user's authentication properties. Detailed below.
        """
        return pulumi.get(self, "authentication_mode")

    @authentication_mode.setter
    def authentication_mode(self, value: pulumi.Input['UserAuthenticationModeArgs']):
        pulumi.set(self, "authentication_mode", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Input[str]:
        """
        Name of the MemoryDB user. Up to 40 characters.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 access_string: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 authentication_mode: Optional[pulumi.Input['UserAuthenticationModeArgs']] = None,
                 minimum_engine_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[str] access_string: The access permissions string used for this user.
        :param pulumi.Input[str] arn: The ARN of the user.
        :param pulumi.Input['UserAuthenticationModeArgs'] authentication_mode: Denotes the user's authentication properties. Detailed below.
        :param pulumi.Input[str] minimum_engine_version: The minimum engine version supported for the user.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_name: Name of the MemoryDB user. Up to 40 characters.
               
               The following arguments are optional:
        """
        if access_string is not None:
            pulumi.set(__self__, "access_string", access_string)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if authentication_mode is not None:
            pulumi.set(__self__, "authentication_mode", authentication_mode)
        if minimum_engine_version is not None:
            pulumi.set(__self__, "minimum_engine_version", minimum_engine_version)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="accessString")
    def access_string(self) -> Optional[pulumi.Input[str]]:
        """
        The access permissions string used for this user.
        """
        return pulumi.get(self, "access_string")

    @access_string.setter
    def access_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_string", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the user.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="authenticationMode")
    def authentication_mode(self) -> Optional[pulumi.Input['UserAuthenticationModeArgs']]:
        """
        Denotes the user's authentication properties. Detailed below.
        """
        return pulumi.get(self, "authentication_mode")

    @authentication_mode.setter
    def authentication_mode(self, value: Optional[pulumi.Input['UserAuthenticationModeArgs']]):
        pulumi.set(self, "authentication_mode", value)

    @property
    @pulumi.getter(name="minimumEngineVersion")
    def minimum_engine_version(self) -> Optional[pulumi.Input[str]]:
        """
        The minimum engine version supported for the user.
        """
        return pulumi.get(self, "minimum_engine_version")

    @minimum_engine_version.setter
    def minimum_engine_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "minimum_engine_version", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the MemoryDB user. Up to 40 characters.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_string: Optional[pulumi.Input[str]] = None,
                 authentication_mode: Optional[pulumi.Input[pulumi.InputType['UserAuthenticationModeArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a MemoryDB User.

        More information about users and ACL-s can be found in the [MemoryDB User Guide](https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html).

        > **Note:** All arguments including the username and passwords will be stored in the raw state as plain-text.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_random as random

        example = random.index.Password("example", length=16)
        example_user = aws.memorydb.User("example",
            user_name="my-user",
            access_string="on ~* &* +@all",
            authentication_mode=aws.memorydb.UserAuthenticationModeArgs(
                type="password",
                passwords=[example["result"]],
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import a user using the `user_name`. For example:

        ```sh
        $ pulumi import aws:memorydb/user:User example my-user
        ```
        The `passwords` are not available for imported resources, as this information cannot be read back from the MemoryDB API.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_string: The access permissions string used for this user.
        :param pulumi.Input[pulumi.InputType['UserAuthenticationModeArgs']] authentication_mode: Denotes the user's authentication properties. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] user_name: Name of the MemoryDB user. Up to 40 characters.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a MemoryDB User.

        More information about users and ACL-s can be found in the [MemoryDB User Guide](https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html).

        > **Note:** All arguments including the username and passwords will be stored in the raw state as plain-text.
        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_random as random

        example = random.index.Password("example", length=16)
        example_user = aws.memorydb.User("example",
            user_name="my-user",
            access_string="on ~* &* +@all",
            authentication_mode=aws.memorydb.UserAuthenticationModeArgs(
                type="password",
                passwords=[example["result"]],
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import a user using the `user_name`. For example:

        ```sh
        $ pulumi import aws:memorydb/user:User example my-user
        ```
        The `passwords` are not available for imported resources, as this information cannot be read back from the MemoryDB API.

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_string: Optional[pulumi.Input[str]] = None,
                 authentication_mode: Optional[pulumi.Input[pulumi.InputType['UserAuthenticationModeArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            if access_string is None and not opts.urn:
                raise TypeError("Missing required property 'access_string'")
            __props__.__dict__["access_string"] = access_string
            if authentication_mode is None and not opts.urn:
                raise TypeError("Missing required property 'authentication_mode'")
            __props__.__dict__["authentication_mode"] = authentication_mode
            __props__.__dict__["tags"] = tags
            if user_name is None and not opts.urn:
                raise TypeError("Missing required property 'user_name'")
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["arn"] = None
            __props__.__dict__["minimum_engine_version"] = None
            __props__.__dict__["tags_all"] = None
        super(User, __self__).__init__(
            'aws:memorydb/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_string: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            authentication_mode: Optional[pulumi.Input[pulumi.InputType['UserAuthenticationModeArgs']]] = None,
            minimum_engine_version: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            user_name: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_string: The access permissions string used for this user.
        :param pulumi.Input[str] arn: The ARN of the user.
        :param pulumi.Input[pulumi.InputType['UserAuthenticationModeArgs']] authentication_mode: Denotes the user's authentication properties. Detailed below.
        :param pulumi.Input[str] minimum_engine_version: The minimum engine version supported for the user.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_name: Name of the MemoryDB user. Up to 40 characters.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["access_string"] = access_string
        __props__.__dict__["arn"] = arn
        __props__.__dict__["authentication_mode"] = authentication_mode
        __props__.__dict__["minimum_engine_version"] = minimum_engine_version
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["user_name"] = user_name
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessString")
    def access_string(self) -> pulumi.Output[str]:
        """
        The access permissions string used for this user.
        """
        return pulumi.get(self, "access_string")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the user.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authenticationMode")
    def authentication_mode(self) -> pulumi.Output['outputs.UserAuthenticationMode']:
        """
        Denotes the user's authentication properties. Detailed below.
        """
        return pulumi.get(self, "authentication_mode")

    @property
    @pulumi.getter(name="minimumEngineVersion")
    def minimum_engine_version(self) -> pulumi.Output[str]:
        """
        The minimum engine version supported for the user.
        """
        return pulumi.get(self, "minimum_engine_version")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        Name of the MemoryDB user. Up to 40 characters.

        The following arguments are optional:
        """
        return pulumi.get(self, "user_name")

