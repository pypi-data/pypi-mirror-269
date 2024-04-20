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

__all__ = ['CustomPluginArgs', 'CustomPlugin']

@pulumi.input_type
class CustomPluginArgs:
    def __init__(__self__, *,
                 content_type: pulumi.Input[str],
                 location: pulumi.Input['CustomPluginLocationArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CustomPlugin resource.
        :param pulumi.Input[str] content_type: The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        :param pulumi.Input['CustomPluginLocationArgs'] location: Information about the location of a custom plugin. See below.
               
               The following arguments are optional:
        :param pulumi.Input[str] description: A summary description of the custom plugin.
        :param pulumi.Input[str] name: The name of the custom plugin..
        """
        pulumi.set(__self__, "content_type", content_type)
        pulumi.set(__self__, "location", location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Input[str]:
        """
        The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input['CustomPluginLocationArgs']:
        """
        Information about the location of a custom plugin. See below.

        The following arguments are optional:
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input['CustomPluginLocationArgs']):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A summary description of the custom plugin.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the custom plugin..
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _CustomPluginState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 latest_revision: Optional[pulumi.Input[int]] = None,
                 location: Optional[pulumi.Input['CustomPluginLocationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CustomPlugin resources.
        :param pulumi.Input[str] arn: the Amazon Resource Name (ARN) of the custom plugin.
        :param pulumi.Input[str] content_type: The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        :param pulumi.Input[str] description: A summary description of the custom plugin.
        :param pulumi.Input[int] latest_revision: an ID of the latest successfully created revision of the custom plugin.
        :param pulumi.Input['CustomPluginLocationArgs'] location: Information about the location of a custom plugin. See below.
               
               The following arguments are optional:
        :param pulumi.Input[str] name: The name of the custom plugin..
        :param pulumi.Input[str] state: the state of the custom plugin.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if latest_revision is not None:
            pulumi.set(__self__, "latest_revision", latest_revision)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        the Amazon Resource Name (ARN) of the custom plugin.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A summary description of the custom plugin.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> Optional[pulumi.Input[int]]:
        """
        an ID of the latest successfully created revision of the custom plugin.
        """
        return pulumi.get(self, "latest_revision")

    @latest_revision.setter
    def latest_revision(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "latest_revision", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input['CustomPluginLocationArgs']]:
        """
        Information about the location of a custom plugin. See below.

        The following arguments are optional:
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input['CustomPluginLocationArgs']]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the custom plugin..
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        the state of the custom plugin.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


class CustomPlugin(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[pulumi.InputType['CustomPluginLocationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Amazon MSK Connect Custom Plugin Resource.

        ## Example Usage

        ### Basic configuration

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example")
        example_bucket_objectv2 = aws.s3.BucketObjectv2("example",
            bucket=example.id,
            key="debezium.zip",
            source=pulumi.FileAsset("debezium.zip"))
        example_custom_plugin = aws.mskconnect.CustomPlugin("example",
            name="debezium-example",
            content_type="ZIP",
            location=aws.mskconnect.CustomPluginLocationArgs(
                s3=aws.mskconnect.CustomPluginLocationS3Args(
                    bucket_arn=example.arn,
                    file_key=example_bucket_objectv2.key,
                ),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import MSK Connect Custom Plugin using the plugin's `arn`. For example:

        ```sh
        $ pulumi import aws:mskconnect/customPlugin:CustomPlugin example 'arn:aws:kafkaconnect:eu-central-1:123456789012:custom-plugin/debezium-example/abcdefgh-1234-5678-9abc-defghijklmno-4'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content_type: The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        :param pulumi.Input[str] description: A summary description of the custom plugin.
        :param pulumi.Input[pulumi.InputType['CustomPluginLocationArgs']] location: Information about the location of a custom plugin. See below.
               
               The following arguments are optional:
        :param pulumi.Input[str] name: The name of the custom plugin..
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomPluginArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon MSK Connect Custom Plugin Resource.

        ## Example Usage

        ### Basic configuration

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example")
        example_bucket_objectv2 = aws.s3.BucketObjectv2("example",
            bucket=example.id,
            key="debezium.zip",
            source=pulumi.FileAsset("debezium.zip"))
        example_custom_plugin = aws.mskconnect.CustomPlugin("example",
            name="debezium-example",
            content_type="ZIP",
            location=aws.mskconnect.CustomPluginLocationArgs(
                s3=aws.mskconnect.CustomPluginLocationS3Args(
                    bucket_arn=example.arn,
                    file_key=example_bucket_objectv2.key,
                ),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import MSK Connect Custom Plugin using the plugin's `arn`. For example:

        ```sh
        $ pulumi import aws:mskconnect/customPlugin:CustomPlugin example 'arn:aws:kafkaconnect:eu-central-1:123456789012:custom-plugin/debezium-example/abcdefgh-1234-5678-9abc-defghijklmno-4'
        ```

        :param str resource_name: The name of the resource.
        :param CustomPluginArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomPluginArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[pulumi.InputType['CustomPluginLocationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomPluginArgs.__new__(CustomPluginArgs)

            if content_type is None and not opts.urn:
                raise TypeError("Missing required property 'content_type'")
            __props__.__dict__["content_type"] = content_type
            __props__.__dict__["description"] = description
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["arn"] = None
            __props__.__dict__["latest_revision"] = None
            __props__.__dict__["state"] = None
        super(CustomPlugin, __self__).__init__(
            'aws:mskconnect/customPlugin:CustomPlugin',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            latest_revision: Optional[pulumi.Input[int]] = None,
            location: Optional[pulumi.Input[pulumi.InputType['CustomPluginLocationArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None) -> 'CustomPlugin':
        """
        Get an existing CustomPlugin resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: the Amazon Resource Name (ARN) of the custom plugin.
        :param pulumi.Input[str] content_type: The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        :param pulumi.Input[str] description: A summary description of the custom plugin.
        :param pulumi.Input[int] latest_revision: an ID of the latest successfully created revision of the custom plugin.
        :param pulumi.Input[pulumi.InputType['CustomPluginLocationArgs']] location: Information about the location of a custom plugin. See below.
               
               The following arguments are optional:
        :param pulumi.Input[str] name: The name of the custom plugin..
        :param pulumi.Input[str] state: the state of the custom plugin.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CustomPluginState.__new__(_CustomPluginState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["description"] = description
        __props__.__dict__["latest_revision"] = latest_revision
        __props__.__dict__["location"] = location
        __props__.__dict__["name"] = name
        __props__.__dict__["state"] = state
        return CustomPlugin(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        the Amazon Resource Name (ARN) of the custom plugin.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[str]:
        """
        The type of the plugin file. Allowed values are `ZIP` and `JAR`.
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A summary description of the custom plugin.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> pulumi.Output[int]:
        """
        an ID of the latest successfully created revision of the custom plugin.
        """
        return pulumi.get(self, "latest_revision")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output['outputs.CustomPluginLocation']:
        """
        Information about the location of a custom plugin. See below.

        The following arguments are optional:
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the custom plugin..
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        the state of the custom plugin.
        """
        return pulumi.get(self, "state")

