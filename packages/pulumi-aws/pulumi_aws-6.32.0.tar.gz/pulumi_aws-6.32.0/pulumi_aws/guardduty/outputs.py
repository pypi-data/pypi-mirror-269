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
    'DetectorDatasources',
    'DetectorDatasourcesKubernetes',
    'DetectorDatasourcesKubernetesAuditLogs',
    'DetectorDatasourcesMalwareProtection',
    'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings',
    'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes',
    'DetectorDatasourcesS3Logs',
    'DetectorFeatureAdditionalConfiguration',
    'FilterFindingCriteria',
    'FilterFindingCriteriaCriterion',
    'OrganizationConfigurationDatasources',
    'OrganizationConfigurationDatasourcesKubernetes',
    'OrganizationConfigurationDatasourcesKubernetesAuditLogs',
    'OrganizationConfigurationDatasourcesMalwareProtection',
    'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings',
    'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes',
    'OrganizationConfigurationDatasourcesS3Logs',
    'OrganizationConfigurationFeatureAdditionalConfiguration',
    'GetDetectorFeatureResult',
    'GetDetectorFeatureAdditionalConfigurationResult',
]

@pulumi.output_type
class DetectorDatasources(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "malwareProtection":
            suggest = "malware_protection"
        elif key == "s3Logs":
            suggest = "s3_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorDatasources. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorDatasources.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorDatasources.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kubernetes: Optional['outputs.DetectorDatasourcesKubernetes'] = None,
                 malware_protection: Optional['outputs.DetectorDatasourcesMalwareProtection'] = None,
                 s3_logs: Optional['outputs.DetectorDatasourcesS3Logs'] = None):
        """
        :param 'DetectorDatasourcesKubernetesArgs' kubernetes: Configures [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes and Kubernetes Audit Logs below for more details.
        :param 'DetectorDatasourcesMalwareProtectionArgs' malware_protection: Configures [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html).
               See Malware Protection, Scan EC2 instance with findings and EBS volumes below for more details.
               
               The `datasources` block is deprecated since March 2023. Use the `features` block instead and [map each `datasources` block to the corresponding `features` block](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-feature-object-api-changes-march2023.html#guardduty-feature-enablement-datasource-relation).
        :param 'DetectorDatasourcesS3LogsArgs' s3_logs: Configures [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
               See S3 Logs below for more details.
        """
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional['outputs.DetectorDatasourcesKubernetes']:
        """
        Configures [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes and Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "kubernetes")

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional['outputs.DetectorDatasourcesMalwareProtection']:
        """
        Configures [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html).
        See Malware Protection, Scan EC2 instance with findings and EBS volumes below for more details.

        The `datasources` block is deprecated since March 2023. Use the `features` block instead and [map each `datasources` block to the corresponding `features` block](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-feature-object-api-changes-march2023.html#guardduty-feature-enablement-datasource-relation).
        """
        return pulumi.get(self, "malware_protection")

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional['outputs.DetectorDatasourcesS3Logs']:
        """
        Configures [S3 protection](https://docs.aws.amazon.com/guardduty/latest/ug/s3-protection.html).
        See S3 Logs below for more details.
        """
        return pulumi.get(self, "s3_logs")


@pulumi.output_type
class DetectorDatasourcesKubernetes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "auditLogs":
            suggest = "audit_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorDatasourcesKubernetes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorDatasourcesKubernetes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorDatasourcesKubernetes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 audit_logs: 'outputs.DetectorDatasourcesKubernetesAuditLogs'):
        """
        :param 'DetectorDatasourcesKubernetesAuditLogsArgs' audit_logs: Configures Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes Audit Logs below for more details.
        """
        pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> 'outputs.DetectorDatasourcesKubernetesAuditLogs':
        """
        Configures Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "audit_logs")


@pulumi.output_type
class DetectorDatasourcesKubernetesAuditLogs(dict):
    def __init__(__self__, *,
                 enable: bool):
        """
        :param bool enable: If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> bool:
        """
        If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")


@pulumi.output_type
class DetectorDatasourcesMalwareProtection(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "scanEc2InstanceWithFindings":
            suggest = "scan_ec2_instance_with_findings"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorDatasourcesMalwareProtection. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorDatasourcesMalwareProtection.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorDatasourcesMalwareProtection.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: 'outputs.DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings'):
        """
        :param 'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs' scan_ec2_instance_with_findings: Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) is enabled as data source for EC2 instances with findings for the detector.
               See Scan EC2 instance with findings below for more details.
        """
        pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> 'outputs.DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings':
        """
        Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) is enabled as data source for EC2 instances with findings for the detector.
        See Scan EC2 instance with findings below for more details.
        """
        return pulumi.get(self, "scan_ec2_instance_with_findings")


@pulumi.output_type
class DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ebsVolumes":
            suggest = "ebs_volumes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ebs_volumes: 'outputs.DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes'):
        """
        :param 'DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs' ebs_volumes: Configure whether scanning EBS volumes is enabled as data source for the detector for instances with findings.
               See EBS volumes below for more details.
        """
        pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> 'outputs.DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes':
        """
        Configure whether scanning EBS volumes is enabled as data source for the detector for instances with findings.
        See EBS volumes below for more details.
        """
        return pulumi.get(self, "ebs_volumes")


@pulumi.output_type
class DetectorDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes(dict):
    def __init__(__self__, *,
                 enable: bool):
        """
        :param bool enable: If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) as data source for the detector.
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> bool:
        """
        If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) as data source for the detector.
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")


@pulumi.output_type
class DetectorDatasourcesS3Logs(dict):
    def __init__(__self__, *,
                 enable: bool):
        """
        :param bool enable: Enable monitoring and feedback reporting. Setting to `false` is equivalent to "suspending" GuardDuty. Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> bool:
        """
        Enable monitoring and feedback reporting. Setting to `false` is equivalent to "suspending" GuardDuty. Defaults to `true`.
        """
        return pulumi.get(self, "enable")


@pulumi.output_type
class DetectorFeatureAdditionalConfiguration(dict):
    def __init__(__self__, *,
                 name: str,
                 status: str):
        """
        :param str name: The name of the additional configuration. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        :param str status: The status of the additional configuration. Valid values: `ENABLED`, `DISABLED`.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the additional configuration. Refer to the [AWS Documentation](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_DetectorAdditionalConfiguration.html) for the current list of supported values.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the additional configuration. Valid values: `ENABLED`, `DISABLED`.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class FilterFindingCriteria(dict):
    def __init__(__self__, *,
                 criterions: Sequence['outputs.FilterFindingCriteriaCriterion']):
        pulumi.set(__self__, "criterions", criterions)

    @property
    @pulumi.getter
    def criterions(self) -> Sequence['outputs.FilterFindingCriteriaCriterion']:
        return pulumi.get(self, "criterions")


@pulumi.output_type
class FilterFindingCriteriaCriterion(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "greaterThan":
            suggest = "greater_than"
        elif key == "greaterThanOrEqual":
            suggest = "greater_than_or_equal"
        elif key == "lessThan":
            suggest = "less_than"
        elif key == "lessThanOrEqual":
            suggest = "less_than_or_equal"
        elif key == "notEquals":
            suggest = "not_equals"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FilterFindingCriteriaCriterion. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FilterFindingCriteriaCriterion.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FilterFindingCriteriaCriterion.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field: str,
                 equals: Optional[Sequence[str]] = None,
                 greater_than: Optional[str] = None,
                 greater_than_or_equal: Optional[str] = None,
                 less_than: Optional[str] = None,
                 less_than_or_equal: Optional[str] = None,
                 not_equals: Optional[Sequence[str]] = None):
        """
        :param str field: The name of the field to be evaluated. The full list of field names can be found in [AWS documentation](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria).
        :param Sequence[str] equals: List of string values to be evaluated.
        :param str greater_than: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param str greater_than_or_equal: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param str less_than: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param str less_than_or_equal: A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        :param Sequence[str] not_equals: List of string values to be evaluated.
        """
        pulumi.set(__self__, "field", field)
        if equals is not None:
            pulumi.set(__self__, "equals", equals)
        if greater_than is not None:
            pulumi.set(__self__, "greater_than", greater_than)
        if greater_than_or_equal is not None:
            pulumi.set(__self__, "greater_than_or_equal", greater_than_or_equal)
        if less_than is not None:
            pulumi.set(__self__, "less_than", less_than)
        if less_than_or_equal is not None:
            pulumi.set(__self__, "less_than_or_equal", less_than_or_equal)
        if not_equals is not None:
            pulumi.set(__self__, "not_equals", not_equals)

    @property
    @pulumi.getter
    def field(self) -> str:
        """
        The name of the field to be evaluated. The full list of field names can be found in [AWS documentation](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html#filter_criteria).
        """
        return pulumi.get(self, "field")

    @property
    @pulumi.getter
    def equals(self) -> Optional[Sequence[str]]:
        """
        List of string values to be evaluated.
        """
        return pulumi.get(self, "equals")

    @property
    @pulumi.getter(name="greaterThan")
    def greater_than(self) -> Optional[str]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "greater_than")

    @property
    @pulumi.getter(name="greaterThanOrEqual")
    def greater_than_or_equal(self) -> Optional[str]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "greater_than_or_equal")

    @property
    @pulumi.getter(name="lessThan")
    def less_than(self) -> Optional[str]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "less_than")

    @property
    @pulumi.getter(name="lessThanOrEqual")
    def less_than_or_equal(self) -> Optional[str]:
        """
        A value to be evaluated. Accepts either an integer or a date in [RFC 3339 format](https://tools.ietf.org/html/rfc3339#section-5.8).
        """
        return pulumi.get(self, "less_than_or_equal")

    @property
    @pulumi.getter(name="notEquals")
    def not_equals(self) -> Optional[Sequence[str]]:
        """
        List of string values to be evaluated.
        """
        return pulumi.get(self, "not_equals")


@pulumi.output_type
class OrganizationConfigurationDatasources(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "malwareProtection":
            suggest = "malware_protection"
        elif key == "s3Logs":
            suggest = "s3_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasources. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasources.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasources.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kubernetes: Optional['outputs.OrganizationConfigurationDatasourcesKubernetes'] = None,
                 malware_protection: Optional['outputs.OrganizationConfigurationDatasourcesMalwareProtection'] = None,
                 s3_logs: Optional['outputs.OrganizationConfigurationDatasourcesS3Logs'] = None):
        """
        :param 'OrganizationConfigurationDatasourcesKubernetesArgs' kubernetes: Enable Kubernetes Audit Logs Monitoring automatically for new member accounts.
        :param 'OrganizationConfigurationDatasourcesMalwareProtectionArgs' malware_protection: Enable Malware Protection automatically for new member accounts.
        :param 'OrganizationConfigurationDatasourcesS3LogsArgs' s3_logs: Enable S3 Protection automatically for new member accounts.
        """
        if kubernetes is not None:
            pulumi.set(__self__, "kubernetes", kubernetes)
        if malware_protection is not None:
            pulumi.set(__self__, "malware_protection", malware_protection)
        if s3_logs is not None:
            pulumi.set(__self__, "s3_logs", s3_logs)

    @property
    @pulumi.getter
    def kubernetes(self) -> Optional['outputs.OrganizationConfigurationDatasourcesKubernetes']:
        """
        Enable Kubernetes Audit Logs Monitoring automatically for new member accounts.
        """
        return pulumi.get(self, "kubernetes")

    @property
    @pulumi.getter(name="malwareProtection")
    def malware_protection(self) -> Optional['outputs.OrganizationConfigurationDatasourcesMalwareProtection']:
        """
        Enable Malware Protection automatically for new member accounts.
        """
        return pulumi.get(self, "malware_protection")

    @property
    @pulumi.getter(name="s3Logs")
    def s3_logs(self) -> Optional['outputs.OrganizationConfigurationDatasourcesS3Logs']:
        """
        Enable S3 Protection automatically for new member accounts.
        """
        return pulumi.get(self, "s3_logs")


@pulumi.output_type
class OrganizationConfigurationDatasourcesKubernetes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "auditLogs":
            suggest = "audit_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasourcesKubernetes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasourcesKubernetes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasourcesKubernetes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 audit_logs: 'outputs.OrganizationConfigurationDatasourcesKubernetesAuditLogs'):
        """
        :param 'OrganizationConfigurationDatasourcesKubernetesAuditLogsArgs' audit_logs: Enable Kubernetes Audit Logs Monitoring automatically for new member accounts. [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               See Kubernetes Audit Logs below for more details.
        """
        pulumi.set(__self__, "audit_logs", audit_logs)

    @property
    @pulumi.getter(name="auditLogs")
    def audit_logs(self) -> 'outputs.OrganizationConfigurationDatasourcesKubernetesAuditLogs':
        """
        Enable Kubernetes Audit Logs Monitoring automatically for new member accounts. [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        See Kubernetes Audit Logs below for more details.
        """
        return pulumi.get(self, "audit_logs")


@pulumi.output_type
class OrganizationConfigurationDatasourcesKubernetesAuditLogs(dict):
    def __init__(__self__, *,
                 enable: bool):
        """
        :param bool enable: If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
               Defaults to `true`.
        """
        pulumi.set(__self__, "enable", enable)

    @property
    @pulumi.getter
    def enable(self) -> bool:
        """
        If true, enables Kubernetes audit logs as a data source for [Kubernetes protection](https://docs.aws.amazon.com/guardduty/latest/ug/kubernetes-protection.html).
        Defaults to `true`.
        """
        return pulumi.get(self, "enable")


@pulumi.output_type
class OrganizationConfigurationDatasourcesMalwareProtection(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "scanEc2InstanceWithFindings":
            suggest = "scan_ec2_instance_with_findings"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasourcesMalwareProtection. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtection.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtection.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 scan_ec2_instance_with_findings: 'outputs.OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings'):
        """
        :param 'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsArgs' scan_ec2_instance_with_findings: Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for EC2 instances with findings should be auto-enabled for new members joining the organization.
               See Scan EC2 instance with findings below for more details.
        """
        pulumi.set(__self__, "scan_ec2_instance_with_findings", scan_ec2_instance_with_findings)

    @property
    @pulumi.getter(name="scanEc2InstanceWithFindings")
    def scan_ec2_instance_with_findings(self) -> 'outputs.OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings':
        """
        Configure whether [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for EC2 instances with findings should be auto-enabled for new members joining the organization.
        See Scan EC2 instance with findings below for more details.
        """
        return pulumi.get(self, "scan_ec2_instance_with_findings")


@pulumi.output_type
class OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ebsVolumes":
            suggest = "ebs_volumes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindings.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ebs_volumes: 'outputs.OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes'):
        """
        :param 'OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesArgs' ebs_volumes: Configure whether scanning EBS volumes should be auto-enabled for new members joining the organization
               See EBS volumes below for more details.
        """
        pulumi.set(__self__, "ebs_volumes", ebs_volumes)

    @property
    @pulumi.getter(name="ebsVolumes")
    def ebs_volumes(self) -> 'outputs.OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes':
        """
        Configure whether scanning EBS volumes should be auto-enabled for new members joining the organization
        See EBS volumes below for more details.
        """
        return pulumi.get(self, "ebs_volumes")


@pulumi.output_type
class OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoEnable":
            suggest = "auto_enable"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumes.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_enable: bool):
        """
        :param bool auto_enable: If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for all new accounts joining the organization.
               Defaults to `true`.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> bool:
        """
        If true, enables [Malware Protection](https://docs.aws.amazon.com/guardduty/latest/ug/malware-protection.html) for all new accounts joining the organization.
        Defaults to `true`.
        """
        return pulumi.get(self, "auto_enable")


@pulumi.output_type
class OrganizationConfigurationDatasourcesS3Logs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoEnable":
            suggest = "auto_enable"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationDatasourcesS3Logs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationDatasourcesS3Logs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationDatasourcesS3Logs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_enable: bool):
        """
        :param bool auto_enable: *Deprecated:* Use `auto_enable_organization_members` instead. When this setting is enabled, all new accounts that are created in, or added to, the organization are added as a member accounts of the organization’s GuardDuty delegated administrator and GuardDuty is enabled in that AWS Region.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> bool:
        """
        *Deprecated:* Use `auto_enable_organization_members` instead. When this setting is enabled, all new accounts that are created in, or added to, the organization are added as a member accounts of the organization’s GuardDuty delegated administrator and GuardDuty is enabled in that AWS Region.
        """
        return pulumi.get(self, "auto_enable")


@pulumi.output_type
class OrganizationConfigurationFeatureAdditionalConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoEnable":
            suggest = "auto_enable"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrganizationConfigurationFeatureAdditionalConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrganizationConfigurationFeatureAdditionalConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrganizationConfigurationFeatureAdditionalConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_enable: str,
                 name: str):
        """
        :param str auto_enable: The status of the additional configuration that will be configured for the organization. Valid values: `NEW`, `ALL`, `NONE`.
        :param str name: The name of the additional configuration that will be configured for the organization. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`.
        """
        pulumi.set(__self__, "auto_enable", auto_enable)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="autoEnable")
    def auto_enable(self) -> str:
        """
        The status of the additional configuration that will be configured for the organization. Valid values: `NEW`, `ALL`, `NONE`.
        """
        return pulumi.get(self, "auto_enable")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the additional configuration that will be configured for the organization. Valid values: `EKS_ADDON_MANAGEMENT`, `ECS_FARGATE_AGENT_MANAGEMENT`, `EC2_AGENT_MANAGEMENT`.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class GetDetectorFeatureResult(dict):
    def __init__(__self__, *,
                 additional_configurations: Sequence['outputs.GetDetectorFeatureAdditionalConfigurationResult'],
                 name: str,
                 status: str):
        """
        :param Sequence['GetDetectorFeatureAdditionalConfigurationArgs'] additional_configurations: Additional feature configuration.
        :param str name: The name of the detector feature.
        :param str status: Current status of the detector.
        """
        pulumi.set(__self__, "additional_configurations", additional_configurations)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="additionalConfigurations")
    def additional_configurations(self) -> Sequence['outputs.GetDetectorFeatureAdditionalConfigurationResult']:
        """
        Additional feature configuration.
        """
        return pulumi.get(self, "additional_configurations")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the detector feature.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Current status of the detector.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetDetectorFeatureAdditionalConfigurationResult(dict):
    def __init__(__self__, *,
                 name: str,
                 status: str):
        """
        :param str name: The name of the detector feature.
        :param str status: Current status of the detector.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the detector feature.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Current status of the detector.
        """
        return pulumi.get(self, "status")


