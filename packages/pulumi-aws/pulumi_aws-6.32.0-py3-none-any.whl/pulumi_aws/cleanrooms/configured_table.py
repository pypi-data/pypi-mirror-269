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

__all__ = ['ConfiguredTableArgs', 'ConfiguredTable']

@pulumi.input_type
class ConfiguredTableArgs:
    def __init__(__self__, *,
                 allowed_columns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 analysis_method: pulumi.Input[str],
                 table_reference: pulumi.Input['ConfiguredTableTableReferenceArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ConfiguredTable resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_columns: The columns of the references table which will be included in the configured table.
        :param pulumi.Input[str] analysis_method: The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        :param pulumi.Input['ConfiguredTableTableReferenceArgs'] table_reference: A reference to the AWS Glue table which will be used to create the configured table.
               * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
               * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        :param pulumi.Input[str] description: A description for the configured table.
        :param pulumi.Input[str] name: The name of the configured table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key value pairs which tag the configured table.
        """
        pulumi.set(__self__, "allowed_columns", allowed_columns)
        pulumi.set(__self__, "analysis_method", analysis_method)
        pulumi.set(__self__, "table_reference", table_reference)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowedColumns")
    def allowed_columns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The columns of the references table which will be included in the configured table.
        """
        return pulumi.get(self, "allowed_columns")

    @allowed_columns.setter
    def allowed_columns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_columns", value)

    @property
    @pulumi.getter(name="analysisMethod")
    def analysis_method(self) -> pulumi.Input[str]:
        """
        The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        """
        return pulumi.get(self, "analysis_method")

    @analysis_method.setter
    def analysis_method(self, value: pulumi.Input[str]):
        pulumi.set(self, "analysis_method", value)

    @property
    @pulumi.getter(name="tableReference")
    def table_reference(self) -> pulumi.Input['ConfiguredTableTableReferenceArgs']:
        """
        A reference to the AWS Glue table which will be used to create the configured table.
        * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
        * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        """
        return pulumi.get(self, "table_reference")

    @table_reference.setter
    def table_reference(self, value: pulumi.Input['ConfiguredTableTableReferenceArgs']):
        pulumi.set(self, "table_reference", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the configured table.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configured table.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key value pairs which tag the configured table.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ConfiguredTableState:
    def __init__(__self__, *,
                 allowed_columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 analysis_method: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 table_reference: Optional[pulumi.Input['ConfiguredTableTableReferenceArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 update_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ConfiguredTable resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_columns: The columns of the references table which will be included in the configured table.
        :param pulumi.Input[str] analysis_method: The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        :param pulumi.Input[str] arn: The ARN of the configured table.
        :param pulumi.Input[str] create_time: The date and time the configured table was created.
        :param pulumi.Input[str] description: A description for the configured table.
        :param pulumi.Input[str] name: The name of the configured table.
        :param pulumi.Input['ConfiguredTableTableReferenceArgs'] table_reference: A reference to the AWS Glue table which will be used to create the configured table.
               * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
               * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key value pairs which tag the configured table.
        :param pulumi.Input[str] update_time: The date and time the configured table was last updated.
        """
        if allowed_columns is not None:
            pulumi.set(__self__, "allowed_columns", allowed_columns)
        if analysis_method is not None:
            pulumi.set(__self__, "analysis_method", analysis_method)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if table_reference is not None:
            pulumi.set(__self__, "table_reference", table_reference)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if update_time is not None:
            pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter(name="allowedColumns")
    def allowed_columns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The columns of the references table which will be included in the configured table.
        """
        return pulumi.get(self, "allowed_columns")

    @allowed_columns.setter
    def allowed_columns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_columns", value)

    @property
    @pulumi.getter(name="analysisMethod")
    def analysis_method(self) -> Optional[pulumi.Input[str]]:
        """
        The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        """
        return pulumi.get(self, "analysis_method")

    @analysis_method.setter
    def analysis_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "analysis_method", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the configured table.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time the configured table was created.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description for the configured table.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the configured table.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="tableReference")
    def table_reference(self) -> Optional[pulumi.Input['ConfiguredTableTableReferenceArgs']]:
        """
        A reference to the AWS Glue table which will be used to create the configured table.
        * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
        * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        """
        return pulumi.get(self, "table_reference")

    @table_reference.setter
    def table_reference(self, value: Optional[pulumi.Input['ConfiguredTableTableReferenceArgs']]):
        pulumi.set(self, "table_reference", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key value pairs which tag the configured table.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time the configured table was last updated.
        """
        return pulumi.get(self, "update_time")

    @update_time.setter
    def update_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_time", value)


class ConfiguredTable(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 analysis_method: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 table_reference: Optional[pulumi.Input[pulumi.InputType['ConfiguredTableTableReferenceArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a AWS Clean Rooms configured table. Configured tables are used to represent references to existing tables in the AWS Glue Data Catalog.

        ## Example Usage

        ### Configured table with tags

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test_configured_table = aws.cleanrooms.ConfiguredTable("test_configured_table",
            name="pulumi-example-table",
            description="I made this table with Pulumi!",
            analysis_method="DIRECT_QUERY",
            allowed_columns=[
                "column1",
                "column2",
                "column3",
            ],
            table_reference=aws.cleanrooms.ConfiguredTableTableReferenceArgs(
                database_name="example_database",
                table_name="example_table",
            ),
            tags={
                "Project": "Pulumi",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_cleanrooms_configured_table` using the `id`. For example:

        ```sh
        $ pulumi import aws:cleanrooms/configuredTable:ConfiguredTable table 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_columns: The columns of the references table which will be included in the configured table.
        :param pulumi.Input[str] analysis_method: The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        :param pulumi.Input[str] description: A description for the configured table.
        :param pulumi.Input[str] name: The name of the configured table.
        :param pulumi.Input[pulumi.InputType['ConfiguredTableTableReferenceArgs']] table_reference: A reference to the AWS Glue table which will be used to create the configured table.
               * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
               * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key value pairs which tag the configured table.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfiguredTableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a AWS Clean Rooms configured table. Configured tables are used to represent references to existing tables in the AWS Glue Data Catalog.

        ## Example Usage

        ### Configured table with tags

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test_configured_table = aws.cleanrooms.ConfiguredTable("test_configured_table",
            name="pulumi-example-table",
            description="I made this table with Pulumi!",
            analysis_method="DIRECT_QUERY",
            allowed_columns=[
                "column1",
                "column2",
                "column3",
            ],
            table_reference=aws.cleanrooms.ConfiguredTableTableReferenceArgs(
                database_name="example_database",
                table_name="example_table",
            ),
            tags={
                "Project": "Pulumi",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_cleanrooms_configured_table` using the `id`. For example:

        ```sh
        $ pulumi import aws:cleanrooms/configuredTable:ConfiguredTable table 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param ConfiguredTableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfiguredTableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowed_columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 analysis_method: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 table_reference: Optional[pulumi.Input[pulumi.InputType['ConfiguredTableTableReferenceArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConfiguredTableArgs.__new__(ConfiguredTableArgs)

            if allowed_columns is None and not opts.urn:
                raise TypeError("Missing required property 'allowed_columns'")
            __props__.__dict__["allowed_columns"] = allowed_columns
            if analysis_method is None and not opts.urn:
                raise TypeError("Missing required property 'analysis_method'")
            __props__.__dict__["analysis_method"] = analysis_method
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if table_reference is None and not opts.urn:
                raise TypeError("Missing required property 'table_reference'")
            __props__.__dict__["table_reference"] = table_reference
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["update_time"] = None
        super(ConfiguredTable, __self__).__init__(
            'aws:cleanrooms/configuredTable:ConfiguredTable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allowed_columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            analysis_method: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            table_reference: Optional[pulumi.Input[pulumi.InputType['ConfiguredTableTableReferenceArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'ConfiguredTable':
        """
        Get an existing ConfiguredTable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_columns: The columns of the references table which will be included in the configured table.
        :param pulumi.Input[str] analysis_method: The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        :param pulumi.Input[str] arn: The ARN of the configured table.
        :param pulumi.Input[str] create_time: The date and time the configured table was created.
        :param pulumi.Input[str] description: A description for the configured table.
        :param pulumi.Input[str] name: The name of the configured table.
        :param pulumi.Input[pulumi.InputType['ConfiguredTableTableReferenceArgs']] table_reference: A reference to the AWS Glue table which will be used to create the configured table.
               * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
               * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key value pairs which tag the configured table.
        :param pulumi.Input[str] update_time: The date and time the configured table was last updated.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConfiguredTableState.__new__(_ConfiguredTableState)

        __props__.__dict__["allowed_columns"] = allowed_columns
        __props__.__dict__["analysis_method"] = analysis_method
        __props__.__dict__["arn"] = arn
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["table_reference"] = table_reference
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["update_time"] = update_time
        return ConfiguredTable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowedColumns")
    def allowed_columns(self) -> pulumi.Output[Sequence[str]]:
        """
        The columns of the references table which will be included in the configured table.
        """
        return pulumi.get(self, "allowed_columns")

    @property
    @pulumi.getter(name="analysisMethod")
    def analysis_method(self) -> pulumi.Output[str]:
        """
        The analysis method for the configured table. The only valid value is currently `DIRECT_QUERY`.
        """
        return pulumi.get(self, "analysis_method")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the configured table.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The date and time the configured table was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for the configured table.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the configured table.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="tableReference")
    def table_reference(self) -> pulumi.Output['outputs.ConfiguredTableTableReference']:
        """
        A reference to the AWS Glue table which will be used to create the configured table.
        * `table_reference.database_name` - (Required - Forces new resource) - The name of the AWS Glue database which contains the table.
        * `table_reference.table_name` - (Required - Forces new resource) - The name of the AWS Glue table which will be used to create the configured table.
        """
        return pulumi.get(self, "table_reference")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key value pairs which tag the configured table.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The date and time the configured table was last updated.
        """
        return pulumi.get(self, "update_time")

