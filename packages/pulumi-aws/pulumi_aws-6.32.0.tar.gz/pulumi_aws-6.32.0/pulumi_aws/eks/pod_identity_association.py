# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PodIdentityAssociationArgs', 'PodIdentityAssociation']

@pulumi.input_type
class PodIdentityAssociationArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 namespace: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 service_account: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a PodIdentityAssociation resource.
        :param pulumi.Input[str] cluster_name: The name of the cluster to create the association in.
        :param pulumi.Input[str] namespace: The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        :param pulumi.Input[str] service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "namespace", namespace)
        pulumi.set(__self__, "role_arn", role_arn)
        pulumi.set(__self__, "service_account", service_account)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the cluster to create the association in.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Input[str]:
        """
        The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Input[str]:
        """
        The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

        The following arguments are optional:
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _PodIdentityAssociationState:
    def __init__(__self__, *,
                 association_arn: Optional[pulumi.Input[str]] = None,
                 association_id: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering PodIdentityAssociation resources.
        :param pulumi.Input[str] association_arn: The Amazon Resource Name (ARN) of the association.
        :param pulumi.Input[str] association_id: The ID of the association.
        :param pulumi.Input[str] cluster_name: The name of the cluster to create the association in.
        :param pulumi.Input[str] namespace: The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        :param pulumi.Input[str] service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if association_arn is not None:
            pulumi.set(__self__, "association_arn", association_arn)
        if association_id is not None:
            pulumi.set(__self__, "association_id", association_id)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="associationArn")
    def association_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the association.
        """
        return pulumi.get(self, "association_arn")

    @association_arn.setter
    def association_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "association_arn", value)

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the association.
        """
        return pulumi.get(self, "association_id")

    @association_id.setter
    def association_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "association_id", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cluster to create the association in.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

        The following arguments are optional:
        """
        return pulumi.get(self, "service_account")

    @service_account.setter
    def service_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_account", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class PodIdentityAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS EKS (Elastic Kubernetes) Pod Identity Association.

        Creates an EKS Pod Identity association between a service account in an Amazon EKS cluster and an IAM role with EKS Pod Identity. Use EKS Pod Identity to give temporary IAM credentials to pods and the credentials are rotated automatically.

        Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to Amazon EC2 instances.

        If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod. The environment variables configure the Amazon Web Services SDKs, including the Command Line Interface, to use the EKS Pod Identity credentials.

        Pod Identity is a simpler method than IAM roles for service accounts, as this method doesn’t use OIDC identity providers. Additionally, you can configure a role for Pod Identity once, and reuse it across clusters.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["pods.eks.amazonaws.com"],
            )],
            actions=[
                "sts:AssumeRole",
                "sts:TagSession",
            ],
        )])
        example = aws.iam.Role("example",
            name="eks-pod-identity-example",
            assume_role_policy=assume_role.json)
        example_s3 = aws.iam.RolePolicyAttachment("example_s3",
            policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
            role=example.name)
        example_pod_identity_association = aws.eks.PodIdentityAssociation("example",
            cluster_name=example_aws_eks_cluster["name"],
            namespace="example",
            service_account="example-sa",
            role_arn=example.arn)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import EKS (Elastic Kubernetes) Pod Identity Association using the `cluster_name` and `association_id` separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:eks/podIdentityAssociation:PodIdentityAssociation example example,a-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the cluster to create the association in.
        :param pulumi.Input[str] namespace: The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        :param pulumi.Input[str] service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PodIdentityAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS EKS (Elastic Kubernetes) Pod Identity Association.

        Creates an EKS Pod Identity association between a service account in an Amazon EKS cluster and an IAM role with EKS Pod Identity. Use EKS Pod Identity to give temporary IAM credentials to pods and the credentials are rotated automatically.

        Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that EC2 instance profiles provide credentials to Amazon EC2 instances.

        If a pod uses a service account that has an association, Amazon EKS sets environment variables in the containers of the pod. The environment variables configure the Amazon Web Services SDKs, including the Command Line Interface, to use the EKS Pod Identity credentials.

        Pod Identity is a simpler method than IAM roles for service accounts, as this method doesn’t use OIDC identity providers. Additionally, you can configure a role for Pod Identity once, and reuse it across clusters.

        ## Example Usage

        ### Basic Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["pods.eks.amazonaws.com"],
            )],
            actions=[
                "sts:AssumeRole",
                "sts:TagSession",
            ],
        )])
        example = aws.iam.Role("example",
            name="eks-pod-identity-example",
            assume_role_policy=assume_role.json)
        example_s3 = aws.iam.RolePolicyAttachment("example_s3",
            policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
            role=example.name)
        example_pod_identity_association = aws.eks.PodIdentityAssociation("example",
            cluster_name=example_aws_eks_cluster["name"],
            namespace="example",
            service_account="example-sa",
            role_arn=example.arn)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import EKS (Elastic Kubernetes) Pod Identity Association using the `cluster_name` and `association_id` separated by a comma (`,`). For example:

        ```sh
        $ pulumi import aws:eks/podIdentityAssociation:PodIdentityAssociation example example,a-12345678
        ```

        :param str resource_name: The name of the resource.
        :param PodIdentityAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PodIdentityAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 service_account: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PodIdentityAssociationArgs.__new__(PodIdentityAssociationArgs)

            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            if namespace is None and not opts.urn:
                raise TypeError("Missing required property 'namespace'")
            __props__.__dict__["namespace"] = namespace
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            if service_account is None and not opts.urn:
                raise TypeError("Missing required property 'service_account'")
            __props__.__dict__["service_account"] = service_account
            __props__.__dict__["tags"] = tags
            __props__.__dict__["association_arn"] = None
            __props__.__dict__["association_id"] = None
            __props__.__dict__["tags_all"] = None
        super(PodIdentityAssociation, __self__).__init__(
            'aws:eks/podIdentityAssociation:PodIdentityAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            association_arn: Optional[pulumi.Input[str]] = None,
            association_id: Optional[pulumi.Input[str]] = None,
            cluster_name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            service_account: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'PodIdentityAssociation':
        """
        Get an existing PodIdentityAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] association_arn: The Amazon Resource Name (ARN) of the association.
        :param pulumi.Input[str] association_id: The ID of the association.
        :param pulumi.Input[str] cluster_name: The name of the cluster to create the association in.
        :param pulumi.Input[str] namespace: The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        :param pulumi.Input[str] service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PodIdentityAssociationState.__new__(_PodIdentityAssociationState)

        __props__.__dict__["association_arn"] = association_arn
        __props__.__dict__["association_id"] = association_id
        __props__.__dict__["cluster_name"] = cluster_name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["role_arn"] = role_arn
        __props__.__dict__["service_account"] = service_account
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return PodIdentityAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associationArn")
    def association_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the association.
        """
        return pulumi.get(self, "association_arn")

    @property
    @pulumi.getter(name="associationId")
    def association_id(self) -> pulumi.Output[str]:
        """
        The ID of the association.
        """
        return pulumi.get(self, "association_id")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[str]:
        """
        The name of the cluster to create the association in.
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[str]:
        """
        The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the pods that use the service account must be in this namespace.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the pods that use this service account.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> pulumi.Output[str]:
        """
        The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

        The following arguments are optional:
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

