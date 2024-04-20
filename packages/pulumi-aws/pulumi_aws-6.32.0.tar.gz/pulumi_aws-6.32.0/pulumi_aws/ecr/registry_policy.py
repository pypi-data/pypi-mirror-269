# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RegistryPolicyArgs', 'RegistryPolicy']

@pulumi.input_type
class RegistryPolicyArgs:
    def __init__(__self__, *,
                 policy: pulumi.Input[str]):
        """
        The set of arguments for constructing a RegistryPolicy resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        """
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)


@pulumi.input_type
class _RegistryPolicyState:
    def __init__(__self__, *,
                 policy: Optional[pulumi.Input[str]] = None,
                 registry_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RegistryPolicy resources.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] registry_id: The registry ID where the registry was created.
        """
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if registry_id is not None:
            pulumi.set(__self__, "registry_id", registry_id)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> Optional[pulumi.Input[str]]:
        """
        The registry ID where the registry was created.
        """
        return pulumi.get(self, "registry_id")

    @registry_id.setter
    def registry_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "registry_id", value)


class RegistryPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Elastic Container Registry Policy.

        > **NOTE on ECR Registry Policies:** While the AWS Management Console interface may suggest the ability to define multiple policies by creating multiple statements, ECR registry policies are effectively managed as singular entities at the regional level by the AWS APIs. Therefore, the `ecr.RegistryPolicy` resource should be configured only once per region with all necessary statements defined in the same policy. Attempting to define multiple `ecr.RegistryPolicy` resources may result in perpetual differences, with one policy overriding another.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        current = aws.get_caller_identity()
        current_get_region = aws.get_region()
        current_get_partition = aws.get_partition()
        example = aws.ecr.RegistryPolicy("example", policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "testpolicy",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:{current_get_partition.partition}:iam::{current.account_id}:root",
                },
                "Action": ["ecr:ReplicateImage"],
                "Resource": [f"arn:{current_get_partition.partition}:ecr:{current_get_region.name}:{current.account_id}:repository/*"],
            }],
        }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import ECR Registry Policy using the registry id. For example:

        ```sh
        $ pulumi import aws:ecr/registryPolicy:RegistryPolicy example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegistryPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Elastic Container Registry Policy.

        > **NOTE on ECR Registry Policies:** While the AWS Management Console interface may suggest the ability to define multiple policies by creating multiple statements, ECR registry policies are effectively managed as singular entities at the regional level by the AWS APIs. Therefore, the `ecr.RegistryPolicy` resource should be configured only once per region with all necessary statements defined in the same policy. Attempting to define multiple `ecr.RegistryPolicy` resources may result in perpetual differences, with one policy overriding another.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        current = aws.get_caller_identity()
        current_get_region = aws.get_region()
        current_get_partition = aws.get_partition()
        example = aws.ecr.RegistryPolicy("example", policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "testpolicy",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:{current_get_partition.partition}:iam::{current.account_id}:root",
                },
                "Action": ["ecr:ReplicateImage"],
                "Resource": [f"arn:{current_get_partition.partition}:ecr:{current_get_region.name}:{current.account_id}:repository/*"],
            }],
        }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import ECR Registry Policy using the registry id. For example:

        ```sh
        $ pulumi import aws:ecr/registryPolicy:RegistryPolicy example 123456789012
        ```

        :param str resource_name: The name of the resource.
        :param RegistryPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegistryPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegistryPolicyArgs.__new__(RegistryPolicyArgs)

            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            __props__.__dict__["registry_id"] = None
        super(RegistryPolicy, __self__).__init__(
            'aws:ecr/registryPolicy:RegistryPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy: Optional[pulumi.Input[str]] = None,
            registry_id: Optional[pulumi.Input[str]] = None) -> 'RegistryPolicy':
        """
        Get an existing RegistryPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The policy document. This is a JSON formatted string.
        :param pulumi.Input[str] registry_id: The registry ID where the registry was created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RegistryPolicyState.__new__(_RegistryPolicyState)

        __props__.__dict__["policy"] = policy
        __props__.__dict__["registry_id"] = registry_id
        return RegistryPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The policy document. This is a JSON formatted string.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="registryId")
    def registry_id(self) -> pulumi.Output[str]:
        """
        The registry ID where the registry was created.
        """
        return pulumi.get(self, "registry_id")

