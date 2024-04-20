# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:
    def __init__(__self__, *,
                 policy: pulumi.Input[str],
                 resource_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] policy: JSON-formatted IAM policy to attach to the specified private CA resource.
        :param pulumi.Input[str] resource_arn: ARN of the private CA to associate with the policy.
        """
        pulumi.set(__self__, "policy", policy)
        pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        JSON-formatted IAM policy to attach to the specified private CA resource.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Input[str]:
        """
        ARN of the private CA to associate with the policy.
        """
        return pulumi.get(self, "resource_arn")

    @resource_arn.setter
    def resource_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_arn", value)


@pulumi.input_type
class _PolicyState:
    def __init__(__self__, *,
                 policy: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input[str] policy: JSON-formatted IAM policy to attach to the specified private CA resource.
        :param pulumi.Input[str] resource_arn: ARN of the private CA to associate with the policy.
        """
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if resource_arn is not None:
            pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        JSON-formatted IAM policy to attach to the specified private CA resource.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the private CA to associate with the policy.
        """
        return pulumi.get(self, "resource_arn")

    @resource_arn.setter
    def resource_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_arn", value)


class Policy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a resource based policy to a private CA.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.iam.get_policy_document(statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="1",
                effect="Allow",
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS",
                    identifiers=[current["accountId"]],
                )],
                actions=[
                    "acm-pca:DescribeCertificateAuthority",
                    "acm-pca:GetCertificate",
                    "acm-pca:GetCertificateAuthorityCertificate",
                    "acm-pca:ListPermissions",
                    "acm-pca:ListTags",
                ],
                resources=[example_aws_acmpca_certificate_authority["arn"]],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="2",
                effect=allow,
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS",
                    identifiers=[current["accountId"]],
                )],
                actions=["acm-pca:IssueCertificate"],
                resources=[example_aws_acmpca_certificate_authority["arn"]],
                conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
                    test="StringEquals",
                    variable="acm-pca:TemplateArn",
                    values=["arn:aws:acm-pca:::template/EndEntityCertificate/V1"],
                )],
            ),
        ])
        example_policy = aws.acmpca.Policy("example",
            resource_arn=example_aws_acmpca_certificate_authority["arn"],
            policy=example.json)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_acmpca_policy` using the `resource_arn` value. For example:

        ```sh
        $ pulumi import aws:acmpca/policy:Policy example arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: JSON-formatted IAM policy to attach to the specified private CA resource.
        :param pulumi.Input[str] resource_arn: ARN of the private CA to associate with the policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a resource based policy to a private CA.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.iam.get_policy_document(statements=[
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="1",
                effect="Allow",
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS",
                    identifiers=[current["accountId"]],
                )],
                actions=[
                    "acm-pca:DescribeCertificateAuthority",
                    "acm-pca:GetCertificate",
                    "acm-pca:GetCertificateAuthorityCertificate",
                    "acm-pca:ListPermissions",
                    "acm-pca:ListTags",
                ],
                resources=[example_aws_acmpca_certificate_authority["arn"]],
            ),
            aws.iam.GetPolicyDocumentStatementArgs(
                sid="2",
                effect=allow,
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS",
                    identifiers=[current["accountId"]],
                )],
                actions=["acm-pca:IssueCertificate"],
                resources=[example_aws_acmpca_certificate_authority["arn"]],
                conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
                    test="StringEquals",
                    variable="acm-pca:TemplateArn",
                    values=["arn:aws:acm-pca:::template/EndEntityCertificate/V1"],
                )],
            ),
        ])
        example_policy = aws.acmpca.Policy("example",
            resource_arn=example_aws_acmpca_certificate_authority["arn"],
            policy=example.json)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_acmpca_policy` using the `resource_arn` value. For example:

        ```sh
        $ pulumi import aws:acmpca/policy:Policy example arn:aws:acm-pca:us-east-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012
        ```

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyArgs.__new__(PolicyArgs)

            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            if resource_arn is None and not opts.urn:
                raise TypeError("Missing required property 'resource_arn'")
            __props__.__dict__["resource_arn"] = resource_arn
        super(Policy, __self__).__init__(
            'aws:acmpca/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy: Optional[pulumi.Input[str]] = None,
            resource_arn: Optional[pulumi.Input[str]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: JSON-formatted IAM policy to attach to the specified private CA resource.
        :param pulumi.Input[str] resource_arn: ARN of the private CA to associate with the policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyState.__new__(_PolicyState)

        __props__.__dict__["policy"] = policy
        __props__.__dict__["resource_arn"] = resource_arn
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        JSON-formatted IAM policy to attach to the specified private CA resource.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Output[str]:
        """
        ARN of the private CA to associate with the policy.
        """
        return pulumi.get(self, "resource_arn")

