# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ClusterIamRolesArgs', 'ClusterIamRoles']

@pulumi.input_type
class ClusterIamRolesArgs:
    def __init__(__self__, *,
                 cluster_identifier: pulumi.Input[str],
                 default_iam_role_arn: Optional[pulumi.Input[str]] = None,
                 iam_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ClusterIamRoles resource.
        :param pulumi.Input[str] cluster_identifier: The name of the Redshift Cluster IAM Roles.
        :param pulumi.Input[str] default_iam_role_arn: The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] iam_role_arns: A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        if default_iam_role_arn is not None:
            pulumi.set(__self__, "default_iam_role_arn", default_iam_role_arn)
        if iam_role_arns is not None:
            pulumi.set(__self__, "iam_role_arns", iam_role_arns)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> pulumi.Input[str]:
        """
        The name of the Redshift Cluster IAM Roles.
        """
        return pulumi.get(self, "cluster_identifier")

    @cluster_identifier.setter
    def cluster_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_identifier", value)

    @property
    @pulumi.getter(name="defaultIamRoleArn")
    def default_iam_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        """
        return pulumi.get(self, "default_iam_role_arn")

    @default_iam_role_arn.setter
    def default_iam_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_iam_role_arn", value)

    @property
    @pulumi.getter(name="iamRoleArns")
    def iam_role_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        return pulumi.get(self, "iam_role_arns")

    @iam_role_arns.setter
    def iam_role_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "iam_role_arns", value)


@pulumi.input_type
class _ClusterIamRolesState:
    def __init__(__self__, *,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 default_iam_role_arn: Optional[pulumi.Input[str]] = None,
                 iam_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ClusterIamRoles resources.
        :param pulumi.Input[str] cluster_identifier: The name of the Redshift Cluster IAM Roles.
        :param pulumi.Input[str] default_iam_role_arn: The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] iam_role_arns: A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        if cluster_identifier is not None:
            pulumi.set(__self__, "cluster_identifier", cluster_identifier)
        if default_iam_role_arn is not None:
            pulumi.set(__self__, "default_iam_role_arn", default_iam_role_arn)
        if iam_role_arns is not None:
            pulumi.set(__self__, "iam_role_arns", iam_role_arns)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Redshift Cluster IAM Roles.
        """
        return pulumi.get(self, "cluster_identifier")

    @cluster_identifier.setter
    def cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_identifier", value)

    @property
    @pulumi.getter(name="defaultIamRoleArn")
    def default_iam_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        """
        return pulumi.get(self, "default_iam_role_arn")

    @default_iam_role_arn.setter
    def default_iam_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_iam_role_arn", value)

    @property
    @pulumi.getter(name="iamRoleArns")
    def iam_role_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        return pulumi.get(self, "iam_role_arns")

    @iam_role_arns.setter
    def iam_role_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "iam_role_arns", value)


class ClusterIamRoles(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 default_iam_role_arn: Optional[pulumi.Input[str]] = None,
                 iam_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Redshift Cluster IAM Roles resource.

        > **NOTE:** A Redshift cluster's default IAM role can be managed both by this resource's `default_iam_role_arn` argument and the `redshift.Cluster` resource's `default_iam_role_arn` argument. Do not configure different values for both arguments. Doing so will cause a conflict of default IAM roles.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshift.ClusterIamRoles("example",
            cluster_identifier=example_aws_redshift_cluster["clusterIdentifier"],
            iam_role_arns=[example_aws_iam_role["arn"]])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Redshift Cluster IAM Roless using the `cluster_identifier`. For example:

        ```sh
        $ pulumi import aws:redshift/clusterIamRoles:ClusterIamRoles examplegroup1 example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_identifier: The name of the Redshift Cluster IAM Roles.
        :param pulumi.Input[str] default_iam_role_arn: The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] iam_role_arns: A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterIamRolesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Redshift Cluster IAM Roles resource.

        > **NOTE:** A Redshift cluster's default IAM role can be managed both by this resource's `default_iam_role_arn` argument and the `redshift.Cluster` resource's `default_iam_role_arn` argument. Do not configure different values for both arguments. Doing so will cause a conflict of default IAM roles.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.redshift.ClusterIamRoles("example",
            cluster_identifier=example_aws_redshift_cluster["clusterIdentifier"],
            iam_role_arns=[example_aws_iam_role["arn"]])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Redshift Cluster IAM Roless using the `cluster_identifier`. For example:

        ```sh
        $ pulumi import aws:redshift/clusterIamRoles:ClusterIamRoles examplegroup1 example
        ```

        :param str resource_name: The name of the resource.
        :param ClusterIamRolesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterIamRolesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_identifier: Optional[pulumi.Input[str]] = None,
                 default_iam_role_arn: Optional[pulumi.Input[str]] = None,
                 iam_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterIamRolesArgs.__new__(ClusterIamRolesArgs)

            if cluster_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_identifier'")
            __props__.__dict__["cluster_identifier"] = cluster_identifier
            __props__.__dict__["default_iam_role_arn"] = default_iam_role_arn
            __props__.__dict__["iam_role_arns"] = iam_role_arns
        super(ClusterIamRoles, __self__).__init__(
            'aws:redshift/clusterIamRoles:ClusterIamRoles',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_identifier: Optional[pulumi.Input[str]] = None,
            default_iam_role_arn: Optional[pulumi.Input[str]] = None,
            iam_role_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'ClusterIamRoles':
        """
        Get an existing ClusterIamRoles resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_identifier: The name of the Redshift Cluster IAM Roles.
        :param pulumi.Input[str] default_iam_role_arn: The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] iam_role_arns: A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterIamRolesState.__new__(_ClusterIamRolesState)

        __props__.__dict__["cluster_identifier"] = cluster_identifier
        __props__.__dict__["default_iam_role_arn"] = default_iam_role_arn
        __props__.__dict__["iam_role_arns"] = iam_role_arns
        return ClusterIamRoles(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterIdentifier")
    def cluster_identifier(self) -> pulumi.Output[str]:
        """
        The name of the Redshift Cluster IAM Roles.
        """
        return pulumi.get(self, "cluster_identifier")

    @property
    @pulumi.getter(name="defaultIamRoleArn")
    def default_iam_role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the IAM role that was set as default for the cluster when the cluster was created.
        """
        return pulumi.get(self, "default_iam_role_arn")

    @property
    @pulumi.getter(name="iamRoleArns")
    def iam_role_arns(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of IAM Role ARNs to associate with the cluster. A Maximum of 10 can be associated to the cluster at any time.
        """
        return pulumi.get(self, "iam_role_arns")

