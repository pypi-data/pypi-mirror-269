# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EventSubscriptionArgs', 'EventSubscription']

@pulumi.input_type
class EventSubscriptionArgs:
    def __init__(__self__, *,
                 event_categories: pulumi.Input[Sequence[pulumi.Input[str]]],
                 sns_topic_arn: pulumi.Input[str],
                 source_type: pulumi.Input[str],
                 enabled: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a EventSubscription resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "event_categories", event_categories)
        pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)
        pulumi.set(__self__, "source_type", source_type)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if source_ids is not None:
            pulumi.set(__self__, "source_ids", source_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="eventCategories")
    def event_categories(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        """
        return pulumi.get(self, "event_categories")

    @event_categories.setter
    def event_categories(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "event_categories", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> pulumi.Input[str]:
        """
        SNS topic arn to send events on.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "sns_topic_arn", value)

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> pulumi.Input[str]:
        """
        Type of source for events. Valid values: `replication-instance` or `replication-task`
        """
        return pulumi.get(self, "source_type")

    @source_type.setter
    def source_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_type", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the event subscription should be enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of event subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="sourceIds")
    def source_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        """
        return pulumi.get(self, "source_ids")

    @source_ids.setter
    def source_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "source_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _EventSubscriptionState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering EventSubscription resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DMS Event Subscription.
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if event_categories is not None:
            pulumi.set(__self__, "event_categories", event_categories)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if sns_topic_arn is not None:
            pulumi.set(__self__, "sns_topic_arn", sns_topic_arn)
        if source_ids is not None:
            pulumi.set(__self__, "source_ids", source_ids)
        if source_type is not None:
            pulumi.set(__self__, "source_type", source_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the DMS Event Subscription.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the event subscription should be enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="eventCategories")
    def event_categories(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        """
        return pulumi.get(self, "event_categories")

    @event_categories.setter
    def event_categories(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "event_categories", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of event subscription.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        SNS topic arn to send events on.
        """
        return pulumi.get(self, "sns_topic_arn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sns_topic_arn", value)

    @property
    @pulumi.getter(name="sourceIds")
    def source_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        """
        return pulumi.get(self, "source_ids")

    @source_ids.setter
    def source_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "source_ids", value)

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of source for events. Valid values: `replication-instance` or `replication-task`
        """
        return pulumi.get(self, "source_type")

    @source_type.setter
    def source_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class EventSubscription(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a DMS (Data Migration Service) event subscription resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dms.EventSubscription("example",
            enabled=True,
            event_categories=[
                "creation",
                "failure",
            ],
            name="my-favorite-event-subscription",
            sns_topic_arn=example_aws_sns_topic["arn"],
            source_ids=[example_aws_dms_replication_task["replicationTaskId"]],
            source_type="replication-task",
            tags={
                "Name": "example",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import event subscriptions using the `name`. For example:

        ```sh
        $ pulumi import aws:dms/eventSubscription:EventSubscription test my-awesome-event-subscription
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventSubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DMS (Data Migration Service) event subscription resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dms.EventSubscription("example",
            enabled=True,
            event_categories=[
                "creation",
                "failure",
            ],
            name="my-favorite-event-subscription",
            sns_topic_arn=example_aws_sns_topic["arn"],
            source_ids=[example_aws_dms_replication_task["replicationTaskId"]],
            source_type="replication-task",
            tags={
                "Name": "example",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import event subscriptions using the `name`. For example:

        ```sh
        $ pulumi import aws:dms/eventSubscription:EventSubscription test my-awesome-event-subscription
        ```

        :param str resource_name: The name of the resource.
        :param EventSubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventSubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventSubscriptionArgs.__new__(EventSubscriptionArgs)

            __props__.__dict__["enabled"] = enabled
            if event_categories is None and not opts.urn:
                raise TypeError("Missing required property 'event_categories'")
            __props__.__dict__["event_categories"] = event_categories
            __props__.__dict__["name"] = name
            if sns_topic_arn is None and not opts.urn:
                raise TypeError("Missing required property 'sns_topic_arn'")
            __props__.__dict__["sns_topic_arn"] = sns_topic_arn
            __props__.__dict__["source_ids"] = source_ids
            if source_type is None and not opts.urn:
                raise TypeError("Missing required property 'source_type'")
            __props__.__dict__["source_type"] = source_type
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(EventSubscription, __self__).__init__(
            'aws:dms/eventSubscription:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            event_categories: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            sns_topic_arn: Optional[pulumi.Input[str]] = None,
            source_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            source_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'EventSubscription':
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DMS Event Subscription.
        :param pulumi.Input[bool] enabled: Whether the event subscription should be enabled.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_categories: List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        :param pulumi.Input[str] name: Name of event subscription.
        :param pulumi.Input[str] sns_topic_arn: SNS topic arn to send events on.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_ids: Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        :param pulumi.Input[str] source_type: Type of source for events. Valid values: `replication-instance` or `replication-task`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EventSubscriptionState.__new__(_EventSubscriptionState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["event_categories"] = event_categories
        __props__.__dict__["name"] = name
        __props__.__dict__["sns_topic_arn"] = sns_topic_arn
        __props__.__dict__["source_ids"] = source_ids
        __props__.__dict__["source_type"] = source_type
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the DMS Event Subscription.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the event subscription should be enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="eventCategories")
    def event_categories(self) -> pulumi.Output[Sequence[str]]:
        """
        List of event categories to listen for, see `DescribeEventCategories` for a canonical list.
        """
        return pulumi.get(self, "event_categories")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of event subscription.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="snsTopicArn")
    def sns_topic_arn(self) -> pulumi.Output[str]:
        """
        SNS topic arn to send events on.
        """
        return pulumi.get(self, "sns_topic_arn")

    @property
    @pulumi.getter(name="sourceIds")
    def source_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Ids of sources to listen to. If you don't specify a value, notifications are provided for all sources.
        """
        return pulumi.get(self, "source_ids")

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> pulumi.Output[str]:
        """
        Type of source for events. Valid values: `replication-instance` or `replication-task`
        """
        return pulumi.get(self, "source_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of resource tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

