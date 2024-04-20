# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InstanceMetadataDefaultsArgs', 'InstanceMetadataDefaults']

@pulumi.input_type
class InstanceMetadataDefaultsArgs:
    def __init__(__self__, *,
                 http_endpoint: Optional[pulumi.Input[str]] = None,
                 http_put_response_hop_limit: Optional[pulumi.Input[int]] = None,
                 http_tokens: Optional[pulumi.Input[str]] = None,
                 instance_metadata_tags: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a InstanceMetadataDefaults resource.
        :param pulumi.Input[str] http_endpoint: Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[int] http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        :param pulumi.Input[str] http_tokens: Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[str] instance_metadata_tags: Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        if http_endpoint is not None:
            pulumi.set(__self__, "http_endpoint", http_endpoint)
        if http_put_response_hop_limit is not None:
            pulumi.set(__self__, "http_put_response_hop_limit", http_put_response_hop_limit)
        if http_tokens is not None:
            pulumi.set(__self__, "http_tokens", http_tokens)
        if instance_metadata_tags is not None:
            pulumi.set(__self__, "instance_metadata_tags", instance_metadata_tags)

    @property
    @pulumi.getter(name="httpEndpoint")
    def http_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_endpoint")

    @http_endpoint.setter
    def http_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_endpoint", value)

    @property
    @pulumi.getter(name="httpPutResponseHopLimit")
    def http_put_response_hop_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        """
        return pulumi.get(self, "http_put_response_hop_limit")

    @http_put_response_hop_limit.setter
    def http_put_response_hop_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_put_response_hop_limit", value)

    @property
    @pulumi.getter(name="httpTokens")
    def http_tokens(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_tokens")

    @http_tokens.setter
    def http_tokens(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_tokens", value)

    @property
    @pulumi.getter(name="instanceMetadataTags")
    def instance_metadata_tags(self) -> Optional[pulumi.Input[str]]:
        """
        Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "instance_metadata_tags")

    @instance_metadata_tags.setter
    def instance_metadata_tags(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_metadata_tags", value)


@pulumi.input_type
class _InstanceMetadataDefaultsState:
    def __init__(__self__, *,
                 http_endpoint: Optional[pulumi.Input[str]] = None,
                 http_put_response_hop_limit: Optional[pulumi.Input[int]] = None,
                 http_tokens: Optional[pulumi.Input[str]] = None,
                 instance_metadata_tags: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceMetadataDefaults resources.
        :param pulumi.Input[str] http_endpoint: Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[int] http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        :param pulumi.Input[str] http_tokens: Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[str] instance_metadata_tags: Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        if http_endpoint is not None:
            pulumi.set(__self__, "http_endpoint", http_endpoint)
        if http_put_response_hop_limit is not None:
            pulumi.set(__self__, "http_put_response_hop_limit", http_put_response_hop_limit)
        if http_tokens is not None:
            pulumi.set(__self__, "http_tokens", http_tokens)
        if instance_metadata_tags is not None:
            pulumi.set(__self__, "instance_metadata_tags", instance_metadata_tags)

    @property
    @pulumi.getter(name="httpEndpoint")
    def http_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_endpoint")

    @http_endpoint.setter
    def http_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_endpoint", value)

    @property
    @pulumi.getter(name="httpPutResponseHopLimit")
    def http_put_response_hop_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        """
        return pulumi.get(self, "http_put_response_hop_limit")

    @http_put_response_hop_limit.setter
    def http_put_response_hop_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_put_response_hop_limit", value)

    @property
    @pulumi.getter(name="httpTokens")
    def http_tokens(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_tokens")

    @http_tokens.setter
    def http_tokens(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_tokens", value)

    @property
    @pulumi.getter(name="instanceMetadataTags")
    def instance_metadata_tags(self) -> Optional[pulumi.Input[str]]:
        """
        Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "instance_metadata_tags")

    @instance_metadata_tags.setter
    def instance_metadata_tags(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_metadata_tags", value)


class InstanceMetadataDefaults(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 http_endpoint: Optional[pulumi.Input[str]] = None,
                 http_put_response_hop_limit: Optional[pulumi.Input[int]] = None,
                 http_tokens: Optional[pulumi.Input[str]] = None,
                 instance_metadata_tags: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages regional EC2 instance metadata default settings.
        More information can be found in the [Configure instance metadata options for new instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-new-instances.html) user guide.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        enforce_imdsv2 = aws.ec2.InstanceMetadataDefaults("enforce-imdsv2",
            http_tokens="required",
            http_put_response_hop_limit=1)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        You cannot import this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] http_endpoint: Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[int] http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        :param pulumi.Input[str] http_tokens: Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[str] instance_metadata_tags: Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[InstanceMetadataDefaultsArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages regional EC2 instance metadata default settings.
        More information can be found in the [Configure instance metadata options for new instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-new-instances.html) user guide.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        enforce_imdsv2 = aws.ec2.InstanceMetadataDefaults("enforce-imdsv2",
            http_tokens="required",
            http_put_response_hop_limit=1)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        You cannot import this resource.

        :param str resource_name: The name of the resource.
        :param InstanceMetadataDefaultsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceMetadataDefaultsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 http_endpoint: Optional[pulumi.Input[str]] = None,
                 http_put_response_hop_limit: Optional[pulumi.Input[int]] = None,
                 http_tokens: Optional[pulumi.Input[str]] = None,
                 instance_metadata_tags: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceMetadataDefaultsArgs.__new__(InstanceMetadataDefaultsArgs)

            __props__.__dict__["http_endpoint"] = http_endpoint
            __props__.__dict__["http_put_response_hop_limit"] = http_put_response_hop_limit
            __props__.__dict__["http_tokens"] = http_tokens
            __props__.__dict__["instance_metadata_tags"] = instance_metadata_tags
        super(InstanceMetadataDefaults, __self__).__init__(
            'aws:ec2/instanceMetadataDefaults:InstanceMetadataDefaults',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            http_endpoint: Optional[pulumi.Input[str]] = None,
            http_put_response_hop_limit: Optional[pulumi.Input[int]] = None,
            http_tokens: Optional[pulumi.Input[str]] = None,
            instance_metadata_tags: Optional[pulumi.Input[str]] = None) -> 'InstanceMetadataDefaults':
        """
        Get an existing InstanceMetadataDefaults resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] http_endpoint: Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[int] http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        :param pulumi.Input[str] http_tokens: Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        :param pulumi.Input[str] instance_metadata_tags: Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceMetadataDefaultsState.__new__(_InstanceMetadataDefaultsState)

        __props__.__dict__["http_endpoint"] = http_endpoint
        __props__.__dict__["http_put_response_hop_limit"] = http_put_response_hop_limit
        __props__.__dict__["http_tokens"] = http_tokens
        __props__.__dict__["instance_metadata_tags"] = instance_metadata_tags
        return InstanceMetadataDefaults(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="httpEndpoint")
    def http_endpoint(self) -> pulumi.Output[str]:
        """
        Whether the metadata service is available. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_endpoint")

    @property
    @pulumi.getter(name="httpPutResponseHopLimit")
    def http_put_response_hop_limit(self) -> pulumi.Output[int]:
        """
        The desired HTTP PUT response hop limit for instance metadata requests. The larger the number, the further instance metadata requests can travel. Can be an integer from `1` to `64`, or `-1` to indicate no preference. Default: `-1`.
        """
        return pulumi.get(self, "http_put_response_hop_limit")

    @property
    @pulumi.getter(name="httpTokens")
    def http_tokens(self) -> pulumi.Output[str]:
        """
        Whether the metadata service requires session tokens, also referred to as _Instance Metadata Service Version 2 (IMDSv2)_. Can be `"optional"`, `"required"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "http_tokens")

    @property
    @pulumi.getter(name="instanceMetadataTags")
    def instance_metadata_tags(self) -> pulumi.Output[str]:
        """
        Enables or disables access to instance tags from the instance metadata service. Can be `"enabled"`, `"disabled"`, or `"no-preference"`. Default: `"no-preference"`.
        """
        return pulumi.get(self, "instance_metadata_tags")

