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

__all__ = ['RecordingConfigurationArgs', 'RecordingConfiguration']

@pulumi.input_type
class RecordingConfigurationArgs:
    def __init__(__self__, *,
                 destination_configuration: pulumi.Input['RecordingConfigurationDestinationConfigurationArgs'],
                 name: Optional[pulumi.Input[str]] = None,
                 recording_reconnect_window_seconds: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbnail_configuration: Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']] = None):
        """
        The set of arguments for constructing a RecordingConfiguration resource.
        :param pulumi.Input['RecordingConfigurationDestinationConfigurationArgs'] destination_configuration: Object containing destination configuration for where recorded video will be stored.
        :param pulumi.Input[str] name: Recording Configuration name.
        :param pulumi.Input[int] recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs'] thumbnail_configuration: Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        pulumi.set(__self__, "destination_configuration", destination_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recording_reconnect_window_seconds is not None:
            pulumi.set(__self__, "recording_reconnect_window_seconds", recording_reconnect_window_seconds)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if thumbnail_configuration is not None:
            pulumi.set(__self__, "thumbnail_configuration", thumbnail_configuration)

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> pulumi.Input['RecordingConfigurationDestinationConfigurationArgs']:
        """
        Object containing destination configuration for where recorded video will be stored.
        """
        return pulumi.get(self, "destination_configuration")

    @destination_configuration.setter
    def destination_configuration(self, value: pulumi.Input['RecordingConfigurationDestinationConfigurationArgs']):
        pulumi.set(self, "destination_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Recording Configuration name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="recordingReconnectWindowSeconds")
    def recording_reconnect_window_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        """
        return pulumi.get(self, "recording_reconnect_window_seconds")

    @recording_reconnect_window_seconds.setter
    def recording_reconnect_window_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "recording_reconnect_window_seconds", value)

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
    @pulumi.getter(name="thumbnailConfiguration")
    def thumbnail_configuration(self) -> Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']]:
        """
        Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        return pulumi.get(self, "thumbnail_configuration")

    @thumbnail_configuration.setter
    def thumbnail_configuration(self, value: Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']]):
        pulumi.set(self, "thumbnail_configuration", value)


@pulumi.input_type
class _RecordingConfigurationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 destination_configuration: Optional[pulumi.Input['RecordingConfigurationDestinationConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_reconnect_window_seconds: Optional[pulumi.Input[int]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbnail_configuration: Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']] = None):
        """
        Input properties used for looking up and filtering RecordingConfiguration resources.
        :param pulumi.Input[str] arn: ARN of the Recording Configuration.
        :param pulumi.Input['RecordingConfigurationDestinationConfigurationArgs'] destination_configuration: Object containing destination configuration for where recorded video will be stored.
        :param pulumi.Input[str] name: Recording Configuration name.
        :param pulumi.Input[int] recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        :param pulumi.Input[str] state: The current state of the Recording Configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs'] thumbnail_configuration: Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if destination_configuration is not None:
            pulumi.set(__self__, "destination_configuration", destination_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recording_reconnect_window_seconds is not None:
            pulumi.set(__self__, "recording_reconnect_window_seconds", recording_reconnect_window_seconds)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if thumbnail_configuration is not None:
            pulumi.set(__self__, "thumbnail_configuration", thumbnail_configuration)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Recording Configuration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> Optional[pulumi.Input['RecordingConfigurationDestinationConfigurationArgs']]:
        """
        Object containing destination configuration for where recorded video will be stored.
        """
        return pulumi.get(self, "destination_configuration")

    @destination_configuration.setter
    def destination_configuration(self, value: Optional[pulumi.Input['RecordingConfigurationDestinationConfigurationArgs']]):
        pulumi.set(self, "destination_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Recording Configuration name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="recordingReconnectWindowSeconds")
    def recording_reconnect_window_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        """
        return pulumi.get(self, "recording_reconnect_window_seconds")

    @recording_reconnect_window_seconds.setter
    def recording_reconnect_window_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "recording_reconnect_window_seconds", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the Recording Configuration.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

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
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="thumbnailConfiguration")
    def thumbnail_configuration(self) -> Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']]:
        """
        Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        return pulumi.get(self, "thumbnail_configuration")

    @thumbnail_configuration.setter
    def thumbnail_configuration(self, value: Optional[pulumi.Input['RecordingConfigurationThumbnailConfigurationArgs']]):
        pulumi.set(self, "thumbnail_configuration", value)


class RecordingConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationDestinationConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_reconnect_window_seconds: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbnail_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationThumbnailConfigurationArgs']]] = None,
                 __props__=None):
        """
        Resource for managing an AWS IVS (Interactive Video) Recording Configuration.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.RecordingConfiguration("example",
            name="recording_configuration-1",
            destination_configuration=aws.ivs.RecordingConfigurationDestinationConfigurationArgs(
                s3=aws.ivs.RecordingConfigurationDestinationConfigurationS3Args(
                    bucket_name="ivs-stream-archive",
                ),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import IVS (Interactive Video) Recording Configuration using the ARN. For example:

        ```sh
        $ pulumi import aws:ivs/recordingConfiguration:RecordingConfiguration example arn:aws:ivs:us-west-2:326937407773:recording-configuration/KAk1sHBl2L47
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RecordingConfigurationDestinationConfigurationArgs']] destination_configuration: Object containing destination configuration for where recorded video will be stored.
        :param pulumi.Input[str] name: Recording Configuration name.
        :param pulumi.Input[int] recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['RecordingConfigurationThumbnailConfigurationArgs']] thumbnail_configuration: Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RecordingConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS IVS (Interactive Video) Recording Configuration.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.RecordingConfiguration("example",
            name="recording_configuration-1",
            destination_configuration=aws.ivs.RecordingConfigurationDestinationConfigurationArgs(
                s3=aws.ivs.RecordingConfigurationDestinationConfigurationS3Args(
                    bucket_name="ivs-stream-archive",
                ),
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import IVS (Interactive Video) Recording Configuration using the ARN. For example:

        ```sh
        $ pulumi import aws:ivs/recordingConfiguration:RecordingConfiguration example arn:aws:ivs:us-west-2:326937407773:recording-configuration/KAk1sHBl2L47
        ```

        :param str resource_name: The name of the resource.
        :param RecordingConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RecordingConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationDestinationConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recording_reconnect_window_seconds: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbnail_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationThumbnailConfigurationArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RecordingConfigurationArgs.__new__(RecordingConfigurationArgs)

            if destination_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'destination_configuration'")
            __props__.__dict__["destination_configuration"] = destination_configuration
            __props__.__dict__["name"] = name
            __props__.__dict__["recording_reconnect_window_seconds"] = recording_reconnect_window_seconds
            __props__.__dict__["tags"] = tags
            __props__.__dict__["thumbnail_configuration"] = thumbnail_configuration
            __props__.__dict__["arn"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["tags_all"] = None
        super(RecordingConfiguration, __self__).__init__(
            'aws:ivs/recordingConfiguration:RecordingConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            destination_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationDestinationConfigurationArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            recording_reconnect_window_seconds: Optional[pulumi.Input[int]] = None,
            state: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            thumbnail_configuration: Optional[pulumi.Input[pulumi.InputType['RecordingConfigurationThumbnailConfigurationArgs']]] = None) -> 'RecordingConfiguration':
        """
        Get an existing RecordingConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Recording Configuration.
        :param pulumi.Input[pulumi.InputType['RecordingConfigurationDestinationConfigurationArgs']] destination_configuration: Object containing destination configuration for where recorded video will be stored.
        :param pulumi.Input[str] name: Recording Configuration name.
        :param pulumi.Input[int] recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        :param pulumi.Input[str] state: The current state of the Recording Configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[pulumi.InputType['RecordingConfigurationThumbnailConfigurationArgs']] thumbnail_configuration: Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RecordingConfigurationState.__new__(_RecordingConfigurationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["destination_configuration"] = destination_configuration
        __props__.__dict__["name"] = name
        __props__.__dict__["recording_reconnect_window_seconds"] = recording_reconnect_window_seconds
        __props__.__dict__["state"] = state
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["thumbnail_configuration"] = thumbnail_configuration
        return RecordingConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Recording Configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> pulumi.Output['outputs.RecordingConfigurationDestinationConfiguration']:
        """
        Object containing destination configuration for where recorded video will be stored.
        """
        return pulumi.get(self, "destination_configuration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Recording Configuration name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="recordingReconnectWindowSeconds")
    def recording_reconnect_window_seconds(self) -> pulumi.Output[int]:
        """
        If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.
        """
        return pulumi.get(self, "recording_reconnect_window_seconds")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the Recording Configuration.
        """
        return pulumi.get(self, "state")

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
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="thumbnailConfiguration")
    def thumbnail_configuration(self) -> pulumi.Output['outputs.RecordingConfigurationThumbnailConfiguration']:
        """
        Object containing information to enable/disable the recording of thumbnails for a live session and modify the interval at which thumbnails are generated for the live session.
        """
        return pulumi.get(self, "thumbnail_configuration")

