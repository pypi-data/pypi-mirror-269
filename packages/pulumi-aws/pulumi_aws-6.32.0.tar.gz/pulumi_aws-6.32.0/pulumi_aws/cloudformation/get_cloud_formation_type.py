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
    'GetCloudFormationTypeResult',
    'AwaitableGetCloudFormationTypeResult',
    'get_cloud_formation_type',
    'get_cloud_formation_type_output',
]

@pulumi.output_type
class GetCloudFormationTypeResult:
    """
    A collection of values returned by getCloudFormationType.
    """
    def __init__(__self__, arn=None, default_version_id=None, deprecated_status=None, description=None, documentation_url=None, execution_role_arn=None, id=None, is_default_version=None, logging_configs=None, provisioning_type=None, schema=None, source_url=None, type=None, type_arn=None, type_name=None, version_id=None, visibility=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_version_id and not isinstance(default_version_id, str):
            raise TypeError("Expected argument 'default_version_id' to be a str")
        pulumi.set(__self__, "default_version_id", default_version_id)
        if deprecated_status and not isinstance(deprecated_status, str):
            raise TypeError("Expected argument 'deprecated_status' to be a str")
        pulumi.set(__self__, "deprecated_status", deprecated_status)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if documentation_url and not isinstance(documentation_url, str):
            raise TypeError("Expected argument 'documentation_url' to be a str")
        pulumi.set(__self__, "documentation_url", documentation_url)
        if execution_role_arn and not isinstance(execution_role_arn, str):
            raise TypeError("Expected argument 'execution_role_arn' to be a str")
        pulumi.set(__self__, "execution_role_arn", execution_role_arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_default_version and not isinstance(is_default_version, bool):
            raise TypeError("Expected argument 'is_default_version' to be a bool")
        pulumi.set(__self__, "is_default_version", is_default_version)
        if logging_configs and not isinstance(logging_configs, list):
            raise TypeError("Expected argument 'logging_configs' to be a list")
        pulumi.set(__self__, "logging_configs", logging_configs)
        if provisioning_type and not isinstance(provisioning_type, str):
            raise TypeError("Expected argument 'provisioning_type' to be a str")
        pulumi.set(__self__, "provisioning_type", provisioning_type)
        if schema and not isinstance(schema, str):
            raise TypeError("Expected argument 'schema' to be a str")
        pulumi.set(__self__, "schema", schema)
        if source_url and not isinstance(source_url, str):
            raise TypeError("Expected argument 'source_url' to be a str")
        pulumi.set(__self__, "source_url", source_url)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if type_arn and not isinstance(type_arn, str):
            raise TypeError("Expected argument 'type_arn' to be a str")
        pulumi.set(__self__, "type_arn", type_arn)
        if type_name and not isinstance(type_name, str):
            raise TypeError("Expected argument 'type_name' to be a str")
        pulumi.set(__self__, "type_name", type_name)
        if version_id and not isinstance(version_id, str):
            raise TypeError("Expected argument 'version_id' to be a str")
        pulumi.set(__self__, "version_id", version_id)
        if visibility and not isinstance(visibility, str):
            raise TypeError("Expected argument 'visibility' to be a str")
        pulumi.set(__self__, "visibility", visibility)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultVersionId")
    def default_version_id(self) -> str:
        """
        Identifier of the CloudFormation Type default version.
        """
        return pulumi.get(self, "default_version_id")

    @property
    @pulumi.getter(name="deprecatedStatus")
    def deprecated_status(self) -> str:
        """
        Deprecation status of the CloudFormation Type.
        """
        return pulumi.get(self, "deprecated_status")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the CloudFormation Type.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentationUrl")
    def documentation_url(self) -> str:
        """
        URL of the documentation for the CloudFormation Type.
        """
        return pulumi.get(self, "documentation_url")

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> str:
        """
        ARN of the IAM Role used to register the CloudFormation Type.
        """
        return pulumi.get(self, "execution_role_arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isDefaultVersion")
    def is_default_version(self) -> bool:
        """
        Whether the CloudFormation Type version is the default version.
        """
        return pulumi.get(self, "is_default_version")

    @property
    @pulumi.getter(name="loggingConfigs")
    def logging_configs(self) -> Sequence['outputs.GetCloudFormationTypeLoggingConfigResult']:
        """
        List of objects containing logging configuration.
        """
        return pulumi.get(self, "logging_configs")

    @property
    @pulumi.getter(name="provisioningType")
    def provisioning_type(self) -> str:
        """
        Provisioning behavior of the CloudFormation Type.
        """
        return pulumi.get(self, "provisioning_type")

    @property
    @pulumi.getter
    def schema(self) -> str:
        """
        JSON document of the CloudFormation Type schema.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter(name="sourceUrl")
    def source_url(self) -> str:
        """
        URL of the source code for the CloudFormation Type.
        """
        return pulumi.get(self, "source_url")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="typeArn")
    def type_arn(self) -> str:
        return pulumi.get(self, "type_arn")

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> str:
        return pulumi.get(self, "type_name")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> Optional[str]:
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter
    def visibility(self) -> str:
        """
        Scope of the CloudFormation Type.
        """
        return pulumi.get(self, "visibility")


class AwaitableGetCloudFormationTypeResult(GetCloudFormationTypeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudFormationTypeResult(
            arn=self.arn,
            default_version_id=self.default_version_id,
            deprecated_status=self.deprecated_status,
            description=self.description,
            documentation_url=self.documentation_url,
            execution_role_arn=self.execution_role_arn,
            id=self.id,
            is_default_version=self.is_default_version,
            logging_configs=self.logging_configs,
            provisioning_type=self.provisioning_type,
            schema=self.schema,
            source_url=self.source_url,
            type=self.type,
            type_arn=self.type_arn,
            type_name=self.type_name,
            version_id=self.version_id,
            visibility=self.visibility)


def get_cloud_formation_type(arn: Optional[str] = None,
                             type: Optional[str] = None,
                             type_name: Optional[str] = None,
                             version_id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudFormationTypeResult:
    """
    Provides details about a CloudFormation Type.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudformation.get_cloud_formation_type(type="RESOURCE",
        type_name="AWS::Athena::WorkGroup")
    ```
    <!--End PulumiCodeChooser -->


    :param str arn: ARN of the CloudFormation Type. For example, `arn:aws:cloudformation:us-west-2::type/resource/AWS-EC2-VPC`.
    :param str type: CloudFormation Registry Type. For example, `RESOURCE`.
    :param str type_name: CloudFormation Type name. For example, `AWS::EC2::VPC`.
    :param str version_id: Identifier of the CloudFormation Type version.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['type'] = type
    __args__['typeName'] = type_name
    __args__['versionId'] = version_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudformation/getCloudFormationType:getCloudFormationType', __args__, opts=opts, typ=GetCloudFormationTypeResult).value

    return AwaitableGetCloudFormationTypeResult(
        arn=pulumi.get(__ret__, 'arn'),
        default_version_id=pulumi.get(__ret__, 'default_version_id'),
        deprecated_status=pulumi.get(__ret__, 'deprecated_status'),
        description=pulumi.get(__ret__, 'description'),
        documentation_url=pulumi.get(__ret__, 'documentation_url'),
        execution_role_arn=pulumi.get(__ret__, 'execution_role_arn'),
        id=pulumi.get(__ret__, 'id'),
        is_default_version=pulumi.get(__ret__, 'is_default_version'),
        logging_configs=pulumi.get(__ret__, 'logging_configs'),
        provisioning_type=pulumi.get(__ret__, 'provisioning_type'),
        schema=pulumi.get(__ret__, 'schema'),
        source_url=pulumi.get(__ret__, 'source_url'),
        type=pulumi.get(__ret__, 'type'),
        type_arn=pulumi.get(__ret__, 'type_arn'),
        type_name=pulumi.get(__ret__, 'type_name'),
        version_id=pulumi.get(__ret__, 'version_id'),
        visibility=pulumi.get(__ret__, 'visibility'))


@_utilities.lift_output_func(get_cloud_formation_type)
def get_cloud_formation_type_output(arn: Optional[pulumi.Input[Optional[str]]] = None,
                                    type: Optional[pulumi.Input[Optional[str]]] = None,
                                    type_name: Optional[pulumi.Input[Optional[str]]] = None,
                                    version_id: Optional[pulumi.Input[Optional[str]]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudFormationTypeResult]:
    """
    Provides details about a CloudFormation Type.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudformation.get_cloud_formation_type(type="RESOURCE",
        type_name="AWS::Athena::WorkGroup")
    ```
    <!--End PulumiCodeChooser -->


    :param str arn: ARN of the CloudFormation Type. For example, `arn:aws:cloudformation:us-west-2::type/resource/AWS-EC2-VPC`.
    :param str type: CloudFormation Registry Type. For example, `RESOURCE`.
    :param str type_name: CloudFormation Type name. For example, `AWS::EC2::VPC`.
    :param str version_id: Identifier of the CloudFormation Type version.
    """
    ...
