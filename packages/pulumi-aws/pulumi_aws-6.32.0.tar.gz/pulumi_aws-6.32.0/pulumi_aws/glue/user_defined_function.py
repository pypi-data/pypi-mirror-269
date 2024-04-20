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

__all__ = ['UserDefinedFunctionArgs', 'UserDefinedFunction']

@pulumi.input_type
class UserDefinedFunctionArgs:
    def __init__(__self__, *,
                 class_name: pulumi.Input[str],
                 database_name: pulumi.Input[str],
                 owner_name: pulumi.Input[str],
                 owner_type: pulumi.Input[str],
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_uris: Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]] = None):
        """
        The set of arguments for constructing a UserDefinedFunction resource.
        :param pulumi.Input[str] class_name: The Java class that contains the function code.
        :param pulumi.Input[str] database_name: The name of the Database to create the Function.
        :param pulumi.Input[str] owner_name: The owner of the function.
        :param pulumi.Input[str] owner_type: The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        :param pulumi.Input[str] catalog_id: ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        :param pulumi.Input[str] name: The name of the function.
        :param pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]] resource_uris: The configuration block for Resource URIs. See resource uris below for more details.
        """
        pulumi.set(__self__, "class_name", class_name)
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "owner_name", owner_name)
        pulumi.set(__self__, "owner_type", owner_type)
        if catalog_id is not None:
            pulumi.set(__self__, "catalog_id", catalog_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_uris is not None:
            pulumi.set(__self__, "resource_uris", resource_uris)

    @property
    @pulumi.getter(name="className")
    def class_name(self) -> pulumi.Input[str]:
        """
        The Java class that contains the function code.
        """
        return pulumi.get(self, "class_name")

    @class_name.setter
    def class_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "class_name", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        The name of the Database to create the Function.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="ownerName")
    def owner_name(self) -> pulumi.Input[str]:
        """
        The owner of the function.
        """
        return pulumi.get(self, "owner_name")

    @owner_name.setter
    def owner_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "owner_name", value)

    @property
    @pulumi.getter(name="ownerType")
    def owner_type(self) -> pulumi.Input[str]:
        """
        The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        """
        return pulumi.get(self, "owner_type")

    @owner_type.setter
    def owner_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "owner_type", value)

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        """
        return pulumi.get(self, "catalog_id")

    @catalog_id.setter
    def catalog_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "catalog_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the function.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceUris")
    def resource_uris(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]]:
        """
        The configuration block for Resource URIs. See resource uris below for more details.
        """
        return pulumi.get(self, "resource_uris")

    @resource_uris.setter
    def resource_uris(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]]):
        pulumi.set(self, "resource_uris", value)


@pulumi.input_type
class _UserDefinedFunctionState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 class_name: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_name: Optional[pulumi.Input[str]] = None,
                 owner_type: Optional[pulumi.Input[str]] = None,
                 resource_uris: Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]] = None):
        """
        Input properties used for looking up and filtering UserDefinedFunction resources.
        :param pulumi.Input[str] arn: The ARN of the Glue User Defined Function.
        :param pulumi.Input[str] catalog_id: ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        :param pulumi.Input[str] class_name: The Java class that contains the function code.
        :param pulumi.Input[str] create_time: The time at which the function was created.
        :param pulumi.Input[str] database_name: The name of the Database to create the Function.
        :param pulumi.Input[str] name: The name of the function.
        :param pulumi.Input[str] owner_name: The owner of the function.
        :param pulumi.Input[str] owner_type: The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        :param pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]] resource_uris: The configuration block for Resource URIs. See resource uris below for more details.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if catalog_id is not None:
            pulumi.set(__self__, "catalog_id", catalog_id)
        if class_name is not None:
            pulumi.set(__self__, "class_name", class_name)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner_name is not None:
            pulumi.set(__self__, "owner_name", owner_name)
        if owner_type is not None:
            pulumi.set(__self__, "owner_type", owner_type)
        if resource_uris is not None:
            pulumi.set(__self__, "resource_uris", resource_uris)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the Glue User Defined Function.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        """
        return pulumi.get(self, "catalog_id")

    @catalog_id.setter
    def catalog_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "catalog_id", value)

    @property
    @pulumi.getter(name="className")
    def class_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Java class that contains the function code.
        """
        return pulumi.get(self, "class_name")

    @class_name.setter
    def class_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "class_name", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time at which the function was created.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Database to create the Function.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the function.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="ownerName")
    def owner_name(self) -> Optional[pulumi.Input[str]]:
        """
        The owner of the function.
        """
        return pulumi.get(self, "owner_name")

    @owner_name.setter
    def owner_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_name", value)

    @property
    @pulumi.getter(name="ownerType")
    def owner_type(self) -> Optional[pulumi.Input[str]]:
        """
        The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        """
        return pulumi.get(self, "owner_type")

    @owner_type.setter
    def owner_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_type", value)

    @property
    @pulumi.getter(name="resourceUris")
    def resource_uris(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]]:
        """
        The configuration block for Resource URIs. See resource uris below for more details.
        """
        return pulumi.get(self, "resource_uris")

    @resource_uris.setter
    def resource_uris(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserDefinedFunctionResourceUriArgs']]]]):
        pulumi.set(self, "resource_uris", value)


class UserDefinedFunction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 class_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_name: Optional[pulumi.Input[str]] = None,
                 owner_type: Optional[pulumi.Input[str]] = None,
                 resource_uris: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserDefinedFunctionResourceUriArgs']]]]] = None,
                 __props__=None):
        """
        Provides a Glue User Defined Function Resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.CatalogDatabase("example", name="my_database")
        example_user_defined_function = aws.glue.UserDefinedFunction("example",
            name="my_func",
            catalog_id=example.catalog_id,
            database_name=example.name,
            class_name="class",
            owner_name="owner",
            owner_type="GROUP",
            resource_uris=[aws.glue.UserDefinedFunctionResourceUriArgs(
                resource_type="ARCHIVE",
                uri="uri",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Glue User Defined Functions using the `catalog_id:database_name:function_name`. If you have not set a Catalog ID specify the AWS Account ID that the database is in. For example:

        ```sh
        $ pulumi import aws:glue/userDefinedFunction:UserDefinedFunction func 123456789012:my_database:my_func
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] catalog_id: ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        :param pulumi.Input[str] class_name: The Java class that contains the function code.
        :param pulumi.Input[str] database_name: The name of the Database to create the Function.
        :param pulumi.Input[str] name: The name of the function.
        :param pulumi.Input[str] owner_name: The owner of the function.
        :param pulumi.Input[str] owner_type: The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserDefinedFunctionResourceUriArgs']]]] resource_uris: The configuration block for Resource URIs. See resource uris below for more details.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserDefinedFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Glue User Defined Function Resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.glue.CatalogDatabase("example", name="my_database")
        example_user_defined_function = aws.glue.UserDefinedFunction("example",
            name="my_func",
            catalog_id=example.catalog_id,
            database_name=example.name,
            class_name="class",
            owner_name="owner",
            owner_type="GROUP",
            resource_uris=[aws.glue.UserDefinedFunctionResourceUriArgs(
                resource_type="ARCHIVE",
                uri="uri",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Glue User Defined Functions using the `catalog_id:database_name:function_name`. If you have not set a Catalog ID specify the AWS Account ID that the database is in. For example:

        ```sh
        $ pulumi import aws:glue/userDefinedFunction:UserDefinedFunction func 123456789012:my_database:my_func
        ```

        :param str resource_name: The name of the resource.
        :param UserDefinedFunctionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserDefinedFunctionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_id: Optional[pulumi.Input[str]] = None,
                 class_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_name: Optional[pulumi.Input[str]] = None,
                 owner_type: Optional[pulumi.Input[str]] = None,
                 resource_uris: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserDefinedFunctionResourceUriArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserDefinedFunctionArgs.__new__(UserDefinedFunctionArgs)

            __props__.__dict__["catalog_id"] = catalog_id
            if class_name is None and not opts.urn:
                raise TypeError("Missing required property 'class_name'")
            __props__.__dict__["class_name"] = class_name
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["name"] = name
            if owner_name is None and not opts.urn:
                raise TypeError("Missing required property 'owner_name'")
            __props__.__dict__["owner_name"] = owner_name
            if owner_type is None and not opts.urn:
                raise TypeError("Missing required property 'owner_type'")
            __props__.__dict__["owner_type"] = owner_type
            __props__.__dict__["resource_uris"] = resource_uris
            __props__.__dict__["arn"] = None
            __props__.__dict__["create_time"] = None
        super(UserDefinedFunction, __self__).__init__(
            'aws:glue/userDefinedFunction:UserDefinedFunction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            catalog_id: Optional[pulumi.Input[str]] = None,
            class_name: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            database_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner_name: Optional[pulumi.Input[str]] = None,
            owner_type: Optional[pulumi.Input[str]] = None,
            resource_uris: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserDefinedFunctionResourceUriArgs']]]]] = None) -> 'UserDefinedFunction':
        """
        Get an existing UserDefinedFunction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the Glue User Defined Function.
        :param pulumi.Input[str] catalog_id: ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        :param pulumi.Input[str] class_name: The Java class that contains the function code.
        :param pulumi.Input[str] create_time: The time at which the function was created.
        :param pulumi.Input[str] database_name: The name of the Database to create the Function.
        :param pulumi.Input[str] name: The name of the function.
        :param pulumi.Input[str] owner_name: The owner of the function.
        :param pulumi.Input[str] owner_type: The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserDefinedFunctionResourceUriArgs']]]] resource_uris: The configuration block for Resource URIs. See resource uris below for more details.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserDefinedFunctionState.__new__(_UserDefinedFunctionState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["catalog_id"] = catalog_id
        __props__.__dict__["class_name"] = class_name
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["database_name"] = database_name
        __props__.__dict__["name"] = name
        __props__.__dict__["owner_name"] = owner_name
        __props__.__dict__["owner_type"] = owner_type
        __props__.__dict__["resource_uris"] = resource_uris
        return UserDefinedFunction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Glue User Defined Function.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID of the Glue Catalog to create the function in. If omitted, this defaults to the AWS Account ID.
        """
        return pulumi.get(self, "catalog_id")

    @property
    @pulumi.getter(name="className")
    def class_name(self) -> pulumi.Output[str]:
        """
        The Java class that contains the function code.
        """
        return pulumi.get(self, "class_name")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time at which the function was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Output[str]:
        """
        The name of the Database to create the Function.
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the function.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerName")
    def owner_name(self) -> pulumi.Output[str]:
        """
        The owner of the function.
        """
        return pulumi.get(self, "owner_name")

    @property
    @pulumi.getter(name="ownerType")
    def owner_type(self) -> pulumi.Output[str]:
        """
        The owner type. can be one of `USER`, `ROLE`, and `GROUP`.
        """
        return pulumi.get(self, "owner_type")

    @property
    @pulumi.getter(name="resourceUris")
    def resource_uris(self) -> pulumi.Output[Optional[Sequence['outputs.UserDefinedFunctionResourceUri']]]:
        """
        The configuration block for Resource URIs. See resource uris below for more details.
        """
        return pulumi.get(self, "resource_uris")

