# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EventApiDestinationArgs', 'EventApiDestination']

@pulumi.input_type
class EventApiDestinationArgs:
    def __init__(__self__, *,
                 connection_arn: pulumi.Input[str],
                 http_method: pulumi.Input[str],
                 invocation_endpoint: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 invocation_rate_limit_per_second: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EventApiDestination resource.
        :param pulumi.Input[str] connection_arn: ARN of the EventBridge Connection to use for the API Destination.
        :param pulumi.Input[str] http_method: Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        :param pulumi.Input[str] invocation_endpoint: URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        :param pulumi.Input[str] description: The description of the new API Destination. Maximum of 512 characters.
        :param pulumi.Input[int] invocation_rate_limit_per_second: Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        :param pulumi.Input[str] name: The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        pulumi.set(__self__, "connection_arn", connection_arn)
        pulumi.set(__self__, "http_method", http_method)
        pulumi.set(__self__, "invocation_endpoint", invocation_endpoint)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if invocation_rate_limit_per_second is not None:
            pulumi.set(__self__, "invocation_rate_limit_per_second", invocation_rate_limit_per_second)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> pulumi.Input[str]:
        """
        ARN of the EventBridge Connection to use for the API Destination.
        """
        return pulumi.get(self, "connection_arn")

    @connection_arn.setter
    def connection_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "connection_arn", value)

    @property
    @pulumi.getter(name="httpMethod")
    def http_method(self) -> pulumi.Input[str]:
        """
        Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        """
        return pulumi.get(self, "http_method")

    @http_method.setter
    def http_method(self, value: pulumi.Input[str]):
        pulumi.set(self, "http_method", value)

    @property
    @pulumi.getter(name="invocationEndpoint")
    def invocation_endpoint(self) -> pulumi.Input[str]:
        """
        URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        """
        return pulumi.get(self, "invocation_endpoint")

    @invocation_endpoint.setter
    def invocation_endpoint(self, value: pulumi.Input[str]):
        pulumi.set(self, "invocation_endpoint", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the new API Destination. Maximum of 512 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="invocationRateLimitPerSecond")
    def invocation_rate_limit_per_second(self) -> Optional[pulumi.Input[int]]:
        """
        Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        """
        return pulumi.get(self, "invocation_rate_limit_per_second")

    @invocation_rate_limit_per_second.setter
    def invocation_rate_limit_per_second(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "invocation_rate_limit_per_second", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _EventApiDestinationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 connection_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 http_method: Optional[pulumi.Input[str]] = None,
                 invocation_endpoint: Optional[pulumi.Input[str]] = None,
                 invocation_rate_limit_per_second: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EventApiDestination resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the event API Destination.
        :param pulumi.Input[str] connection_arn: ARN of the EventBridge Connection to use for the API Destination.
        :param pulumi.Input[str] description: The description of the new API Destination. Maximum of 512 characters.
        :param pulumi.Input[str] http_method: Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        :param pulumi.Input[str] invocation_endpoint: URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        :param pulumi.Input[int] invocation_rate_limit_per_second: Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        :param pulumi.Input[str] name: The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if connection_arn is not None:
            pulumi.set(__self__, "connection_arn", connection_arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if http_method is not None:
            pulumi.set(__self__, "http_method", http_method)
        if invocation_endpoint is not None:
            pulumi.set(__self__, "invocation_endpoint", invocation_endpoint)
        if invocation_rate_limit_per_second is not None:
            pulumi.set(__self__, "invocation_rate_limit_per_second", invocation_rate_limit_per_second)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the event API Destination.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the EventBridge Connection to use for the API Destination.
        """
        return pulumi.get(self, "connection_arn")

    @connection_arn.setter
    def connection_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the new API Destination. Maximum of 512 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="httpMethod")
    def http_method(self) -> Optional[pulumi.Input[str]]:
        """
        Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        """
        return pulumi.get(self, "http_method")

    @http_method.setter
    def http_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_method", value)

    @property
    @pulumi.getter(name="invocationEndpoint")
    def invocation_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        """
        return pulumi.get(self, "invocation_endpoint")

    @invocation_endpoint.setter
    def invocation_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invocation_endpoint", value)

    @property
    @pulumi.getter(name="invocationRateLimitPerSecond")
    def invocation_rate_limit_per_second(self) -> Optional[pulumi.Input[int]]:
        """
        Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        """
        return pulumi.get(self, "invocation_rate_limit_per_second")

    @invocation_rate_limit_per_second.setter
    def invocation_rate_limit_per_second(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "invocation_rate_limit_per_second", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class EventApiDestination(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 http_method: Optional[pulumi.Input[str]] = None,
                 invocation_endpoint: Optional[pulumi.Input[str]] = None,
                 invocation_rate_limit_per_second: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an EventBridge event API Destination resource.

        > **Note:** EventBridge was formerly known as CloudWatch Events. The functionality is identical.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.cloudwatch.EventApiDestination("test",
            name="api-destination",
            description="An API Destination",
            invocation_endpoint="https://api.destination.com/endpoint",
            http_method="POST",
            invocation_rate_limit_per_second=20,
            connection_arn=test_aws_cloudwatch_event_connection["arn"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import EventBridge API Destinations using the `name`. For example:

        ```sh
        $ pulumi import aws:cloudwatch/eventApiDestination:EventApiDestination test api-destination
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_arn: ARN of the EventBridge Connection to use for the API Destination.
        :param pulumi.Input[str] description: The description of the new API Destination. Maximum of 512 characters.
        :param pulumi.Input[str] http_method: Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        :param pulumi.Input[str] invocation_endpoint: URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        :param pulumi.Input[int] invocation_rate_limit_per_second: Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        :param pulumi.Input[str] name: The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventApiDestinationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an EventBridge event API Destination resource.

        > **Note:** EventBridge was formerly known as CloudWatch Events. The functionality is identical.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.cloudwatch.EventApiDestination("test",
            name="api-destination",
            description="An API Destination",
            invocation_endpoint="https://api.destination.com/endpoint",
            http_method="POST",
            invocation_rate_limit_per_second=20,
            connection_arn=test_aws_cloudwatch_event_connection["arn"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import EventBridge API Destinations using the `name`. For example:

        ```sh
        $ pulumi import aws:cloudwatch/eventApiDestination:EventApiDestination test api-destination
        ```

        :param str resource_name: The name of the resource.
        :param EventApiDestinationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventApiDestinationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 http_method: Optional[pulumi.Input[str]] = None,
                 invocation_endpoint: Optional[pulumi.Input[str]] = None,
                 invocation_rate_limit_per_second: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventApiDestinationArgs.__new__(EventApiDestinationArgs)

            if connection_arn is None and not opts.urn:
                raise TypeError("Missing required property 'connection_arn'")
            __props__.__dict__["connection_arn"] = connection_arn
            __props__.__dict__["description"] = description
            if http_method is None and not opts.urn:
                raise TypeError("Missing required property 'http_method'")
            __props__.__dict__["http_method"] = http_method
            if invocation_endpoint is None and not opts.urn:
                raise TypeError("Missing required property 'invocation_endpoint'")
            __props__.__dict__["invocation_endpoint"] = invocation_endpoint
            __props__.__dict__["invocation_rate_limit_per_second"] = invocation_rate_limit_per_second
            __props__.__dict__["name"] = name
            __props__.__dict__["arn"] = None
        super(EventApiDestination, __self__).__init__(
            'aws:cloudwatch/eventApiDestination:EventApiDestination',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            connection_arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            http_method: Optional[pulumi.Input[str]] = None,
            invocation_endpoint: Optional[pulumi.Input[str]] = None,
            invocation_rate_limit_per_second: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'EventApiDestination':
        """
        Get an existing EventApiDestination resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the event API Destination.
        :param pulumi.Input[str] connection_arn: ARN of the EventBridge Connection to use for the API Destination.
        :param pulumi.Input[str] description: The description of the new API Destination. Maximum of 512 characters.
        :param pulumi.Input[str] http_method: Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        :param pulumi.Input[str] invocation_endpoint: URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        :param pulumi.Input[int] invocation_rate_limit_per_second: Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        :param pulumi.Input[str] name: The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EventApiDestinationState.__new__(_EventApiDestinationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["connection_arn"] = connection_arn
        __props__.__dict__["description"] = description
        __props__.__dict__["http_method"] = http_method
        __props__.__dict__["invocation_endpoint"] = invocation_endpoint
        __props__.__dict__["invocation_rate_limit_per_second"] = invocation_rate_limit_per_second
        __props__.__dict__["name"] = name
        return EventApiDestination(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the event API Destination.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> pulumi.Output[str]:
        """
        ARN of the EventBridge Connection to use for the API Destination.
        """
        return pulumi.get(self, "connection_arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the new API Destination. Maximum of 512 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="httpMethod")
    def http_method(self) -> pulumi.Output[str]:
        """
        Select the HTTP method used for the invocation endpoint, such as GET, POST, PUT, etc.
        """
        return pulumi.get(self, "http_method")

    @property
    @pulumi.getter(name="invocationEndpoint")
    def invocation_endpoint(self) -> pulumi.Output[str]:
        """
        URL endpoint to invoke as a target. This could be a valid endpoint generated by a partner service. You can include "*" as path parameters wildcards to be set from the Target HttpParameters.
        """
        return pulumi.get(self, "invocation_endpoint")

    @property
    @pulumi.getter(name="invocationRateLimitPerSecond")
    def invocation_rate_limit_per_second(self) -> pulumi.Output[Optional[int]]:
        """
        Enter the maximum number of invocations per second to allow for this destination. Enter a value greater than 0 (default 300).
        """
        return pulumi.get(self, "invocation_rate_limit_per_second")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the new API Destination. The name must be unique for your account. Maximum of 64 characters consisting of numbers, lower/upper case letters, .,-,_.
        """
        return pulumi.get(self, "name")

