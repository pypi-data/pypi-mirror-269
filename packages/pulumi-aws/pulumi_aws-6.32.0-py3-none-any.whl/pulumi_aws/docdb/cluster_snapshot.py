# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ClusterSnapshotArgs', 'ClusterSnapshot']

@pulumi.input_type
class ClusterSnapshotArgs:
    def __init__(__self__, *,
                 db_cluster_identifier: pulumi.Input[str],
                 db_cluster_snapshot_identifier: pulumi.Input[str]):
        """
        The set of arguments for constructing a ClusterSnapshot resource.
        :param pulumi.Input[str] db_cluster_identifier: The DocumentDB Cluster Identifier from which to take the snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_identifier: The Identifier for the snapshot.
        """
        pulumi.set(__self__, "db_cluster_identifier", db_cluster_identifier)
        pulumi.set(__self__, "db_cluster_snapshot_identifier", db_cluster_snapshot_identifier)

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> pulumi.Input[str]:
        """
        The DocumentDB Cluster Identifier from which to take the snapshot.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_cluster_identifier", value)

    @property
    @pulumi.getter(name="dbClusterSnapshotIdentifier")
    def db_cluster_snapshot_identifier(self) -> pulumi.Input[str]:
        """
        The Identifier for the snapshot.
        """
        return pulumi.get(self, "db_cluster_snapshot_identifier")

    @db_cluster_snapshot_identifier.setter
    def db_cluster_snapshot_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_cluster_snapshot_identifier", value)


@pulumi.input_type
class _ClusterSnapshotState:
    def __init__(__self__, *,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 db_cluster_snapshot_arn: Optional[pulumi.Input[str]] = None,
                 db_cluster_snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 engine: Optional[pulumi.Input[str]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 snapshot_type: Optional[pulumi.Input[str]] = None,
                 source_db_cluster_snapshot_arn: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 storage_encrypted: Optional[pulumi.Input[bool]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ClusterSnapshot resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] availability_zones: List of EC2 Availability Zones that instances in the DocumentDB cluster snapshot can be restored in.
        :param pulumi.Input[str] db_cluster_identifier: The DocumentDB Cluster Identifier from which to take the snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_arn: The Amazon Resource Name (ARN) for the DocumentDB Cluster Snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_identifier: The Identifier for the snapshot.
        :param pulumi.Input[str] engine: Specifies the name of the database engine.
        :param pulumi.Input[str] engine_version: Version of the database engine for this DocumentDB cluster snapshot.
        :param pulumi.Input[str] kms_key_id: If storage_encrypted is true, the AWS KMS key identifier for the encrypted DocumentDB cluster snapshot.
        :param pulumi.Input[int] port: Port that the DocumentDB cluster was listening on at the time of the snapshot.
        :param pulumi.Input[str] status: The status of this DocumentDB Cluster Snapshot.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the DocumentDB cluster snapshot is encrypted.
        :param pulumi.Input[str] vpc_id: The VPC ID associated with the DocumentDB cluster snapshot.
        """
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if db_cluster_identifier is not None:
            pulumi.set(__self__, "db_cluster_identifier", db_cluster_identifier)
        if db_cluster_snapshot_arn is not None:
            pulumi.set(__self__, "db_cluster_snapshot_arn", db_cluster_snapshot_arn)
        if db_cluster_snapshot_identifier is not None:
            pulumi.set(__self__, "db_cluster_snapshot_identifier", db_cluster_snapshot_identifier)
        if engine is not None:
            pulumi.set(__self__, "engine", engine)
        if engine_version is not None:
            pulumi.set(__self__, "engine_version", engine_version)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if snapshot_type is not None:
            pulumi.set(__self__, "snapshot_type", snapshot_type)
        if source_db_cluster_snapshot_arn is not None:
            pulumi.set(__self__, "source_db_cluster_snapshot_arn", source_db_cluster_snapshot_arn)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if storage_encrypted is not None:
            pulumi.set(__self__, "storage_encrypted", storage_encrypted)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of EC2 Availability Zones that instances in the DocumentDB cluster snapshot can be restored in.
        """
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The DocumentDB Cluster Identifier from which to take the snapshot.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_identifier", value)

    @property
    @pulumi.getter(name="dbClusterSnapshotArn")
    def db_cluster_snapshot_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) for the DocumentDB Cluster Snapshot.
        """
        return pulumi.get(self, "db_cluster_snapshot_arn")

    @db_cluster_snapshot_arn.setter
    def db_cluster_snapshot_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_snapshot_arn", value)

    @property
    @pulumi.getter(name="dbClusterSnapshotIdentifier")
    def db_cluster_snapshot_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The Identifier for the snapshot.
        """
        return pulumi.get(self, "db_cluster_snapshot_identifier")

    @db_cluster_snapshot_identifier.setter
    def db_cluster_snapshot_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_snapshot_identifier", value)

    @property
    @pulumi.getter
    def engine(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the database engine.
        """
        return pulumi.get(self, "engine")

    @engine.setter
    def engine(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engine", value)

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the database engine for this DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "engine_version")

    @engine_version.setter
    def engine_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engine_version", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        If storage_encrypted is true, the AWS KMS key identifier for the encrypted DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        Port that the DocumentDB cluster was listening on at the time of the snapshot.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="snapshotType")
    def snapshot_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "snapshot_type")

    @snapshot_type.setter
    def snapshot_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_type", value)

    @property
    @pulumi.getter(name="sourceDbClusterSnapshotArn")
    def source_db_cluster_snapshot_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_db_cluster_snapshot_arn")

    @source_db_cluster_snapshot_arn.setter
    def source_db_cluster_snapshot_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_db_cluster_snapshot_arn", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of this DocumentDB Cluster Snapshot.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the DocumentDB cluster snapshot is encrypted.
        """
        return pulumi.get(self, "storage_encrypted")

    @storage_encrypted.setter
    def storage_encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "storage_encrypted", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC ID associated with the DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class ClusterSnapshot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 db_cluster_snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a DocumentDB database cluster snapshot for DocumentDB clusters.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.docdb.ClusterSnapshot("example",
            db_cluster_identifier=example_aws_docdb_cluster["id"],
            db_cluster_snapshot_identifier="resourcetestsnapshot1234")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_docdb_cluster_snapshot` using the cluster snapshot identifier. For example:

        ```sh
        $ pulumi import aws:docdb/clusterSnapshot:ClusterSnapshot example my-cluster-snapshot
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_cluster_identifier: The DocumentDB Cluster Identifier from which to take the snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_identifier: The Identifier for the snapshot.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterSnapshotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a DocumentDB database cluster snapshot for DocumentDB clusters.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.docdb.ClusterSnapshot("example",
            db_cluster_identifier=example_aws_docdb_cluster["id"],
            db_cluster_snapshot_identifier="resourcetestsnapshot1234")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import `aws_docdb_cluster_snapshot` using the cluster snapshot identifier. For example:

        ```sh
        $ pulumi import aws:docdb/clusterSnapshot:ClusterSnapshot example my-cluster-snapshot
        ```

        :param str resource_name: The name of the resource.
        :param ClusterSnapshotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterSnapshotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 db_cluster_snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterSnapshotArgs.__new__(ClusterSnapshotArgs)

            if db_cluster_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'db_cluster_identifier'")
            __props__.__dict__["db_cluster_identifier"] = db_cluster_identifier
            if db_cluster_snapshot_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'db_cluster_snapshot_identifier'")
            __props__.__dict__["db_cluster_snapshot_identifier"] = db_cluster_snapshot_identifier
            __props__.__dict__["availability_zones"] = None
            __props__.__dict__["db_cluster_snapshot_arn"] = None
            __props__.__dict__["engine"] = None
            __props__.__dict__["engine_version"] = None
            __props__.__dict__["kms_key_id"] = None
            __props__.__dict__["port"] = None
            __props__.__dict__["snapshot_type"] = None
            __props__.__dict__["source_db_cluster_snapshot_arn"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["storage_encrypted"] = None
            __props__.__dict__["vpc_id"] = None
        super(ClusterSnapshot, __self__).__init__(
            'aws:docdb/clusterSnapshot:ClusterSnapshot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            db_cluster_identifier: Optional[pulumi.Input[str]] = None,
            db_cluster_snapshot_arn: Optional[pulumi.Input[str]] = None,
            db_cluster_snapshot_identifier: Optional[pulumi.Input[str]] = None,
            engine: Optional[pulumi.Input[str]] = None,
            engine_version: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            snapshot_type: Optional[pulumi.Input[str]] = None,
            source_db_cluster_snapshot_arn: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            storage_encrypted: Optional[pulumi.Input[bool]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'ClusterSnapshot':
        """
        Get an existing ClusterSnapshot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] availability_zones: List of EC2 Availability Zones that instances in the DocumentDB cluster snapshot can be restored in.
        :param pulumi.Input[str] db_cluster_identifier: The DocumentDB Cluster Identifier from which to take the snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_arn: The Amazon Resource Name (ARN) for the DocumentDB Cluster Snapshot.
        :param pulumi.Input[str] db_cluster_snapshot_identifier: The Identifier for the snapshot.
        :param pulumi.Input[str] engine: Specifies the name of the database engine.
        :param pulumi.Input[str] engine_version: Version of the database engine for this DocumentDB cluster snapshot.
        :param pulumi.Input[str] kms_key_id: If storage_encrypted is true, the AWS KMS key identifier for the encrypted DocumentDB cluster snapshot.
        :param pulumi.Input[int] port: Port that the DocumentDB cluster was listening on at the time of the snapshot.
        :param pulumi.Input[str] status: The status of this DocumentDB Cluster Snapshot.
        :param pulumi.Input[bool] storage_encrypted: Specifies whether the DocumentDB cluster snapshot is encrypted.
        :param pulumi.Input[str] vpc_id: The VPC ID associated with the DocumentDB cluster snapshot.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterSnapshotState.__new__(_ClusterSnapshotState)

        __props__.__dict__["availability_zones"] = availability_zones
        __props__.__dict__["db_cluster_identifier"] = db_cluster_identifier
        __props__.__dict__["db_cluster_snapshot_arn"] = db_cluster_snapshot_arn
        __props__.__dict__["db_cluster_snapshot_identifier"] = db_cluster_snapshot_identifier
        __props__.__dict__["engine"] = engine
        __props__.__dict__["engine_version"] = engine_version
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["port"] = port
        __props__.__dict__["snapshot_type"] = snapshot_type
        __props__.__dict__["source_db_cluster_snapshot_arn"] = source_db_cluster_snapshot_arn
        __props__.__dict__["status"] = status
        __props__.__dict__["storage_encrypted"] = storage_encrypted
        __props__.__dict__["vpc_id"] = vpc_id
        return ClusterSnapshot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> pulumi.Output[Sequence[str]]:
        """
        List of EC2 Availability Zones that instances in the DocumentDB cluster snapshot can be restored in.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> pulumi.Output[str]:
        """
        The DocumentDB Cluster Identifier from which to take the snapshot.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @property
    @pulumi.getter(name="dbClusterSnapshotArn")
    def db_cluster_snapshot_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) for the DocumentDB Cluster Snapshot.
        """
        return pulumi.get(self, "db_cluster_snapshot_arn")

    @property
    @pulumi.getter(name="dbClusterSnapshotIdentifier")
    def db_cluster_snapshot_identifier(self) -> pulumi.Output[str]:
        """
        The Identifier for the snapshot.
        """
        return pulumi.get(self, "db_cluster_snapshot_identifier")

    @property
    @pulumi.getter
    def engine(self) -> pulumi.Output[str]:
        """
        Specifies the name of the database engine.
        """
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> pulumi.Output[str]:
        """
        Version of the database engine for this DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        If storage_encrypted is true, the AWS KMS key identifier for the encrypted DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        Port that the DocumentDB cluster was listening on at the time of the snapshot.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="snapshotType")
    def snapshot_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "snapshot_type")

    @property
    @pulumi.getter(name="sourceDbClusterSnapshotArn")
    def source_db_cluster_snapshot_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "source_db_cluster_snapshot_arn")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of this DocumentDB Cluster Snapshot.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> pulumi.Output[bool]:
        """
        Specifies whether the DocumentDB cluster snapshot is encrypted.
        """
        return pulumi.get(self, "storage_encrypted")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The VPC ID associated with the DocumentDB cluster snapshot.
        """
        return pulumi.get(self, "vpc_id")

