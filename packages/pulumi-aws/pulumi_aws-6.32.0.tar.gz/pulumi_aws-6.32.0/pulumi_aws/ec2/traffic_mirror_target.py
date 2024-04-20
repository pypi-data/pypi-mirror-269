# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TrafficMirrorTargetArgs', 'TrafficMirrorTarget']

@pulumi.input_type
class TrafficMirrorTargetArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 gateway_load_balancer_endpoint_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 network_load_balancer_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a TrafficMirrorTarget resource.
        :param pulumi.Input[str] description: A description of the traffic mirror session.
        :param pulumi.Input[str] gateway_load_balancer_endpoint_id: The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        :param pulumi.Input[str] network_interface_id: The network interface ID that is associated with the target.
        :param pulumi.Input[str] network_load_balancer_arn: The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
               
               **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if gateway_load_balancer_endpoint_id is not None:
            pulumi.set(__self__, "gateway_load_balancer_endpoint_id", gateway_load_balancer_endpoint_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if network_load_balancer_arn is not None:
            pulumi.set(__self__, "network_load_balancer_arn", network_load_balancer_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the traffic mirror session.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="gatewayLoadBalancerEndpointId")
    def gateway_load_balancer_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "gateway_load_balancer_endpoint_id")

    @gateway_load_balancer_endpoint_id.setter
    def gateway_load_balancer_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_load_balancer_endpoint_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The network interface ID that is associated with the target.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)

    @property
    @pulumi.getter(name="networkLoadBalancerArn")
    def network_load_balancer_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "network_load_balancer_arn")

    @network_load_balancer_arn.setter
    def network_load_balancer_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_load_balancer_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.

        **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _TrafficMirrorTargetState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateway_load_balancer_endpoint_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 network_load_balancer_arn: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering TrafficMirrorTarget resources.
        :param pulumi.Input[str] arn: The ARN of the traffic mirror target.
        :param pulumi.Input[str] description: A description of the traffic mirror session.
        :param pulumi.Input[str] gateway_load_balancer_endpoint_id: The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        :param pulumi.Input[str] network_interface_id: The network interface ID that is associated with the target.
        :param pulumi.Input[str] network_load_balancer_arn: The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the traffic mirror target.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
               
               **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if gateway_load_balancer_endpoint_id is not None:
            pulumi.set(__self__, "gateway_load_balancer_endpoint_id", gateway_load_balancer_endpoint_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if network_load_balancer_arn is not None:
            pulumi.set(__self__, "network_load_balancer_arn", network_load_balancer_arn)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
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
        The ARN of the traffic mirror target.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the traffic mirror session.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="gatewayLoadBalancerEndpointId")
    def gateway_load_balancer_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "gateway_load_balancer_endpoint_id")

    @gateway_load_balancer_endpoint_id.setter
    def gateway_load_balancer_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_load_balancer_endpoint_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The network interface ID that is associated with the target.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)

    @property
    @pulumi.getter(name="networkLoadBalancerArn")
    def network_load_balancer_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "network_load_balancer_arn")

    @network_load_balancer_arn.setter
    def network_load_balancer_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_load_balancer_arn", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the AWS account that owns the traffic mirror target.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.

        **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
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


class TrafficMirrorTarget(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateway_load_balancer_endpoint_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 network_load_balancer_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Traffic mirror target.\\
        Read [limits and considerations](https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-considerations.html) for traffic mirroring

        ## Example Usage

        To create a basic traffic mirror session

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        nlb = aws.ec2.TrafficMirrorTarget("nlb",
            description="NLB target",
            network_load_balancer_arn=lb["arn"])
        eni = aws.ec2.TrafficMirrorTarget("eni",
            description="ENI target",
            network_interface_id=test["primaryNetworkInterfaceId"])
        gwlb = aws.ec2.TrafficMirrorTarget("gwlb",
            description="GWLB target",
            gateway_load_balancer_endpoint_id=example["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import traffic mirror targets using the `id`. For example:

        ```sh
        $ pulumi import aws:ec2/trafficMirrorTarget:TrafficMirrorTarget target tmt-0c13a005422b86606
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the traffic mirror session.
        :param pulumi.Input[str] gateway_load_balancer_endpoint_id: The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        :param pulumi.Input[str] network_interface_id: The network interface ID that is associated with the target.
        :param pulumi.Input[str] network_load_balancer_arn: The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
               
               **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[TrafficMirrorTargetArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Traffic mirror target.\\
        Read [limits and considerations](https://docs.aws.amazon.com/vpc/latest/mirroring/traffic-mirroring-considerations.html) for traffic mirroring

        ## Example Usage

        To create a basic traffic mirror session

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        nlb = aws.ec2.TrafficMirrorTarget("nlb",
            description="NLB target",
            network_load_balancer_arn=lb["arn"])
        eni = aws.ec2.TrafficMirrorTarget("eni",
            description="ENI target",
            network_interface_id=test["primaryNetworkInterfaceId"])
        gwlb = aws.ec2.TrafficMirrorTarget("gwlb",
            description="GWLB target",
            gateway_load_balancer_endpoint_id=example["id"])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import traffic mirror targets using the `id`. For example:

        ```sh
        $ pulumi import aws:ec2/trafficMirrorTarget:TrafficMirrorTarget target tmt-0c13a005422b86606
        ```

        :param str resource_name: The name of the resource.
        :param TrafficMirrorTargetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrafficMirrorTargetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 gateway_load_balancer_endpoint_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 network_load_balancer_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrafficMirrorTargetArgs.__new__(TrafficMirrorTargetArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["gateway_load_balancer_endpoint_id"] = gateway_load_balancer_endpoint_id
            __props__.__dict__["network_interface_id"] = network_interface_id
            __props__.__dict__["network_load_balancer_arn"] = network_load_balancer_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["tags_all"] = None
        super(TrafficMirrorTarget, __self__).__init__(
            'aws:ec2/trafficMirrorTarget:TrafficMirrorTarget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            gateway_load_balancer_endpoint_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None,
            network_load_balancer_arn: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'TrafficMirrorTarget':
        """
        Get an existing TrafficMirrorTarget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the traffic mirror target.
        :param pulumi.Input[str] description: A description of the traffic mirror session.
        :param pulumi.Input[str] gateway_load_balancer_endpoint_id: The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        :param pulumi.Input[str] network_interface_id: The network interface ID that is associated with the target.
        :param pulumi.Input[str] network_load_balancer_arn: The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        :param pulumi.Input[str] owner_id: The ID of the AWS account that owns the traffic mirror target.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
               
               **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TrafficMirrorTargetState.__new__(_TrafficMirrorTargetState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["gateway_load_balancer_endpoint_id"] = gateway_load_balancer_endpoint_id
        __props__.__dict__["network_interface_id"] = network_interface_id
        __props__.__dict__["network_load_balancer_arn"] = network_load_balancer_arn
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return TrafficMirrorTarget(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the traffic mirror target.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the traffic mirror session.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="gatewayLoadBalancerEndpointId")
    def gateway_load_balancer_endpoint_id(self) -> pulumi.Output[Optional[str]]:
        """
        The VPC Endpoint Id of the Gateway Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "gateway_load_balancer_endpoint_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[Optional[str]]:
        """
        The network interface ID that is associated with the target.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter(name="networkLoadBalancerArn")
    def network_load_balancer_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the Network Load Balancer that is associated with the target.
        """
        return pulumi.get(self, "network_load_balancer_arn")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The ID of the AWS account that owns the traffic mirror target.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.

        **NOTE:** Either `network_interface_id` or `network_load_balancer_arn` should be specified and both should not be specified together
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

