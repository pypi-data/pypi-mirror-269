# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ReplicationSubnetGroupArgs', 'ReplicationSubnetGroup']

@pulumi.input_type
class ReplicationSubnetGroupArgs:
    def __init__(__self__, *,
                 replication_subnet_group_description: pulumi.Input[str],
                 replication_subnet_group_id: pulumi.Input[str],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ReplicationSubnetGroup resource.
        :param pulumi.Input[str] replication_subnet_group_description: Description for the subnet group.
        :param pulumi.Input[str] replication_subnet_group_id: Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "replication_subnet_group_description", replication_subnet_group_description)
        pulumi.set(__self__, "replication_subnet_group_id", replication_subnet_group_id)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="replicationSubnetGroupDescription")
    def replication_subnet_group_description(self) -> pulumi.Input[str]:
        """
        Description for the subnet group.
        """
        return pulumi.get(self, "replication_subnet_group_description")

    @replication_subnet_group_description.setter
    def replication_subnet_group_description(self, value: pulumi.Input[str]):
        pulumi.set(self, "replication_subnet_group_description", value)

    @property
    @pulumi.getter(name="replicationSubnetGroupId")
    def replication_subnet_group_id(self) -> pulumi.Input[str]:
        """
        Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        """
        return pulumi.get(self, "replication_subnet_group_id")

    @replication_subnet_group_id.setter
    def replication_subnet_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "replication_subnet_group_id", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ReplicationSubnetGroupState:
    def __init__(__self__, *,
                 replication_subnet_group_arn: Optional[pulumi.Input[str]] = None,
                 replication_subnet_group_description: Optional[pulumi.Input[str]] = None,
                 replication_subnet_group_id: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ReplicationSubnetGroup resources.
        :param pulumi.Input[str] replication_subnet_group_description: Description for the subnet group.
        :param pulumi.Input[str] replication_subnet_group_id: Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vpc_id: The ID of the VPC the subnet group is in.
        """
        if replication_subnet_group_arn is not None:
            pulumi.set(__self__, "replication_subnet_group_arn", replication_subnet_group_arn)
        if replication_subnet_group_description is not None:
            pulumi.set(__self__, "replication_subnet_group_description", replication_subnet_group_description)
        if replication_subnet_group_id is not None:
            pulumi.set(__self__, "replication_subnet_group_id", replication_subnet_group_id)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="replicationSubnetGroupArn")
    def replication_subnet_group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "replication_subnet_group_arn")

    @replication_subnet_group_arn.setter
    def replication_subnet_group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replication_subnet_group_arn", value)

    @property
    @pulumi.getter(name="replicationSubnetGroupDescription")
    def replication_subnet_group_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description for the subnet group.
        """
        return pulumi.get(self, "replication_subnet_group_description")

    @replication_subnet_group_description.setter
    def replication_subnet_group_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replication_subnet_group_description", value)

    @property
    @pulumi.getter(name="replicationSubnetGroupId")
    def replication_subnet_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        """
        return pulumi.get(self, "replication_subnet_group_id")

    @replication_subnet_group_id.setter
    def replication_subnet_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replication_subnet_group_id", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC the subnet group is in.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class ReplicationSubnetGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 replication_subnet_group_description: Optional[pulumi.Input[str]] = None,
                 replication_subnet_group_id: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a DMS (Data Migration Service) replication subnet group resource. DMS replication subnet groups can be created, updated, deleted, and imported.

        > **Note:** AWS requires a special IAM role called `dms-vpc-role` when using this resource. See the example below to create it as part of your configuration.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        # Create a new replication subnet group
        example = aws.dms.ReplicationSubnetGroup("example",
            replication_subnet_group_description="Example replication subnet group",
            replication_subnet_group_id="example-dms-replication-subnet-group-tf",
            subnet_ids=[
                "subnet-12345678",
                "subnet-12345679",
            ],
            tags={
                "Name": "example",
            })
        ```
        <!--End PulumiCodeChooser -->

        ### Creating special IAM role

        If your account does not already include the `dms-vpc-role` IAM role, you will need to create it to allow DMS to manage subnets in the VPC.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        dms_vpc_role = aws.iam.Role("dms-vpc-role",
            name="dms-vpc-role",
            description="Allows DMS to manage VPC",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "dms.amazonaws.com",
                    },
                    "Action": "sts:AssumeRole",
                }],
            }))
        example = aws.iam.RolePolicyAttachment("example",
            role=dms_vpc_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole")
        example_replication_subnet_group = aws.dms.ReplicationSubnetGroup("example",
            replication_subnet_group_description="Example",
            replication_subnet_group_id="example-id",
            subnet_ids=[
                "subnet-12345678",
                "subnet-12345679",
            ],
            tags={
                "Name": "example-id",
            },
            opts=pulumi.ResourceOptions(depends_on=[example]))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import replication subnet groups using the `replication_subnet_group_id`. For example:

        ```sh
        $ pulumi import aws:dms/replicationSubnetGroup:ReplicationSubnetGroup test test-dms-replication-subnet-group-tf
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] replication_subnet_group_description: Description for the subnet group.
        :param pulumi.Input[str] replication_subnet_group_id: Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationSubnetGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DMS (Data Migration Service) replication subnet group resource. DMS replication subnet groups can be created, updated, deleted, and imported.

        > **Note:** AWS requires a special IAM role called `dms-vpc-role` when using this resource. See the example below to create it as part of your configuration.

        ## Example Usage

        ### Basic

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        # Create a new replication subnet group
        example = aws.dms.ReplicationSubnetGroup("example",
            replication_subnet_group_description="Example replication subnet group",
            replication_subnet_group_id="example-dms-replication-subnet-group-tf",
            subnet_ids=[
                "subnet-12345678",
                "subnet-12345679",
            ],
            tags={
                "Name": "example",
            })
        ```
        <!--End PulumiCodeChooser -->

        ### Creating special IAM role

        If your account does not already include the `dms-vpc-role` IAM role, you will need to create it to allow DMS to manage subnets in the VPC.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        dms_vpc_role = aws.iam.Role("dms-vpc-role",
            name="dms-vpc-role",
            description="Allows DMS to manage VPC",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "dms.amazonaws.com",
                    },
                    "Action": "sts:AssumeRole",
                }],
            }))
        example = aws.iam.RolePolicyAttachment("example",
            role=dms_vpc_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole")
        example_replication_subnet_group = aws.dms.ReplicationSubnetGroup("example",
            replication_subnet_group_description="Example",
            replication_subnet_group_id="example-id",
            subnet_ids=[
                "subnet-12345678",
                "subnet-12345679",
            ],
            tags={
                "Name": "example-id",
            },
            opts=pulumi.ResourceOptions(depends_on=[example]))
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import replication subnet groups using the `replication_subnet_group_id`. For example:

        ```sh
        $ pulumi import aws:dms/replicationSubnetGroup:ReplicationSubnetGroup test test-dms-replication-subnet-group-tf
        ```

        :param str resource_name: The name of the resource.
        :param ReplicationSubnetGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationSubnetGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 replication_subnet_group_description: Optional[pulumi.Input[str]] = None,
                 replication_subnet_group_id: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationSubnetGroupArgs.__new__(ReplicationSubnetGroupArgs)

            if replication_subnet_group_description is None and not opts.urn:
                raise TypeError("Missing required property 'replication_subnet_group_description'")
            __props__.__dict__["replication_subnet_group_description"] = replication_subnet_group_description
            if replication_subnet_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'replication_subnet_group_id'")
            __props__.__dict__["replication_subnet_group_id"] = replication_subnet_group_id
            if subnet_ids is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_ids'")
            __props__.__dict__["subnet_ids"] = subnet_ids
            __props__.__dict__["tags"] = tags
            __props__.__dict__["replication_subnet_group_arn"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["vpc_id"] = None
        super(ReplicationSubnetGroup, __self__).__init__(
            'aws:dms/replicationSubnetGroup:ReplicationSubnetGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            replication_subnet_group_arn: Optional[pulumi.Input[str]] = None,
            replication_subnet_group_description: Optional[pulumi.Input[str]] = None,
            replication_subnet_group_id: Optional[pulumi.Input[str]] = None,
            subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'ReplicationSubnetGroup':
        """
        Get an existing ReplicationSubnetGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] replication_subnet_group_description: Description for the subnet group.
        :param pulumi.Input[str] replication_subnet_group_id: Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vpc_id: The ID of the VPC the subnet group is in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReplicationSubnetGroupState.__new__(_ReplicationSubnetGroupState)

        __props__.__dict__["replication_subnet_group_arn"] = replication_subnet_group_arn
        __props__.__dict__["replication_subnet_group_description"] = replication_subnet_group_description
        __props__.__dict__["replication_subnet_group_id"] = replication_subnet_group_id
        __props__.__dict__["subnet_ids"] = subnet_ids
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["vpc_id"] = vpc_id
        return ReplicationSubnetGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="replicationSubnetGroupArn")
    def replication_subnet_group_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "replication_subnet_group_arn")

    @property
    @pulumi.getter(name="replicationSubnetGroupDescription")
    def replication_subnet_group_description(self) -> pulumi.Output[str]:
        """
        Description for the subnet group.
        """
        return pulumi.get(self, "replication_subnet_group_description")

    @property
    @pulumi.getter(name="replicationSubnetGroupId")
    def replication_subnet_group_id(self) -> pulumi.Output[str]:
        """
        Name for the replication subnet group. This value is stored as a lowercase string. It must contain no more than 255 alphanumeric characters, periods, spaces, underscores, or hyphens and cannot be `default`.
        """
        return pulumi.get(self, "replication_subnet_group_id")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        List of at least 2 EC2 subnet IDs for the subnet group. The subnets must cover at least 2 availability zones.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPC the subnet group is in.
        """
        return pulumi.get(self, "vpc_id")

