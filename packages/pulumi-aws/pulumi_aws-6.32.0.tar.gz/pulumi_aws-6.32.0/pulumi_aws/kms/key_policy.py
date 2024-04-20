# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['KeyPolicyArgs', 'KeyPolicy']

@pulumi.input_type
class KeyPolicyArgs:
    def __init__(__self__, *,
                 key_id: pulumi.Input[str],
                 policy: pulumi.Input[str],
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a KeyPolicy resource.
        :param pulumi.Input[str] key_id: The ID of the KMS Key to attach the policy.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.
               
               > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        """
        pulumi.set(__self__, "key_id", key_id)
        pulumi.set(__self__, "policy", policy)
        if bypass_policy_lockout_safety_check is not None:
            pulumi.set(__self__, "bypass_policy_lockout_safety_check", bypass_policy_lockout_safety_check)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Input[str]:
        """
        The ID of the KMS Key to attach the policy.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.

        > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @bypass_policy_lockout_safety_check.setter
    def bypass_policy_lockout_safety_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_policy_lockout_safety_check", value)


@pulumi.input_type
class _KeyPolicyState:
    def __init__(__self__, *,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering KeyPolicy resources.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        :param pulumi.Input[str] key_id: The ID of the KMS Key to attach the policy.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.
               
               > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        if bypass_policy_lockout_safety_check is not None:
            pulumi.set(__self__, "bypass_policy_lockout_safety_check", bypass_policy_lockout_safety_check)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @bypass_policy_lockout_safety_check.setter
    def bypass_policy_lockout_safety_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_policy_lockout_safety_check", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the KMS Key to attach the policy.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.

        > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)


class KeyPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a policy to a KMS Key.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example = aws.kms.Key("example", description="example")
        example_key_policy = aws.kms.KeyPolicy("example",
            key_id=example.id,
            policy=json.dumps({
                "Id": "example",
                "Statement": [{
                    "Action": "kms:*",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*",
                    },
                    "Resource": "*",
                    "Sid": "Enable IAM User Permissions",
                }],
                "Version": "2012-10-17",
            }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import KMS Key Policies using the `key_id`. For example:

        ```sh
        $ pulumi import aws:kms/keyPolicy:KeyPolicy a 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        :param pulumi.Input[str] key_id: The ID of the KMS Key to attach the policy.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.
               
               > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a policy to a KMS Key.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example = aws.kms.Key("example", description="example")
        example_key_policy = aws.kms.KeyPolicy("example",
            key_id=example.id,
            policy=json.dumps({
                "Id": "example",
                "Statement": [{
                    "Action": "kms:*",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*",
                    },
                    "Resource": "*",
                    "Sid": "Enable IAM User Permissions",
                }],
                "Version": "2012-10-17",
            }))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import KMS Key Policies using the `key_id`. For example:

        ```sh
        $ pulumi import aws:kms/keyPolicy:KeyPolicy a 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param KeyPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyPolicyArgs.__new__(KeyPolicyArgs)

            __props__.__dict__["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
            if key_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_id'")
            __props__.__dict__["key_id"] = key_id
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
        super(KeyPolicy, __self__).__init__(
            'aws:kms/keyPolicy:KeyPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
            key_id: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None) -> 'KeyPolicy':
        """
        Get an existing KeyPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        :param pulumi.Input[str] key_id: The ID of the KMS Key to attach the policy.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.
               
               > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KeyPolicyState.__new__(_KeyPolicyState)

        __props__.__dict__["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
        __props__.__dict__["key_id"] = key_id
        __props__.__dict__["policy"] = policy
        return KeyPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> pulumi.Output[Optional[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. If this value is set, and the resource is destroyed, a warning will be shown, and the resource will be removed from state.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[str]:
        """
        The ID of the KMS Key to attach the policy.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam_get_policy_document`, in the form that designates a principal, can be used. For more information about building policy documents, see the AWS IAM Policy Document Guide.

        > **NOTE:** Note: All KMS keys must have a key policy. If a key policy is not specified, or this resource is destroyed, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
        """
        return pulumi.get(self, "policy")

