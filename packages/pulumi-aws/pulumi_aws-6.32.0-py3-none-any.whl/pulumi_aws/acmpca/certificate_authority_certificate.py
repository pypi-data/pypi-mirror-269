# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CertificateAuthorityCertificateArgs', 'CertificateAuthorityCertificate']

@pulumi.input_type
class CertificateAuthorityCertificateArgs:
    def __init__(__self__, *,
                 certificate: pulumi.Input[str],
                 certificate_authority_arn: pulumi.Input[str],
                 certificate_chain: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CertificateAuthorityCertificate resource.
        :param pulumi.Input[str] certificate: PEM-encoded certificate for the Certificate Authority.
        :param pulumi.Input[str] certificate_authority_arn: ARN of the Certificate Authority.
        :param pulumi.Input[str] certificate_chain: PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        pulumi.set(__self__, "certificate", certificate)
        pulumi.set(__self__, "certificate_authority_arn", certificate_authority_arn)
        if certificate_chain is not None:
            pulumi.set(__self__, "certificate_chain", certificate_chain)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Input[str]:
        """
        PEM-encoded certificate for the Certificate Authority.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> pulumi.Input[str]:
        """
        ARN of the Certificate Authority.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_authority_arn", value)

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> Optional[pulumi.Input[str]]:
        """
        PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        return pulumi.get(self, "certificate_chain")

    @certificate_chain.setter
    def certificate_chain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_chain", value)


@pulumi.input_type
class _CertificateAuthorityCertificateState:
    def __init__(__self__, *,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CertificateAuthorityCertificate resources.
        :param pulumi.Input[str] certificate: PEM-encoded certificate for the Certificate Authority.
        :param pulumi.Input[str] certificate_authority_arn: ARN of the Certificate Authority.
        :param pulumi.Input[str] certificate_chain: PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if certificate_authority_arn is not None:
            pulumi.set(__self__, "certificate_authority_arn", certificate_authority_arn)
        if certificate_chain is not None:
            pulumi.set(__self__, "certificate_chain", certificate_chain)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        PEM-encoded certificate for the Certificate Authority.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Certificate Authority.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_authority_arn", value)

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> Optional[pulumi.Input[str]]:
        """
        PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        return pulumi.get(self, "certificate_chain")

    @certificate_chain.setter
    def certificate_chain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_chain", value)


class CertificateAuthorityCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Associates a certificate with an AWS Certificate Manager Private Certificate Authority (ACM PCA Certificate Authority). An ACM PCA Certificate Authority is unable to issue certificates until it has a certificate associated with it. A root level ACM PCA Certificate Authority is able to self-sign its own root certificate.

        ## Example Usage

        ### Self-Signed Root Certificate Authority Certificate

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example_certificate_authority = aws.acmpca.CertificateAuthority("example",
            type="ROOT",
            certificate_authority_configuration=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationArgs(
                key_algorithm="RSA_4096",
                signing_algorithm="SHA512WITHRSA",
                subject=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationSubjectArgs(
                    common_name="example.com",
                ),
            ))
        current = aws.get_partition()
        example_certificate = aws.acmpca.Certificate("example",
            certificate_authority_arn=example_certificate_authority.arn,
            certificate_signing_request=example_certificate_authority.certificate_signing_request,
            signing_algorithm="SHA512WITHRSA",
            template_arn=f"arn:{current.partition}:acm-pca:::template/RootCACertificate/V1",
            validity=aws.acmpca.CertificateValidityArgs(
                type="YEARS",
                value="1",
            ))
        example = aws.acmpca.CertificateAuthorityCertificate("example",
            certificate_authority_arn=example_certificate_authority.arn,
            certificate=example_certificate.certificate,
            certificate_chain=example_certificate.certificate_chain)
        ```
        <!--End PulumiCodeChooser -->

        ### Certificate for Subordinate Certificate Authority

        Note that the certificate for the subordinate certificate authority must be issued by the root certificate authority using a signing request from the subordinate certificate authority.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        subordinate_certificate_authority = aws.acmpca.CertificateAuthority("subordinate",
            type="SUBORDINATE",
            certificate_authority_configuration=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationArgs(
                key_algorithm="RSA_2048",
                signing_algorithm="SHA512WITHRSA",
                subject=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationSubjectArgs(
                    common_name="sub.example.com",
                ),
            ))
        root = aws.acmpca.CertificateAuthority("root")
        current = aws.get_partition()
        subordinate_certificate = aws.acmpca.Certificate("subordinate",
            certificate_authority_arn=root.arn,
            certificate_signing_request=subordinate_certificate_authority.certificate_signing_request,
            signing_algorithm="SHA512WITHRSA",
            template_arn=f"arn:{current.partition}:acm-pca:::template/SubordinateCACertificate_PathLen0/V1",
            validity=aws.acmpca.CertificateValidityArgs(
                type="YEARS",
                value="1",
            ))
        subordinate = aws.acmpca.CertificateAuthorityCertificate("subordinate",
            certificate_authority_arn=subordinate_certificate_authority.arn,
            certificate=subordinate_certificate.certificate,
            certificate_chain=subordinate_certificate.certificate_chain)
        root_certificate_authority_certificate = aws.acmpca.CertificateAuthorityCertificate("root")
        root_certificate = aws.acmpca.Certificate("root")
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate: PEM-encoded certificate for the Certificate Authority.
        :param pulumi.Input[str] certificate_authority_arn: ARN of the Certificate Authority.
        :param pulumi.Input[str] certificate_chain: PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CertificateAuthorityCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Associates a certificate with an AWS Certificate Manager Private Certificate Authority (ACM PCA Certificate Authority). An ACM PCA Certificate Authority is unable to issue certificates until it has a certificate associated with it. A root level ACM PCA Certificate Authority is able to self-sign its own root certificate.

        ## Example Usage

        ### Self-Signed Root Certificate Authority Certificate

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example_certificate_authority = aws.acmpca.CertificateAuthority("example",
            type="ROOT",
            certificate_authority_configuration=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationArgs(
                key_algorithm="RSA_4096",
                signing_algorithm="SHA512WITHRSA",
                subject=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationSubjectArgs(
                    common_name="example.com",
                ),
            ))
        current = aws.get_partition()
        example_certificate = aws.acmpca.Certificate("example",
            certificate_authority_arn=example_certificate_authority.arn,
            certificate_signing_request=example_certificate_authority.certificate_signing_request,
            signing_algorithm="SHA512WITHRSA",
            template_arn=f"arn:{current.partition}:acm-pca:::template/RootCACertificate/V1",
            validity=aws.acmpca.CertificateValidityArgs(
                type="YEARS",
                value="1",
            ))
        example = aws.acmpca.CertificateAuthorityCertificate("example",
            certificate_authority_arn=example_certificate_authority.arn,
            certificate=example_certificate.certificate,
            certificate_chain=example_certificate.certificate_chain)
        ```
        <!--End PulumiCodeChooser -->

        ### Certificate for Subordinate Certificate Authority

        Note that the certificate for the subordinate certificate authority must be issued by the root certificate authority using a signing request from the subordinate certificate authority.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        subordinate_certificate_authority = aws.acmpca.CertificateAuthority("subordinate",
            type="SUBORDINATE",
            certificate_authority_configuration=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationArgs(
                key_algorithm="RSA_2048",
                signing_algorithm="SHA512WITHRSA",
                subject=aws.acmpca.CertificateAuthorityCertificateAuthorityConfigurationSubjectArgs(
                    common_name="sub.example.com",
                ),
            ))
        root = aws.acmpca.CertificateAuthority("root")
        current = aws.get_partition()
        subordinate_certificate = aws.acmpca.Certificate("subordinate",
            certificate_authority_arn=root.arn,
            certificate_signing_request=subordinate_certificate_authority.certificate_signing_request,
            signing_algorithm="SHA512WITHRSA",
            template_arn=f"arn:{current.partition}:acm-pca:::template/SubordinateCACertificate_PathLen0/V1",
            validity=aws.acmpca.CertificateValidityArgs(
                type="YEARS",
                value="1",
            ))
        subordinate = aws.acmpca.CertificateAuthorityCertificate("subordinate",
            certificate_authority_arn=subordinate_certificate_authority.arn,
            certificate=subordinate_certificate.certificate,
            certificate_chain=subordinate_certificate.certificate_chain)
        root_certificate_authority_certificate = aws.acmpca.CertificateAuthorityCertificate("root")
        root_certificate = aws.acmpca.Certificate("root")
        ```
        <!--End PulumiCodeChooser -->

        :param str resource_name: The name of the resource.
        :param CertificateAuthorityCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CertificateAuthorityCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateAuthorityCertificateArgs.__new__(CertificateAuthorityCertificateArgs)

            if certificate is None and not opts.urn:
                raise TypeError("Missing required property 'certificate'")
            __props__.__dict__["certificate"] = certificate
            if certificate_authority_arn is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_authority_arn'")
            __props__.__dict__["certificate_authority_arn"] = certificate_authority_arn
            __props__.__dict__["certificate_chain"] = certificate_chain
        super(CertificateAuthorityCertificate, __self__).__init__(
            'aws:acmpca/certificateAuthorityCertificate:CertificateAuthorityCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            certificate: Optional[pulumi.Input[str]] = None,
            certificate_authority_arn: Optional[pulumi.Input[str]] = None,
            certificate_chain: Optional[pulumi.Input[str]] = None) -> 'CertificateAuthorityCertificate':
        """
        Get an existing CertificateAuthorityCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate: PEM-encoded certificate for the Certificate Authority.
        :param pulumi.Input[str] certificate_authority_arn: ARN of the Certificate Authority.
        :param pulumi.Input[str] certificate_chain: PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CertificateAuthorityCertificateState.__new__(_CertificateAuthorityCertificateState)

        __props__.__dict__["certificate"] = certificate
        __props__.__dict__["certificate_authority_arn"] = certificate_authority_arn
        __props__.__dict__["certificate_chain"] = certificate_chain
        return CertificateAuthorityCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output[str]:
        """
        PEM-encoded certificate for the Certificate Authority.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> pulumi.Output[str]:
        """
        ARN of the Certificate Authority.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> pulumi.Output[Optional[str]]:
        """
        PEM-encoded certificate chain that includes any intermediate certificates and chains up to root CA. Required for subordinate Certificate Authorities. Not allowed for root Certificate Authorities.
        """
        return pulumi.get(self, "certificate_chain")

