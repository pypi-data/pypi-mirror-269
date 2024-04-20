# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetNamespaceResult',
    'AwaitableGetNamespaceResult',
    'get_namespace',
    'get_namespace_output',
]

@pulumi.output_type
class GetNamespaceResult:
    """
    A collection of values returned by getNamespace.
    """
    def __init__(__self__, admin_username=None, arn=None, db_name=None, default_iam_role_arn=None, iam_roles=None, id=None, kms_key_id=None, log_exports=None, namespace_id=None, namespace_name=None):
        if admin_username and not isinstance(admin_username, str):
            raise TypeError("Expected argument 'admin_username' to be a str")
        pulumi.set(__self__, "admin_username", admin_username)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if db_name and not isinstance(db_name, str):
            raise TypeError("Expected argument 'db_name' to be a str")
        pulumi.set(__self__, "db_name", db_name)
        if default_iam_role_arn and not isinstance(default_iam_role_arn, str):
            raise TypeError("Expected argument 'default_iam_role_arn' to be a str")
        pulumi.set(__self__, "default_iam_role_arn", default_iam_role_arn)
        if iam_roles and not isinstance(iam_roles, list):
            raise TypeError("Expected argument 'iam_roles' to be a list")
        pulumi.set(__self__, "iam_roles", iam_roles)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if log_exports and not isinstance(log_exports, list):
            raise TypeError("Expected argument 'log_exports' to be a list")
        pulumi.set(__self__, "log_exports", log_exports)
        if namespace_id and not isinstance(namespace_id, str):
            raise TypeError("Expected argument 'namespace_id' to be a str")
        pulumi.set(__self__, "namespace_id", namespace_id)
        if namespace_name and not isinstance(namespace_name, str):
            raise TypeError("Expected argument 'namespace_name' to be a str")
        pulumi.set(__self__, "namespace_name", namespace_name)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> str:
        """
        The username of the administrator for the first database created in the namespace.
        """
        return pulumi.get(self, "admin_username")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the Redshift Serverless Namespace.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dbName")
    def db_name(self) -> str:
        """
        The name of the first database created in the namespace.
        """
        return pulumi.get(self, "db_name")

    @property
    @pulumi.getter(name="defaultIamRoleArn")
    def default_iam_role_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the IAM role to set as a default in the namespace. When specifying `default_iam_role_arn`, it also must be part of `iam_roles`.
        """
        return pulumi.get(self, "default_iam_role_arn")

    @property
    @pulumi.getter(name="iamRoles")
    def iam_roles(self) -> Sequence[str]:
        """
        A list of IAM roles to associate with the namespace.
        """
        return pulumi.get(self, "iam_roles")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> str:
        """
        The ARN of the Amazon Web Services Key Management Service key used to encrypt your data.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="logExports")
    def log_exports(self) -> Sequence[str]:
        """
        The types of logs the namespace can export. Available export types are `userlog`, `connectionlog`, and `useractivitylog`.
        """
        return pulumi.get(self, "log_exports")

    @property
    @pulumi.getter(name="namespaceId")
    def namespace_id(self) -> str:
        """
        The Redshift Namespace ID.
        """
        return pulumi.get(self, "namespace_id")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> str:
        return pulumi.get(self, "namespace_name")


class AwaitableGetNamespaceResult(GetNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespaceResult(
            admin_username=self.admin_username,
            arn=self.arn,
            db_name=self.db_name,
            default_iam_role_arn=self.default_iam_role_arn,
            iam_roles=self.iam_roles,
            id=self.id,
            kms_key_id=self.kms_key_id,
            log_exports=self.log_exports,
            namespace_id=self.namespace_id,
            namespace_name=self.namespace_name)


def get_namespace(namespace_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespaceResult:
    """
    Data source for managing an AWS Redshift Serverless Namespace.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.redshiftserverless.get_namespace(namespace_name="example-namespace")
    ```
    <!--End PulumiCodeChooser -->


    :param str namespace_name: The name of the namespace.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:redshiftserverless/getNamespace:getNamespace', __args__, opts=opts, typ=GetNamespaceResult).value

    return AwaitableGetNamespaceResult(
        admin_username=pulumi.get(__ret__, 'admin_username'),
        arn=pulumi.get(__ret__, 'arn'),
        db_name=pulumi.get(__ret__, 'db_name'),
        default_iam_role_arn=pulumi.get(__ret__, 'default_iam_role_arn'),
        iam_roles=pulumi.get(__ret__, 'iam_roles'),
        id=pulumi.get(__ret__, 'id'),
        kms_key_id=pulumi.get(__ret__, 'kms_key_id'),
        log_exports=pulumi.get(__ret__, 'log_exports'),
        namespace_id=pulumi.get(__ret__, 'namespace_id'),
        namespace_name=pulumi.get(__ret__, 'namespace_name'))


@_utilities.lift_output_func(get_namespace)
def get_namespace_output(namespace_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNamespaceResult]:
    """
    Data source for managing an AWS Redshift Serverless Namespace.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.redshiftserverless.get_namespace(namespace_name="example-namespace")
    ```
    <!--End PulumiCodeChooser -->


    :param str namespace_name: The name of the namespace.
    """
    ...
