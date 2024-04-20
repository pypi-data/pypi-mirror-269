# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccessPointPolicyArgs', 'AccessPointPolicy']

@pulumi.input_type
class AccessPointPolicyArgs:
    def __init__(__self__, *,
                 access_point_arn: pulumi.Input[str],
                 policy: pulumi.Input[str]):
        """
        The set of arguments for constructing a AccessPointPolicy resource.
        :param pulumi.Input[str] access_point_arn: The ARN of the access point that you want to associate with the specified policy.
        :param pulumi.Input[str] policy: The policy that you want to apply to the specified access point.
        """
        pulumi.set(__self__, "access_point_arn", access_point_arn)
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the access point that you want to associate with the specified policy.
        """
        return pulumi.get(self, "access_point_arn")

    @access_point_arn.setter
    def access_point_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_point_arn", value)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        The policy that you want to apply to the specified access point.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)


@pulumi.input_type
class _AccessPointPolicyState:
    def __init__(__self__, *,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 has_public_access_policy: Optional[pulumi.Input[bool]] = None,
                 policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccessPointPolicy resources.
        :param pulumi.Input[str] access_point_arn: The ARN of the access point that you want to associate with the specified policy.
        :param pulumi.Input[bool] has_public_access_policy: Indicates whether this access point currently has a policy that allows public access.
        :param pulumi.Input[str] policy: The policy that you want to apply to the specified access point.
        """
        if access_point_arn is not None:
            pulumi.set(__self__, "access_point_arn", access_point_arn)
        if has_public_access_policy is not None:
            pulumi.set(__self__, "has_public_access_policy", has_public_access_policy)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the access point that you want to associate with the specified policy.
        """
        return pulumi.get(self, "access_point_arn")

    @access_point_arn.setter
    def access_point_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_point_arn", value)

    @property
    @pulumi.getter(name="hasPublicAccessPolicy")
    def has_public_access_policy(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether this access point currently has a policy that allows public access.
        """
        return pulumi.get(self, "has_public_access_policy")

    @has_public_access_policy.setter
    def has_public_access_policy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "has_public_access_policy", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The policy that you want to apply to the specified access point.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)


class AccessPointPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage an S3 Access Point resource policy.

        > **NOTE on Access Points and Access Point Policies:** The provider provides both a standalone Access Point Policy resource and an Access Point resource with a resource policy defined in-line. You cannot use an Access Point with in-line resource policy in conjunction with an Access Point Policy resource. Doing so will cause a conflict of policies and will overwrite the access point's resource policy.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example")
        example_access_point = aws.s3.AccessPoint("example",
            bucket=example.id,
            name="example",
            public_access_block_configuration=aws.s3.AccessPointPublicAccessBlockConfigurationArgs(
                block_public_acls=True,
                block_public_policy=False,
                ignore_public_acls=True,
                restrict_public_buckets=False,
            ))
        example_access_point_policy = aws.s3control.AccessPointPolicy("example",
            access_point_arn=example_access_point.arn,
            policy=pulumi.Output.json_dumps({
                "Version": "2008-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": "s3:GetObjectTagging",
                    "Principal": {
                        "AWS": "*",
                    },
                    "Resource": example_access_point.arn.apply(lambda arn: f"{arn}/object/*"),
                }],
            }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Access Point policies using the `access_point_arn`. For example:

        ```sh
        $ pulumi import aws:s3control/accessPointPolicy:AccessPointPolicy example arn:aws:s3:us-west-2:123456789012:accesspoint/example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_point_arn: The ARN of the access point that you want to associate with the specified policy.
        :param pulumi.Input[str] policy: The policy that you want to apply to the specified access point.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessPointPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage an S3 Access Point resource policy.

        > **NOTE on Access Points and Access Point Policies:** The provider provides both a standalone Access Point Policy resource and an Access Point resource with a resource policy defined in-line. You cannot use an Access Point with in-line resource policy in conjunction with an Access Point Policy resource. Doing so will cause a conflict of policies and will overwrite the access point's resource policy.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="example")
        example_access_point = aws.s3.AccessPoint("example",
            bucket=example.id,
            name="example",
            public_access_block_configuration=aws.s3.AccessPointPublicAccessBlockConfigurationArgs(
                block_public_acls=True,
                block_public_policy=False,
                ignore_public_acls=True,
                restrict_public_buckets=False,
            ))
        example_access_point_policy = aws.s3control.AccessPointPolicy("example",
            access_point_arn=example_access_point.arn,
            policy=pulumi.Output.json_dumps({
                "Version": "2008-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": "s3:GetObjectTagging",
                    "Principal": {
                        "AWS": "*",
                    },
                    "Resource": example_access_point.arn.apply(lambda arn: f"{arn}/object/*"),
                }],
            }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Access Point policies using the `access_point_arn`. For example:

        ```sh
        $ pulumi import aws:s3control/accessPointPolicy:AccessPointPolicy example arn:aws:s3:us-west-2:123456789012:accesspoint/example
        ```

        :param str resource_name: The name of the resource.
        :param AccessPointPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessPointPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessPointPolicyArgs.__new__(AccessPointPolicyArgs)

            if access_point_arn is None and not opts.urn:
                raise TypeError("Missing required property 'access_point_arn'")
            __props__.__dict__["access_point_arn"] = access_point_arn
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            __props__.__dict__["has_public_access_policy"] = None
        super(AccessPointPolicy, __self__).__init__(
            'aws:s3control/accessPointPolicy:AccessPointPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_point_arn: Optional[pulumi.Input[str]] = None,
            has_public_access_policy: Optional[pulumi.Input[bool]] = None,
            policy: Optional[pulumi.Input[str]] = None) -> 'AccessPointPolicy':
        """
        Get an existing AccessPointPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_point_arn: The ARN of the access point that you want to associate with the specified policy.
        :param pulumi.Input[bool] has_public_access_policy: Indicates whether this access point currently has a policy that allows public access.
        :param pulumi.Input[str] policy: The policy that you want to apply to the specified access point.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessPointPolicyState.__new__(_AccessPointPolicyState)

        __props__.__dict__["access_point_arn"] = access_point_arn
        __props__.__dict__["has_public_access_policy"] = has_public_access_policy
        __props__.__dict__["policy"] = policy
        return AccessPointPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the access point that you want to associate with the specified policy.
        """
        return pulumi.get(self, "access_point_arn")

    @property
    @pulumi.getter(name="hasPublicAccessPolicy")
    def has_public_access_policy(self) -> pulumi.Output[bool]:
        """
        Indicates whether this access point currently has a policy that allows public access.
        """
        return pulumi.get(self, "has_public_access_policy")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The policy that you want to apply to the specified access point.
        """
        return pulumi.get(self, "policy")

