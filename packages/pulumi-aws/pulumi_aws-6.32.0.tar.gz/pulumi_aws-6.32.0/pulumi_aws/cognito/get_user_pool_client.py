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
    'GetUserPoolClientResult',
    'AwaitableGetUserPoolClientResult',
    'get_user_pool_client',
    'get_user_pool_client_output',
]

@pulumi.output_type
class GetUserPoolClientResult:
    """
    A collection of values returned by getUserPoolClient.
    """
    def __init__(__self__, access_token_validity=None, allowed_oauth_flows=None, allowed_oauth_flows_user_pool_client=None, allowed_oauth_scopes=None, analytics_configurations=None, callback_urls=None, client_id=None, client_secret=None, default_redirect_uri=None, enable_propagate_additional_user_context_data=None, enable_token_revocation=None, explicit_auth_flows=None, generate_secret=None, id=None, id_token_validity=None, logout_urls=None, name=None, prevent_user_existence_errors=None, read_attributes=None, refresh_token_validity=None, supported_identity_providers=None, token_validity_units=None, user_pool_id=None, write_attributes=None):
        if access_token_validity and not isinstance(access_token_validity, int):
            raise TypeError("Expected argument 'access_token_validity' to be a int")
        pulumi.set(__self__, "access_token_validity", access_token_validity)
        if allowed_oauth_flows and not isinstance(allowed_oauth_flows, list):
            raise TypeError("Expected argument 'allowed_oauth_flows' to be a list")
        pulumi.set(__self__, "allowed_oauth_flows", allowed_oauth_flows)
        if allowed_oauth_flows_user_pool_client and not isinstance(allowed_oauth_flows_user_pool_client, bool):
            raise TypeError("Expected argument 'allowed_oauth_flows_user_pool_client' to be a bool")
        pulumi.set(__self__, "allowed_oauth_flows_user_pool_client", allowed_oauth_flows_user_pool_client)
        if allowed_oauth_scopes and not isinstance(allowed_oauth_scopes, list):
            raise TypeError("Expected argument 'allowed_oauth_scopes' to be a list")
        pulumi.set(__self__, "allowed_oauth_scopes", allowed_oauth_scopes)
        if analytics_configurations and not isinstance(analytics_configurations, list):
            raise TypeError("Expected argument 'analytics_configurations' to be a list")
        pulumi.set(__self__, "analytics_configurations", analytics_configurations)
        if callback_urls and not isinstance(callback_urls, list):
            raise TypeError("Expected argument 'callback_urls' to be a list")
        pulumi.set(__self__, "callback_urls", callback_urls)
        if client_id and not isinstance(client_id, str):
            raise TypeError("Expected argument 'client_id' to be a str")
        pulumi.set(__self__, "client_id", client_id)
        if client_secret and not isinstance(client_secret, str):
            raise TypeError("Expected argument 'client_secret' to be a str")
        pulumi.set(__self__, "client_secret", client_secret)
        if default_redirect_uri and not isinstance(default_redirect_uri, str):
            raise TypeError("Expected argument 'default_redirect_uri' to be a str")
        pulumi.set(__self__, "default_redirect_uri", default_redirect_uri)
        if enable_propagate_additional_user_context_data and not isinstance(enable_propagate_additional_user_context_data, bool):
            raise TypeError("Expected argument 'enable_propagate_additional_user_context_data' to be a bool")
        pulumi.set(__self__, "enable_propagate_additional_user_context_data", enable_propagate_additional_user_context_data)
        if enable_token_revocation and not isinstance(enable_token_revocation, bool):
            raise TypeError("Expected argument 'enable_token_revocation' to be a bool")
        pulumi.set(__self__, "enable_token_revocation", enable_token_revocation)
        if explicit_auth_flows and not isinstance(explicit_auth_flows, list):
            raise TypeError("Expected argument 'explicit_auth_flows' to be a list")
        pulumi.set(__self__, "explicit_auth_flows", explicit_auth_flows)
        if generate_secret and not isinstance(generate_secret, bool):
            raise TypeError("Expected argument 'generate_secret' to be a bool")
        pulumi.set(__self__, "generate_secret", generate_secret)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if id_token_validity and not isinstance(id_token_validity, int):
            raise TypeError("Expected argument 'id_token_validity' to be a int")
        pulumi.set(__self__, "id_token_validity", id_token_validity)
        if logout_urls and not isinstance(logout_urls, list):
            raise TypeError("Expected argument 'logout_urls' to be a list")
        pulumi.set(__self__, "logout_urls", logout_urls)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if prevent_user_existence_errors and not isinstance(prevent_user_existence_errors, str):
            raise TypeError("Expected argument 'prevent_user_existence_errors' to be a str")
        pulumi.set(__self__, "prevent_user_existence_errors", prevent_user_existence_errors)
        if read_attributes and not isinstance(read_attributes, list):
            raise TypeError("Expected argument 'read_attributes' to be a list")
        pulumi.set(__self__, "read_attributes", read_attributes)
        if refresh_token_validity and not isinstance(refresh_token_validity, int):
            raise TypeError("Expected argument 'refresh_token_validity' to be a int")
        pulumi.set(__self__, "refresh_token_validity", refresh_token_validity)
        if supported_identity_providers and not isinstance(supported_identity_providers, list):
            raise TypeError("Expected argument 'supported_identity_providers' to be a list")
        pulumi.set(__self__, "supported_identity_providers", supported_identity_providers)
        if token_validity_units and not isinstance(token_validity_units, list):
            raise TypeError("Expected argument 'token_validity_units' to be a list")
        pulumi.set(__self__, "token_validity_units", token_validity_units)
        if user_pool_id and not isinstance(user_pool_id, str):
            raise TypeError("Expected argument 'user_pool_id' to be a str")
        pulumi.set(__self__, "user_pool_id", user_pool_id)
        if write_attributes and not isinstance(write_attributes, list):
            raise TypeError("Expected argument 'write_attributes' to be a list")
        pulumi.set(__self__, "write_attributes", write_attributes)

    @property
    @pulumi.getter(name="accessTokenValidity")
    def access_token_validity(self) -> int:
        """
        (Optional) Time limit, between 5 minutes and 1 day, after which the access token is no longer valid and cannot be used. This value will be overridden if you have entered a value in `token_validity_units`.
        """
        return pulumi.get(self, "access_token_validity")

    @property
    @pulumi.getter(name="allowedOauthFlows")
    def allowed_oauth_flows(self) -> Sequence[str]:
        """
        (Optional) List of allowed OAuth flows (code, implicit, client_credentials).
        """
        return pulumi.get(self, "allowed_oauth_flows")

    @property
    @pulumi.getter(name="allowedOauthFlowsUserPoolClient")
    def allowed_oauth_flows_user_pool_client(self) -> bool:
        """
        (Optional) Whether the client is allowed to follow the OAuth protocol when interacting with Cognito user pools.
        """
        return pulumi.get(self, "allowed_oauth_flows_user_pool_client")

    @property
    @pulumi.getter(name="allowedOauthScopes")
    def allowed_oauth_scopes(self) -> Sequence[str]:
        """
        (Optional) List of allowed OAuth scopes (phone, email, openid, profile, and aws.cognito.signin.user.admin).
        """
        return pulumi.get(self, "allowed_oauth_scopes")

    @property
    @pulumi.getter(name="analyticsConfigurations")
    def analytics_configurations(self) -> Sequence['outputs.GetUserPoolClientAnalyticsConfigurationResult']:
        """
        (Optional) Configuration block for Amazon Pinpoint analytics for collecting metrics for this user pool. Detailed below.
        """
        return pulumi.get(self, "analytics_configurations")

    @property
    @pulumi.getter(name="callbackUrls")
    def callback_urls(self) -> Sequence[str]:
        """
        (Optional) List of allowed callback URLs for the identity providers.
        """
        return pulumi.get(self, "callback_urls")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> str:
        """
        Client secret of the user pool client.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="defaultRedirectUri")
    def default_redirect_uri(self) -> str:
        """
        (Optional) Default redirect URI. Must be in the list of callback URLs.
        """
        return pulumi.get(self, "default_redirect_uri")

    @property
    @pulumi.getter(name="enablePropagateAdditionalUserContextData")
    def enable_propagate_additional_user_context_data(self) -> bool:
        return pulumi.get(self, "enable_propagate_additional_user_context_data")

    @property
    @pulumi.getter(name="enableTokenRevocation")
    def enable_token_revocation(self) -> bool:
        """
        (Optional) Enables or disables token revocation.
        """
        return pulumi.get(self, "enable_token_revocation")

    @property
    @pulumi.getter(name="explicitAuthFlows")
    def explicit_auth_flows(self) -> Sequence[str]:
        """
        (Optional) List of authentication flows (ADMIN_NO_SRP_AUTH, CUSTOM_AUTH_FLOW_ONLY, USER_PASSWORD_AUTH, ALLOW_ADMIN_USER_PASSWORD_AUTH, ALLOW_CUSTOM_AUTH, ALLOW_USER_PASSWORD_AUTH, ALLOW_USER_SRP_AUTH, ALLOW_REFRESH_TOKEN_AUTH).
        """
        return pulumi.get(self, "explicit_auth_flows")

    @property
    @pulumi.getter(name="generateSecret")
    def generate_secret(self) -> bool:
        """
        (Optional) Should an application secret be generated.
        """
        return pulumi.get(self, "generate_secret")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="idTokenValidity")
    def id_token_validity(self) -> int:
        """
        (Optional) Time limit, between 5 minutes and 1 day, after which the ID token is no longer valid and cannot be used. This value will be overridden if you have entered a value in `token_validity_units`.
        """
        return pulumi.get(self, "id_token_validity")

    @property
    @pulumi.getter(name="logoutUrls")
    def logout_urls(self) -> Sequence[str]:
        """
        (Optional) List of allowed logout URLs for the identity providers.
        """
        return pulumi.get(self, "logout_urls")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="preventUserExistenceErrors")
    def prevent_user_existence_errors(self) -> str:
        """
        (Optional) Choose which errors and responses are returned by Cognito APIs during authentication, account confirmation, and password recovery when the user does not exist in the user pool. When set to `ENABLED` and the user does not exist, authentication returns an error indicating either the username or password was incorrect, and account confirmation and password recovery return a response indicating a code was sent to a simulated destination. When set to `LEGACY`, those APIs will return a `UserNotFoundException` exception if the user does not exist in the user pool.
        """
        return pulumi.get(self, "prevent_user_existence_errors")

    @property
    @pulumi.getter(name="readAttributes")
    def read_attributes(self) -> Sequence[str]:
        """
        (Optional) List of user pool attributes the application client can read from.
        """
        return pulumi.get(self, "read_attributes")

    @property
    @pulumi.getter(name="refreshTokenValidity")
    def refresh_token_validity(self) -> int:
        """
        (Optional) Time limit in days refresh tokens are valid for.
        """
        return pulumi.get(self, "refresh_token_validity")

    @property
    @pulumi.getter(name="supportedIdentityProviders")
    def supported_identity_providers(self) -> Sequence[str]:
        """
        (Optional) List of provider names for the identity providers that are supported on this client. Uses the `provider_name` attribute of `cognito.IdentityProvider` resource(s), or the equivalent string(s).
        """
        return pulumi.get(self, "supported_identity_providers")

    @property
    @pulumi.getter(name="tokenValidityUnits")
    def token_validity_units(self) -> Sequence['outputs.GetUserPoolClientTokenValidityUnitResult']:
        """
        (Optional) Configuration block for units in which the validity times are represented in. Detailed below.
        """
        return pulumi.get(self, "token_validity_units")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> str:
        return pulumi.get(self, "user_pool_id")

    @property
    @pulumi.getter(name="writeAttributes")
    def write_attributes(self) -> Sequence[str]:
        """
        (Optional) List of user pool attributes the application client can write to.
        """
        return pulumi.get(self, "write_attributes")


class AwaitableGetUserPoolClientResult(GetUserPoolClientResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserPoolClientResult(
            access_token_validity=self.access_token_validity,
            allowed_oauth_flows=self.allowed_oauth_flows,
            allowed_oauth_flows_user_pool_client=self.allowed_oauth_flows_user_pool_client,
            allowed_oauth_scopes=self.allowed_oauth_scopes,
            analytics_configurations=self.analytics_configurations,
            callback_urls=self.callback_urls,
            client_id=self.client_id,
            client_secret=self.client_secret,
            default_redirect_uri=self.default_redirect_uri,
            enable_propagate_additional_user_context_data=self.enable_propagate_additional_user_context_data,
            enable_token_revocation=self.enable_token_revocation,
            explicit_auth_flows=self.explicit_auth_flows,
            generate_secret=self.generate_secret,
            id=self.id,
            id_token_validity=self.id_token_validity,
            logout_urls=self.logout_urls,
            name=self.name,
            prevent_user_existence_errors=self.prevent_user_existence_errors,
            read_attributes=self.read_attributes,
            refresh_token_validity=self.refresh_token_validity,
            supported_identity_providers=self.supported_identity_providers,
            token_validity_units=self.token_validity_units,
            user_pool_id=self.user_pool_id,
            write_attributes=self.write_attributes)


def get_user_pool_client(client_id: Optional[str] = None,
                         user_pool_id: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserPoolClientResult:
    """
    Provides a Cognito User Pool Client resource.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    client = aws.cognito.get_user_pool_client(client_id="38fjsnc484p94kpqsnet7mpld0",
        user_pool_id="us-west-2_aaaaaaaaa")
    ```
    <!--End PulumiCodeChooser -->


    :param str client_id: Client Id of the user pool.
    :param str user_pool_id: User pool the client belongs to.
    """
    __args__ = dict()
    __args__['clientId'] = client_id
    __args__['userPoolId'] = user_pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cognito/getUserPoolClient:getUserPoolClient', __args__, opts=opts, typ=GetUserPoolClientResult).value

    return AwaitableGetUserPoolClientResult(
        access_token_validity=pulumi.get(__ret__, 'access_token_validity'),
        allowed_oauth_flows=pulumi.get(__ret__, 'allowed_oauth_flows'),
        allowed_oauth_flows_user_pool_client=pulumi.get(__ret__, 'allowed_oauth_flows_user_pool_client'),
        allowed_oauth_scopes=pulumi.get(__ret__, 'allowed_oauth_scopes'),
        analytics_configurations=pulumi.get(__ret__, 'analytics_configurations'),
        callback_urls=pulumi.get(__ret__, 'callback_urls'),
        client_id=pulumi.get(__ret__, 'client_id'),
        client_secret=pulumi.get(__ret__, 'client_secret'),
        default_redirect_uri=pulumi.get(__ret__, 'default_redirect_uri'),
        enable_propagate_additional_user_context_data=pulumi.get(__ret__, 'enable_propagate_additional_user_context_data'),
        enable_token_revocation=pulumi.get(__ret__, 'enable_token_revocation'),
        explicit_auth_flows=pulumi.get(__ret__, 'explicit_auth_flows'),
        generate_secret=pulumi.get(__ret__, 'generate_secret'),
        id=pulumi.get(__ret__, 'id'),
        id_token_validity=pulumi.get(__ret__, 'id_token_validity'),
        logout_urls=pulumi.get(__ret__, 'logout_urls'),
        name=pulumi.get(__ret__, 'name'),
        prevent_user_existence_errors=pulumi.get(__ret__, 'prevent_user_existence_errors'),
        read_attributes=pulumi.get(__ret__, 'read_attributes'),
        refresh_token_validity=pulumi.get(__ret__, 'refresh_token_validity'),
        supported_identity_providers=pulumi.get(__ret__, 'supported_identity_providers'),
        token_validity_units=pulumi.get(__ret__, 'token_validity_units'),
        user_pool_id=pulumi.get(__ret__, 'user_pool_id'),
        write_attributes=pulumi.get(__ret__, 'write_attributes'))


@_utilities.lift_output_func(get_user_pool_client)
def get_user_pool_client_output(client_id: Optional[pulumi.Input[str]] = None,
                                user_pool_id: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserPoolClientResult]:
    """
    Provides a Cognito User Pool Client resource.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    client = aws.cognito.get_user_pool_client(client_id="38fjsnc484p94kpqsnet7mpld0",
        user_pool_id="us-west-2_aaaaaaaaa")
    ```
    <!--End PulumiCodeChooser -->


    :param str client_id: Client Id of the user pool.
    :param str user_pool_id: User pool the client belongs to.
    """
    ...
