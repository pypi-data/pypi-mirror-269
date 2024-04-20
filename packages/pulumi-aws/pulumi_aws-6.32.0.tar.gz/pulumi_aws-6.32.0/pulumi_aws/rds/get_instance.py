# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetInstanceResult',
    'AwaitableGetInstanceResult',
    'get_instance',
    'get_instance_output',
]

@pulumi.output_type
class GetInstanceResult:
    """
    A collection of values returned by getInstance.
    """
    def __init__(__self__, address=None, allocated_storage=None, auto_minor_version_upgrade=None, availability_zone=None, backup_retention_period=None, ca_cert_identifier=None, db_cluster_identifier=None, db_instance_arn=None, db_instance_class=None, db_instance_identifier=None, db_instance_port=None, db_name=None, db_parameter_groups=None, db_subnet_group=None, enabled_cloudwatch_logs_exports=None, endpoint=None, engine=None, engine_version=None, hosted_zone_id=None, id=None, iops=None, kms_key_id=None, license_model=None, master_user_secrets=None, master_username=None, max_allocated_storage=None, monitoring_interval=None, monitoring_role_arn=None, multi_az=None, network_type=None, option_group_memberships=None, port=None, preferred_backup_window=None, preferred_maintenance_window=None, publicly_accessible=None, replicate_source_db=None, resource_id=None, storage_encrypted=None, storage_throughput=None, storage_type=None, tags=None, timezone=None, vpc_security_groups=None):
        if address and not isinstance(address, str):
            raise TypeError("Expected argument 'address' to be a str")
        pulumi.set(__self__, "address", address)
        if allocated_storage and not isinstance(allocated_storage, int):
            raise TypeError("Expected argument 'allocated_storage' to be a int")
        pulumi.set(__self__, "allocated_storage", allocated_storage)
        if auto_minor_version_upgrade and not isinstance(auto_minor_version_upgrade, bool):
            raise TypeError("Expected argument 'auto_minor_version_upgrade' to be a bool")
        pulumi.set(__self__, "auto_minor_version_upgrade", auto_minor_version_upgrade)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if backup_retention_period and not isinstance(backup_retention_period, int):
            raise TypeError("Expected argument 'backup_retention_period' to be a int")
        pulumi.set(__self__, "backup_retention_period", backup_retention_period)
        if ca_cert_identifier and not isinstance(ca_cert_identifier, str):
            raise TypeError("Expected argument 'ca_cert_identifier' to be a str")
        pulumi.set(__self__, "ca_cert_identifier", ca_cert_identifier)
        if db_cluster_identifier and not isinstance(db_cluster_identifier, str):
            raise TypeError("Expected argument 'db_cluster_identifier' to be a str")
        pulumi.set(__self__, "db_cluster_identifier", db_cluster_identifier)
        if db_instance_arn and not isinstance(db_instance_arn, str):
            raise TypeError("Expected argument 'db_instance_arn' to be a str")
        pulumi.set(__self__, "db_instance_arn", db_instance_arn)
        if db_instance_class and not isinstance(db_instance_class, str):
            raise TypeError("Expected argument 'db_instance_class' to be a str")
        pulumi.set(__self__, "db_instance_class", db_instance_class)
        if db_instance_identifier and not isinstance(db_instance_identifier, str):
            raise TypeError("Expected argument 'db_instance_identifier' to be a str")
        pulumi.set(__self__, "db_instance_identifier", db_instance_identifier)
        if db_instance_port and not isinstance(db_instance_port, int):
            raise TypeError("Expected argument 'db_instance_port' to be a int")
        pulumi.set(__self__, "db_instance_port", db_instance_port)
        if db_name and not isinstance(db_name, str):
            raise TypeError("Expected argument 'db_name' to be a str")
        pulumi.set(__self__, "db_name", db_name)
        if db_parameter_groups and not isinstance(db_parameter_groups, list):
            raise TypeError("Expected argument 'db_parameter_groups' to be a list")
        pulumi.set(__self__, "db_parameter_groups", db_parameter_groups)
        if db_subnet_group and not isinstance(db_subnet_group, str):
            raise TypeError("Expected argument 'db_subnet_group' to be a str")
        pulumi.set(__self__, "db_subnet_group", db_subnet_group)
        if enabled_cloudwatch_logs_exports and not isinstance(enabled_cloudwatch_logs_exports, list):
            raise TypeError("Expected argument 'enabled_cloudwatch_logs_exports' to be a list")
        pulumi.set(__self__, "enabled_cloudwatch_logs_exports", enabled_cloudwatch_logs_exports)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        pulumi.set(__self__, "engine", engine)
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        pulumi.set(__self__, "engine_version", engine_version)
        if hosted_zone_id and not isinstance(hosted_zone_id, str):
            raise TypeError("Expected argument 'hosted_zone_id' to be a str")
        pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if iops and not isinstance(iops, int):
            raise TypeError("Expected argument 'iops' to be a int")
        pulumi.set(__self__, "iops", iops)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if license_model and not isinstance(license_model, str):
            raise TypeError("Expected argument 'license_model' to be a str")
        pulumi.set(__self__, "license_model", license_model)
        if master_user_secrets and not isinstance(master_user_secrets, list):
            raise TypeError("Expected argument 'master_user_secrets' to be a list")
        pulumi.set(__self__, "master_user_secrets", master_user_secrets)
        if master_username and not isinstance(master_username, str):
            raise TypeError("Expected argument 'master_username' to be a str")
        pulumi.set(__self__, "master_username", master_username)
        if max_allocated_storage and not isinstance(max_allocated_storage, int):
            raise TypeError("Expected argument 'max_allocated_storage' to be a int")
        pulumi.set(__self__, "max_allocated_storage", max_allocated_storage)
        if monitoring_interval and not isinstance(monitoring_interval, int):
            raise TypeError("Expected argument 'monitoring_interval' to be a int")
        pulumi.set(__self__, "monitoring_interval", monitoring_interval)
        if monitoring_role_arn and not isinstance(monitoring_role_arn, str):
            raise TypeError("Expected argument 'monitoring_role_arn' to be a str")
        pulumi.set(__self__, "monitoring_role_arn", monitoring_role_arn)
        if multi_az and not isinstance(multi_az, bool):
            raise TypeError("Expected argument 'multi_az' to be a bool")
        pulumi.set(__self__, "multi_az", multi_az)
        if network_type and not isinstance(network_type, str):
            raise TypeError("Expected argument 'network_type' to be a str")
        pulumi.set(__self__, "network_type", network_type)
        if option_group_memberships and not isinstance(option_group_memberships, list):
            raise TypeError("Expected argument 'option_group_memberships' to be a list")
        pulumi.set(__self__, "option_group_memberships", option_group_memberships)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if preferred_backup_window and not isinstance(preferred_backup_window, str):
            raise TypeError("Expected argument 'preferred_backup_window' to be a str")
        pulumi.set(__self__, "preferred_backup_window", preferred_backup_window)
        if preferred_maintenance_window and not isinstance(preferred_maintenance_window, str):
            raise TypeError("Expected argument 'preferred_maintenance_window' to be a str")
        pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if publicly_accessible and not isinstance(publicly_accessible, bool):
            raise TypeError("Expected argument 'publicly_accessible' to be a bool")
        pulumi.set(__self__, "publicly_accessible", publicly_accessible)
        if replicate_source_db and not isinstance(replicate_source_db, str):
            raise TypeError("Expected argument 'replicate_source_db' to be a str")
        pulumi.set(__self__, "replicate_source_db", replicate_source_db)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if storage_encrypted and not isinstance(storage_encrypted, bool):
            raise TypeError("Expected argument 'storage_encrypted' to be a bool")
        pulumi.set(__self__, "storage_encrypted", storage_encrypted)
        if storage_throughput and not isinstance(storage_throughput, int):
            raise TypeError("Expected argument 'storage_throughput' to be a int")
        pulumi.set(__self__, "storage_throughput", storage_throughput)
        if storage_type and not isinstance(storage_type, str):
            raise TypeError("Expected argument 'storage_type' to be a str")
        pulumi.set(__self__, "storage_type", storage_type)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if timezone and not isinstance(timezone, str):
            raise TypeError("Expected argument 'timezone' to be a str")
        pulumi.set(__self__, "timezone", timezone)
        if vpc_security_groups and not isinstance(vpc_security_groups, list):
            raise TypeError("Expected argument 'vpc_security_groups' to be a list")
        pulumi.set(__self__, "vpc_security_groups", vpc_security_groups)

    @property
    @pulumi.getter
    def address(self) -> str:
        """
        Hostname of the RDS instance. See also `endpoint` and `port`.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="allocatedStorage")
    def allocated_storage(self) -> int:
        """
        Allocated storage size specified in gigabytes.
        """
        return pulumi.get(self, "allocated_storage")

    @property
    @pulumi.getter(name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(self) -> bool:
        """
        Indicates that minor version patches are applied automatically.
        """
        return pulumi.get(self, "auto_minor_version_upgrade")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        """
        Name of the Availability Zone the DB instance is located in.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="backupRetentionPeriod")
    def backup_retention_period(self) -> int:
        """
        Specifies the number of days for which automatic DB snapshots are retained.
        """
        return pulumi.get(self, "backup_retention_period")

    @property
    @pulumi.getter(name="caCertIdentifier")
    def ca_cert_identifier(self) -> str:
        """
        Identifier of the CA certificate for the DB instance.
        """
        return pulumi.get(self, "ca_cert_identifier")

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> str:
        """
        If the DB instance is a member of a DB cluster, contains the name of the DB cluster that the DB instance is a member of.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @property
    @pulumi.getter(name="dbInstanceArn")
    def db_instance_arn(self) -> str:
        """
        ARN for the DB instance.
        """
        return pulumi.get(self, "db_instance_arn")

    @property
    @pulumi.getter(name="dbInstanceClass")
    def db_instance_class(self) -> str:
        """
        Contains the name of the compute and memory capacity class of the DB instance.
        """
        return pulumi.get(self, "db_instance_class")

    @property
    @pulumi.getter(name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> str:
        return pulumi.get(self, "db_instance_identifier")

    @property
    @pulumi.getter(name="dbInstancePort")
    def db_instance_port(self) -> int:
        """
        Port that the DB instance listens on.
        """
        return pulumi.get(self, "db_instance_port")

    @property
    @pulumi.getter(name="dbName")
    def db_name(self) -> str:
        """
        Contains the name of the initial database of this instance that was provided at create time, if one was specified when the DB instance was created. This same name is returned for the life of the DB instance.
        """
        return pulumi.get(self, "db_name")

    @property
    @pulumi.getter(name="dbParameterGroups")
    def db_parameter_groups(self) -> Sequence[str]:
        """
        Provides the list of DB parameter groups applied to this DB instance.
        """
        return pulumi.get(self, "db_parameter_groups")

    @property
    @pulumi.getter(name="dbSubnetGroup")
    def db_subnet_group(self) -> str:
        """
        Name of the subnet group associated with the DB instance.
        """
        return pulumi.get(self, "db_subnet_group")

    @property
    @pulumi.getter(name="enabledCloudwatchLogsExports")
    def enabled_cloudwatch_logs_exports(self) -> Sequence[str]:
        """
        List of log types to export to cloudwatch.
        """
        return pulumi.get(self, "enabled_cloudwatch_logs_exports")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        Connection endpoint in `address:port` format.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def engine(self) -> str:
        """
        Provides the name of the database engine to be used for this DB instance.
        """
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> str:
        """
        Database engine version.
        """
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """
        Canonical hosted zone ID of the DB instance (to be used in a Route 53 Alias record).
        """
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def iops(self) -> int:
        """
        Provisioned IOPS (I/O operations per second) value.
        """
        return pulumi.get(self, "iops")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        The Amazon Web Services KMS key identifier that is used to encrypt the secret.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="licenseModel")
    def license_model(self) -> str:
        """
        License model information for this DB instance.
        """
        return pulumi.get(self, "license_model")

    @property
    @pulumi.getter(name="masterUserSecrets")
    def master_user_secrets(self) -> Sequence['outputs.GetInstanceMasterUserSecretResult']:
        """
        Provides the master user secret. Only available when `manage_master_user_password` is set to true. Documented below.
        """
        return pulumi.get(self, "master_user_secrets")

    @property
    @pulumi.getter(name="masterUsername")
    def master_username(self) -> str:
        """
        Contains the master username for the DB instance.
        """
        return pulumi.get(self, "master_username")

    @property
    @pulumi.getter(name="maxAllocatedStorage")
    def max_allocated_storage(self) -> int:
        """
        The upper limit to which Amazon RDS can automatically scale the storage of the DB instance.
        """
        return pulumi.get(self, "max_allocated_storage")

    @property
    @pulumi.getter(name="monitoringInterval")
    def monitoring_interval(self) -> int:
        """
        Interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance.
        """
        return pulumi.get(self, "monitoring_interval")

    @property
    @pulumi.getter(name="monitoringRoleArn")
    def monitoring_role_arn(self) -> str:
        """
        ARN for the IAM role that permits RDS to send Enhanced Monitoring metrics to CloudWatch Logs.
        """
        return pulumi.get(self, "monitoring_role_arn")

    @property
    @pulumi.getter(name="multiAz")
    def multi_az(self) -> bool:
        """
        If the DB instance is a Multi-AZ deployment.
        """
        return pulumi.get(self, "multi_az")

    @property
    @pulumi.getter(name="networkType")
    def network_type(self) -> str:
        """
        Network type of the DB instance.
        """
        return pulumi.get(self, "network_type")

    @property
    @pulumi.getter(name="optionGroupMemberships")
    def option_group_memberships(self) -> Sequence[str]:
        """
        Provides the list of option group memberships for this DB instance.
        """
        return pulumi.get(self, "option_group_memberships")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        Database endpoint port, primarily used by an Aurora DB cluster. For a conventional RDS DB instance, the `db_instance_port` is typically the preferred choice.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="preferredBackupWindow")
    def preferred_backup_window(self) -> str:
        """
        Specifies the daily time range during which automated backups are created.
        """
        return pulumi.get(self, "preferred_backup_window")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> str:
        """
        Specifies the weekly time range during which system maintenance can occur in UTC.
        """
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="publiclyAccessible")
    def publicly_accessible(self) -> bool:
        """
        Accessibility options for the DB instance.
        """
        return pulumi.get(self, "publicly_accessible")

    @property
    @pulumi.getter(name="replicateSourceDb")
    def replicate_source_db(self) -> str:
        """
        Identifier of the source DB that this is a replica of.
        """
        return pulumi.get(self, "replicate_source_db")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        RDS Resource ID of this instance.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> bool:
        """
        Whether the DB instance is encrypted.
        """
        return pulumi.get(self, "storage_encrypted")

    @property
    @pulumi.getter(name="storageThroughput")
    def storage_throughput(self) -> int:
        """
        Storage throughput value for the DB instance.
        """
        return pulumi.get(self, "storage_throughput")

    @property
    @pulumi.getter(name="storageType")
    def storage_type(self) -> str:
        """
        Storage type associated with DB instance.
        """
        return pulumi.get(self, "storage_type")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timezone(self) -> str:
        """
        Time zone of the DB instance.
        """
        return pulumi.get(self, "timezone")

    @property
    @pulumi.getter(name="vpcSecurityGroups")
    def vpc_security_groups(self) -> Sequence[str]:
        """
        Provides a list of VPC security group elements that the DB instance belongs to.
        """
        return pulumi.get(self, "vpc_security_groups")


class AwaitableGetInstanceResult(GetInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceResult(
            address=self.address,
            allocated_storage=self.allocated_storage,
            auto_minor_version_upgrade=self.auto_minor_version_upgrade,
            availability_zone=self.availability_zone,
            backup_retention_period=self.backup_retention_period,
            ca_cert_identifier=self.ca_cert_identifier,
            db_cluster_identifier=self.db_cluster_identifier,
            db_instance_arn=self.db_instance_arn,
            db_instance_class=self.db_instance_class,
            db_instance_identifier=self.db_instance_identifier,
            db_instance_port=self.db_instance_port,
            db_name=self.db_name,
            db_parameter_groups=self.db_parameter_groups,
            db_subnet_group=self.db_subnet_group,
            enabled_cloudwatch_logs_exports=self.enabled_cloudwatch_logs_exports,
            endpoint=self.endpoint,
            engine=self.engine,
            engine_version=self.engine_version,
            hosted_zone_id=self.hosted_zone_id,
            id=self.id,
            iops=self.iops,
            kms_key_id=self.kms_key_id,
            license_model=self.license_model,
            master_user_secrets=self.master_user_secrets,
            master_username=self.master_username,
            max_allocated_storage=self.max_allocated_storage,
            monitoring_interval=self.monitoring_interval,
            monitoring_role_arn=self.monitoring_role_arn,
            multi_az=self.multi_az,
            network_type=self.network_type,
            option_group_memberships=self.option_group_memberships,
            port=self.port,
            preferred_backup_window=self.preferred_backup_window,
            preferred_maintenance_window=self.preferred_maintenance_window,
            publicly_accessible=self.publicly_accessible,
            replicate_source_db=self.replicate_source_db,
            resource_id=self.resource_id,
            storage_encrypted=self.storage_encrypted,
            storage_throughput=self.storage_throughput,
            storage_type=self.storage_type,
            tags=self.tags,
            timezone=self.timezone,
            vpc_security_groups=self.vpc_security_groups)


def get_instance(db_instance_identifier: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceResult:
    """
    Use this data source to get information about an RDS instance

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    database = aws.rds.get_instance(db_instance_identifier="my-test-database")
    ```
    <!--End PulumiCodeChooser -->


    :param str db_instance_identifier: Name of the RDS instance.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired instance.
    """
    __args__ = dict()
    __args__['dbInstanceIdentifier'] = db_instance_identifier
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:rds/getInstance:getInstance', __args__, opts=opts, typ=GetInstanceResult).value

    return AwaitableGetInstanceResult(
        address=pulumi.get(__ret__, 'address'),
        allocated_storage=pulumi.get(__ret__, 'allocated_storage'),
        auto_minor_version_upgrade=pulumi.get(__ret__, 'auto_minor_version_upgrade'),
        availability_zone=pulumi.get(__ret__, 'availability_zone'),
        backup_retention_period=pulumi.get(__ret__, 'backup_retention_period'),
        ca_cert_identifier=pulumi.get(__ret__, 'ca_cert_identifier'),
        db_cluster_identifier=pulumi.get(__ret__, 'db_cluster_identifier'),
        db_instance_arn=pulumi.get(__ret__, 'db_instance_arn'),
        db_instance_class=pulumi.get(__ret__, 'db_instance_class'),
        db_instance_identifier=pulumi.get(__ret__, 'db_instance_identifier'),
        db_instance_port=pulumi.get(__ret__, 'db_instance_port'),
        db_name=pulumi.get(__ret__, 'db_name'),
        db_parameter_groups=pulumi.get(__ret__, 'db_parameter_groups'),
        db_subnet_group=pulumi.get(__ret__, 'db_subnet_group'),
        enabled_cloudwatch_logs_exports=pulumi.get(__ret__, 'enabled_cloudwatch_logs_exports'),
        endpoint=pulumi.get(__ret__, 'endpoint'),
        engine=pulumi.get(__ret__, 'engine'),
        engine_version=pulumi.get(__ret__, 'engine_version'),
        hosted_zone_id=pulumi.get(__ret__, 'hosted_zone_id'),
        id=pulumi.get(__ret__, 'id'),
        iops=pulumi.get(__ret__, 'iops'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        license_model=pulumi.get(__ret__, 'license_model'),
        master_user_secrets=pulumi.get(__ret__, 'master_user_secrets'),
        master_username=pulumi.get(__ret__, 'master_username'),
        max_allocated_storage=pulumi.get(__ret__, 'max_allocated_storage'),
        monitoring_interval=pulumi.get(__ret__, 'monitoring_interval'),
        monitoring_role_arn=pulumi.get(__ret__, 'monitoring_role_arn'),
        multi_az=pulumi.get(__ret__, 'multi_az'),
        network_type=pulumi.get(__ret__, 'network_type'),
        option_group_memberships=pulumi.get(__ret__, 'option_group_memberships'),
        port=pulumi.get(__ret__, 'port'),
        preferred_backup_window=pulumi.get(__ret__, 'preferred_backup_window'),
        preferred_maintenance_window=pulumi.get(__ret__, 'preferred_maintenance_window'),
        publicly_accessible=pulumi.get(__ret__, 'publicly_accessible'),
        replicate_source_db=pulumi.get(__ret__, 'replicate_source_db'),
        resource_id=pulumi.get(__ret__, 'resource_id'),
        storage_encrypted=pulumi.get(__ret__, 'storage_encrypted'),
        storage_throughput=pulumi.get(__ret__, 'storage_throughput'),
        storage_type=pulumi.get(__ret__, 'storage_type'),
        tags=pulumi.get(__ret__, 'tags'),
        timezone=pulumi.get(__ret__, 'timezone'),
        vpc_security_groups=pulumi.get(__ret__, 'vpc_security_groups'))


@_utilities.lift_output_func(get_instance)
def get_instance_output(db_instance_identifier: Optional[pulumi.Input[Optional[str]]] = None,
                        tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceResult]:
    """
    Use this data source to get information about an RDS instance

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    database = aws.rds.get_instance(db_instance_identifier="my-test-database")
    ```
    <!--End PulumiCodeChooser -->


    :param str db_instance_identifier: Name of the RDS instance.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired instance.
    """
    ...
