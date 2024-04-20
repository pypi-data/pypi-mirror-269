# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ResolverQueryLogConfigArgs', 'ResolverQueryLogConfig']

@pulumi.input_type
class ResolverQueryLogConfigArgs:
    def __init__(__self__, *,
                 destination_arn: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ResolverQueryLogConfig resource.
        :param pulumi.Input[str] destination_arn: The ARN of the resource that you want Route 53 Resolver to send query logs.
               You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param pulumi.Input[str] name: The name of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "destination_arn", destination_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the resource that you want Route 53 Resolver to send query logs.
        You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        """
        return pulumi.get(self, "destination_arn")

    @destination_arn.setter
    def destination_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Route 53 Resolver query logging configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ResolverQueryLogConfigState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 destination_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 share_status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ResolverQueryLogConfig resources.
        :param pulumi.Input[str] arn: The ARN (Amazon Resource Name) of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[str] destination_arn: The ARN of the resource that you want Route 53 Resolver to send query logs.
               You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param pulumi.Input[str] name: The name of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[str] owner_id: The AWS account ID of the account that created the query logging configuration.
        :param pulumi.Input[str] share_status: An indication of whether the query logging configuration is shared with other AWS accounts, or was shared with the current account by another AWS account.
               Sharing is configured through AWS Resource Access Manager (AWS RAM).
               Values are `NOT_SHARED`, `SHARED_BY_ME` or `SHARED_WITH_ME`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if destination_arn is not None:
            pulumi.set(__self__, "destination_arn", destination_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if share_status is not None:
            pulumi.set(__self__, "share_status", share_status)
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
        The ARN (Amazon Resource Name) of the Route 53 Resolver query logging configuration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the resource that you want Route 53 Resolver to send query logs.
        You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        """
        return pulumi.get(self, "destination_arn")

    @destination_arn.setter
    def destination_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "destination_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Route 53 Resolver query logging configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account ID of the account that created the query logging configuration.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> Optional[pulumi.Input[str]]:
        """
        An indication of whether the query logging configuration is shared with other AWS accounts, or was shared with the current account by another AWS account.
        Sharing is configured through AWS Resource Access Manager (AWS RAM).
        Values are `NOT_SHARED`, `SHARED_BY_ME` or `SHARED_WITH_ME`
        """
        return pulumi.get(self, "share_status")

    @share_status.setter
    def share_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class ResolverQueryLogConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Route 53 Resolver query logging configuration resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.route53.ResolverQueryLogConfig("example",
            name="example",
            destination_arn=example_aws_s3_bucket["arn"],
            tags={
                "Environment": "Prod",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import  Route 53 Resolver query logging configurations using the Route 53 Resolver query logging configuration ID. For example:

        ```sh
        $ pulumi import aws:route53/resolverQueryLogConfig:ResolverQueryLogConfig example rqlc-92edc3b1838248bf
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] destination_arn: The ARN of the resource that you want Route 53 Resolver to send query logs.
               You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param pulumi.Input[str] name: The name of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResolverQueryLogConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Route 53 Resolver query logging configuration resource.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.route53.ResolverQueryLogConfig("example",
            name="example",
            destination_arn=example_aws_s3_bucket["arn"],
            tags={
                "Environment": "Prod",
            })
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import  Route 53 Resolver query logging configurations using the Route 53 Resolver query logging configuration ID. For example:

        ```sh
        $ pulumi import aws:route53/resolverQueryLogConfig:ResolverQueryLogConfig example rqlc-92edc3b1838248bf
        ```

        :param str resource_name: The name of the resource.
        :param ResolverQueryLogConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResolverQueryLogConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResolverQueryLogConfigArgs.__new__(ResolverQueryLogConfigArgs)

            if destination_arn is None and not opts.urn:
                raise TypeError("Missing required property 'destination_arn'")
            __props__.__dict__["destination_arn"] = destination_arn
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["share_status"] = None
            __props__.__dict__["tags_all"] = None
        super(ResolverQueryLogConfig, __self__).__init__(
            'aws:route53/resolverQueryLogConfig:ResolverQueryLogConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            destination_arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            share_status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'ResolverQueryLogConfig':
        """
        Get an existing ResolverQueryLogConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN (Amazon Resource Name) of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[str] destination_arn: The ARN of the resource that you want Route 53 Resolver to send query logs.
               You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param pulumi.Input[str] name: The name of the Route 53 Resolver query logging configuration.
        :param pulumi.Input[str] owner_id: The AWS account ID of the account that created the query logging configuration.
        :param pulumi.Input[str] share_status: An indication of whether the query logging configuration is shared with other AWS accounts, or was shared with the current account by another AWS account.
               Sharing is configured through AWS Resource Access Manager (AWS RAM).
               Values are `NOT_SHARED`, `SHARED_BY_ME` or `SHARED_WITH_ME`
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResolverQueryLogConfigState.__new__(_ResolverQueryLogConfigState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["destination_arn"] = destination_arn
        __props__.__dict__["name"] = name
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["share_status"] = share_status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return ResolverQueryLogConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN (Amazon Resource Name) of the Route 53 Resolver query logging configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the resource that you want Route 53 Resolver to send query logs.
        You can send query logs to an S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        """
        return pulumi.get(self, "destination_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Route 53 Resolver query logging configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The AWS account ID of the account that created the query logging configuration.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> pulumi.Output[str]:
        """
        An indication of whether the query logging configuration is shared with other AWS accounts, or was shared with the current account by another AWS account.
        Sharing is configured through AWS Resource Access Manager (AWS RAM).
        Values are `NOT_SHARED`, `SHARED_BY_ME` or `SHARED_WITH_ME`
        """
        return pulumi.get(self, "share_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

