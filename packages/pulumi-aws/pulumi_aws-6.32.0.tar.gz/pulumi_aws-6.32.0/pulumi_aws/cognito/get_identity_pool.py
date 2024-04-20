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
    'GetIdentityPoolResult',
    'AwaitableGetIdentityPoolResult',
    'get_identity_pool',
    'get_identity_pool_output',
]

@pulumi.output_type
class GetIdentityPoolResult:
    """
    A collection of values returned by getIdentityPool.
    """
    def __init__(__self__, allow_classic_flow=None, allow_unauthenticated_identities=None, arn=None, cognito_identity_providers=None, developer_provider_name=None, id=None, identity_pool_name=None, openid_connect_provider_arns=None, saml_provider_arns=None, supported_login_providers=None, tags=None):
        if allow_classic_flow and not isinstance(allow_classic_flow, bool):
            raise TypeError("Expected argument 'allow_classic_flow' to be a bool")
        pulumi.set(__self__, "allow_classic_flow", allow_classic_flow)
        if allow_unauthenticated_identities and not isinstance(allow_unauthenticated_identities, bool):
            raise TypeError("Expected argument 'allow_unauthenticated_identities' to be a bool")
        pulumi.set(__self__, "allow_unauthenticated_identities", allow_unauthenticated_identities)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cognito_identity_providers and not isinstance(cognito_identity_providers, list):
            raise TypeError("Expected argument 'cognito_identity_providers' to be a list")
        pulumi.set(__self__, "cognito_identity_providers", cognito_identity_providers)
        if developer_provider_name and not isinstance(developer_provider_name, str):
            raise TypeError("Expected argument 'developer_provider_name' to be a str")
        pulumi.set(__self__, "developer_provider_name", developer_provider_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity_pool_name and not isinstance(identity_pool_name, str):
            raise TypeError("Expected argument 'identity_pool_name' to be a str")
        pulumi.set(__self__, "identity_pool_name", identity_pool_name)
        if openid_connect_provider_arns and not isinstance(openid_connect_provider_arns, list):
            raise TypeError("Expected argument 'openid_connect_provider_arns' to be a list")
        pulumi.set(__self__, "openid_connect_provider_arns", openid_connect_provider_arns)
        if saml_provider_arns and not isinstance(saml_provider_arns, list):
            raise TypeError("Expected argument 'saml_provider_arns' to be a list")
        pulumi.set(__self__, "saml_provider_arns", saml_provider_arns)
        if supported_login_providers and not isinstance(supported_login_providers, dict):
            raise TypeError("Expected argument 'supported_login_providers' to be a dict")
        pulumi.set(__self__, "supported_login_providers", supported_login_providers)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="allowClassicFlow")
    def allow_classic_flow(self) -> bool:
        """
        Whether the classic / basic authentication flow is enabled.
        """
        return pulumi.get(self, "allow_classic_flow")

    @property
    @pulumi.getter(name="allowUnauthenticatedIdentities")
    def allow_unauthenticated_identities(self) -> bool:
        """
        Whether the identity pool supports unauthenticated logins or not.
        """
        return pulumi.get(self, "allow_unauthenticated_identities")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Pool.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cognitoIdentityProviders")
    def cognito_identity_providers(self) -> Sequence['outputs.GetIdentityPoolCognitoIdentityProviderResult']:
        """
        An array of Amazon Cognito Identity user pools and their client IDs.
        """
        return pulumi.get(self, "cognito_identity_providers")

    @property
    @pulumi.getter(name="developerProviderName")
    def developer_provider_name(self) -> str:
        """
        The "domain" by which Cognito will refer to your users.
        """
        return pulumi.get(self, "developer_provider_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="identityPoolName")
    def identity_pool_name(self) -> str:
        return pulumi.get(self, "identity_pool_name")

    @property
    @pulumi.getter(name="openidConnectProviderArns")
    def openid_connect_provider_arns(self) -> Sequence[str]:
        """
        Set of OpendID Connect provider ARNs.
        """
        return pulumi.get(self, "openid_connect_provider_arns")

    @property
    @pulumi.getter(name="samlProviderArns")
    def saml_provider_arns(self) -> Sequence[str]:
        """
        An array of Amazon Resource Names (ARNs) of the SAML provider for your identity.
        """
        return pulumi.get(self, "saml_provider_arns")

    @property
    @pulumi.getter(name="supportedLoginProviders")
    def supported_login_providers(self) -> Mapping[str, str]:
        """
        Key-Value pairs mapping provider names to provider app IDs.
        """
        return pulumi.get(self, "supported_login_providers")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A map of tags to assigned to the Identity Pool.
        """
        return pulumi.get(self, "tags")


class AwaitableGetIdentityPoolResult(GetIdentityPoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIdentityPoolResult(
            allow_classic_flow=self.allow_classic_flow,
            allow_unauthenticated_identities=self.allow_unauthenticated_identities,
            arn=self.arn,
            cognito_identity_providers=self.cognito_identity_providers,
            developer_provider_name=self.developer_provider_name,
            id=self.id,
            identity_pool_name=self.identity_pool_name,
            openid_connect_provider_arns=self.openid_connect_provider_arns,
            saml_provider_arns=self.saml_provider_arns,
            supported_login_providers=self.supported_login_providers,
            tags=self.tags)


def get_identity_pool(identity_pool_name: Optional[str] = None,
                      tags: Optional[Mapping[str, str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIdentityPoolResult:
    """
    Data source for managing an AWS Cognito Identity Pool.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cognito.get_identity_pool(identity_pool_name="test pool")
    ```
    <!--End PulumiCodeChooser -->


    :param str identity_pool_name: The Cognito Identity Pool name.
    :param Mapping[str, str] tags: A map of tags to assigned to the Identity Pool.
    """
    __args__ = dict()
    __args__['identityPoolName'] = identity_pool_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cognito/getIdentityPool:getIdentityPool', __args__, opts=opts, typ=GetIdentityPoolResult).value

    return AwaitableGetIdentityPoolResult(
        allow_classic_flow=pulumi.get(__ret__, 'allow_classic_flow'),
        allow_unauthenticated_identities=pulumi.get(__ret__, 'allow_unauthenticated_identities'),
        arn=pulumi.get(__ret__, 'arn'),
        cognito_identity_providers=pulumi.get(__ret__, 'cognito_identity_providers'),
        developer_provider_name=pulumi.get(__ret__, 'developer_provider_name'),
        id=pulumi.get(__ret__, 'id'),
        identity_pool_name=pulumi.get(__ret__, 'identity_pool_name'),
        openid_connect_provider_arns=pulumi.get(__ret__, 'openid_connect_provider_arns'),
        saml_provider_arns=pulumi.get(__ret__, 'saml_provider_arns'),
        supported_login_providers=pulumi.get(__ret__, 'supported_login_providers'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_identity_pool)
def get_identity_pool_output(identity_pool_name: Optional[pulumi.Input[str]] = None,
                             tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIdentityPoolResult]:
    """
    Data source for managing an AWS Cognito Identity Pool.

    ## Example Usage

    ### Basic Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cognito.get_identity_pool(identity_pool_name="test pool")
    ```
    <!--End PulumiCodeChooser -->


    :param str identity_pool_name: The Cognito Identity Pool name.
    :param Mapping[str, str] tags: A map of tags to assigned to the Identity Pool.
    """
    ...
