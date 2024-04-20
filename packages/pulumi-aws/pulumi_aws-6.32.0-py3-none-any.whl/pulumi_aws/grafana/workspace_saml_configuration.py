# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['WorkspaceSamlConfigurationArgs', 'WorkspaceSamlConfiguration']

@pulumi.input_type
class WorkspaceSamlConfigurationArgs:
    def __init__(__self__, *,
                 editor_role_values: pulumi.Input[Sequence[pulumi.Input[str]]],
                 workspace_id: pulumi.Input[str],
                 admin_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 email_assertion: Optional[pulumi.Input[str]] = None,
                 groups_assertion: Optional[pulumi.Input[str]] = None,
                 idp_metadata_url: Optional[pulumi.Input[str]] = None,
                 idp_metadata_xml: Optional[pulumi.Input[str]] = None,
                 login_assertion: Optional[pulumi.Input[str]] = None,
                 login_validity_duration: Optional[pulumi.Input[int]] = None,
                 name_assertion: Optional[pulumi.Input[str]] = None,
                 org_assertion: Optional[pulumi.Input[str]] = None,
                 role_assertion: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WorkspaceSamlConfiguration resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] editor_role_values: The editor role values.
        :param pulumi.Input[str] workspace_id: The workspace id.
               
               The following arguments are optional:
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_role_values: The admin role values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_organizations: The allowed organizations.
        :param pulumi.Input[str] email_assertion: The email assertion.
        :param pulumi.Input[str] groups_assertion: The groups assertion.
        :param pulumi.Input[str] idp_metadata_url: The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] idp_metadata_xml: The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] login_assertion: The login assertion.
        :param pulumi.Input[int] login_validity_duration: The login validity duration.
        :param pulumi.Input[str] name_assertion: The name assertion.
        :param pulumi.Input[str] org_assertion: The org assertion.
        :param pulumi.Input[str] role_assertion: The role assertion.
        """
        pulumi.set(__self__, "editor_role_values", editor_role_values)
        pulumi.set(__self__, "workspace_id", workspace_id)
        if admin_role_values is not None:
            pulumi.set(__self__, "admin_role_values", admin_role_values)
        if allowed_organizations is not None:
            pulumi.set(__self__, "allowed_organizations", allowed_organizations)
        if email_assertion is not None:
            pulumi.set(__self__, "email_assertion", email_assertion)
        if groups_assertion is not None:
            pulumi.set(__self__, "groups_assertion", groups_assertion)
        if idp_metadata_url is not None:
            pulumi.set(__self__, "idp_metadata_url", idp_metadata_url)
        if idp_metadata_xml is not None:
            pulumi.set(__self__, "idp_metadata_xml", idp_metadata_xml)
        if login_assertion is not None:
            pulumi.set(__self__, "login_assertion", login_assertion)
        if login_validity_duration is not None:
            pulumi.set(__self__, "login_validity_duration", login_validity_duration)
        if name_assertion is not None:
            pulumi.set(__self__, "name_assertion", name_assertion)
        if org_assertion is not None:
            pulumi.set(__self__, "org_assertion", org_assertion)
        if role_assertion is not None:
            pulumi.set(__self__, "role_assertion", role_assertion)

    @property
    @pulumi.getter(name="editorRoleValues")
    def editor_role_values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The editor role values.
        """
        return pulumi.get(self, "editor_role_values")

    @editor_role_values.setter
    def editor_role_values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "editor_role_values", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Input[str]:
        """
        The workspace id.

        The following arguments are optional:
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="adminRoleValues")
    def admin_role_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The admin role values.
        """
        return pulumi.get(self, "admin_role_values")

    @admin_role_values.setter
    def admin_role_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "admin_role_values", value)

    @property
    @pulumi.getter(name="allowedOrganizations")
    def allowed_organizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The allowed organizations.
        """
        return pulumi.get(self, "allowed_organizations")

    @allowed_organizations.setter
    def allowed_organizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_organizations", value)

    @property
    @pulumi.getter(name="emailAssertion")
    def email_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The email assertion.
        """
        return pulumi.get(self, "email_assertion")

    @email_assertion.setter
    def email_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_assertion", value)

    @property
    @pulumi.getter(name="groupsAssertion")
    def groups_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The groups assertion.
        """
        return pulumi.get(self, "groups_assertion")

    @groups_assertion.setter
    def groups_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "groups_assertion", value)

    @property
    @pulumi.getter(name="idpMetadataUrl")
    def idp_metadata_url(self) -> Optional[pulumi.Input[str]]:
        """
        The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_url")

    @idp_metadata_url.setter
    def idp_metadata_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_metadata_url", value)

    @property
    @pulumi.getter(name="idpMetadataXml")
    def idp_metadata_xml(self) -> Optional[pulumi.Input[str]]:
        """
        The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_xml")

    @idp_metadata_xml.setter
    def idp_metadata_xml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_metadata_xml", value)

    @property
    @pulumi.getter(name="loginAssertion")
    def login_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The login assertion.
        """
        return pulumi.get(self, "login_assertion")

    @login_assertion.setter
    def login_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "login_assertion", value)

    @property
    @pulumi.getter(name="loginValidityDuration")
    def login_validity_duration(self) -> Optional[pulumi.Input[int]]:
        """
        The login validity duration.
        """
        return pulumi.get(self, "login_validity_duration")

    @login_validity_duration.setter
    def login_validity_duration(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "login_validity_duration", value)

    @property
    @pulumi.getter(name="nameAssertion")
    def name_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The name assertion.
        """
        return pulumi.get(self, "name_assertion")

    @name_assertion.setter
    def name_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_assertion", value)

    @property
    @pulumi.getter(name="orgAssertion")
    def org_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The org assertion.
        """
        return pulumi.get(self, "org_assertion")

    @org_assertion.setter
    def org_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_assertion", value)

    @property
    @pulumi.getter(name="roleAssertion")
    def role_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The role assertion.
        """
        return pulumi.get(self, "role_assertion")

    @role_assertion.setter
    def role_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_assertion", value)


@pulumi.input_type
class _WorkspaceSamlConfigurationState:
    def __init__(__self__, *,
                 admin_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 editor_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 email_assertion: Optional[pulumi.Input[str]] = None,
                 groups_assertion: Optional[pulumi.Input[str]] = None,
                 idp_metadata_url: Optional[pulumi.Input[str]] = None,
                 idp_metadata_xml: Optional[pulumi.Input[str]] = None,
                 login_assertion: Optional[pulumi.Input[str]] = None,
                 login_validity_duration: Optional[pulumi.Input[int]] = None,
                 name_assertion: Optional[pulumi.Input[str]] = None,
                 org_assertion: Optional[pulumi.Input[str]] = None,
                 role_assertion: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering WorkspaceSamlConfiguration resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_role_values: The admin role values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_organizations: The allowed organizations.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] editor_role_values: The editor role values.
        :param pulumi.Input[str] email_assertion: The email assertion.
        :param pulumi.Input[str] groups_assertion: The groups assertion.
        :param pulumi.Input[str] idp_metadata_url: The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] idp_metadata_xml: The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] login_assertion: The login assertion.
        :param pulumi.Input[int] login_validity_duration: The login validity duration.
        :param pulumi.Input[str] name_assertion: The name assertion.
        :param pulumi.Input[str] org_assertion: The org assertion.
        :param pulumi.Input[str] role_assertion: The role assertion.
        :param pulumi.Input[str] status: The status of the SAML configuration.
        :param pulumi.Input[str] workspace_id: The workspace id.
               
               The following arguments are optional:
        """
        if admin_role_values is not None:
            pulumi.set(__self__, "admin_role_values", admin_role_values)
        if allowed_organizations is not None:
            pulumi.set(__self__, "allowed_organizations", allowed_organizations)
        if editor_role_values is not None:
            pulumi.set(__self__, "editor_role_values", editor_role_values)
        if email_assertion is not None:
            pulumi.set(__self__, "email_assertion", email_assertion)
        if groups_assertion is not None:
            pulumi.set(__self__, "groups_assertion", groups_assertion)
        if idp_metadata_url is not None:
            pulumi.set(__self__, "idp_metadata_url", idp_metadata_url)
        if idp_metadata_xml is not None:
            pulumi.set(__self__, "idp_metadata_xml", idp_metadata_xml)
        if login_assertion is not None:
            pulumi.set(__self__, "login_assertion", login_assertion)
        if login_validity_duration is not None:
            pulumi.set(__self__, "login_validity_duration", login_validity_duration)
        if name_assertion is not None:
            pulumi.set(__self__, "name_assertion", name_assertion)
        if org_assertion is not None:
            pulumi.set(__self__, "org_assertion", org_assertion)
        if role_assertion is not None:
            pulumi.set(__self__, "role_assertion", role_assertion)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="adminRoleValues")
    def admin_role_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The admin role values.
        """
        return pulumi.get(self, "admin_role_values")

    @admin_role_values.setter
    def admin_role_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "admin_role_values", value)

    @property
    @pulumi.getter(name="allowedOrganizations")
    def allowed_organizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The allowed organizations.
        """
        return pulumi.get(self, "allowed_organizations")

    @allowed_organizations.setter
    def allowed_organizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_organizations", value)

    @property
    @pulumi.getter(name="editorRoleValues")
    def editor_role_values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The editor role values.
        """
        return pulumi.get(self, "editor_role_values")

    @editor_role_values.setter
    def editor_role_values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "editor_role_values", value)

    @property
    @pulumi.getter(name="emailAssertion")
    def email_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The email assertion.
        """
        return pulumi.get(self, "email_assertion")

    @email_assertion.setter
    def email_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_assertion", value)

    @property
    @pulumi.getter(name="groupsAssertion")
    def groups_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The groups assertion.
        """
        return pulumi.get(self, "groups_assertion")

    @groups_assertion.setter
    def groups_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "groups_assertion", value)

    @property
    @pulumi.getter(name="idpMetadataUrl")
    def idp_metadata_url(self) -> Optional[pulumi.Input[str]]:
        """
        The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_url")

    @idp_metadata_url.setter
    def idp_metadata_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_metadata_url", value)

    @property
    @pulumi.getter(name="idpMetadataXml")
    def idp_metadata_xml(self) -> Optional[pulumi.Input[str]]:
        """
        The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_xml")

    @idp_metadata_xml.setter
    def idp_metadata_xml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idp_metadata_xml", value)

    @property
    @pulumi.getter(name="loginAssertion")
    def login_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The login assertion.
        """
        return pulumi.get(self, "login_assertion")

    @login_assertion.setter
    def login_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "login_assertion", value)

    @property
    @pulumi.getter(name="loginValidityDuration")
    def login_validity_duration(self) -> Optional[pulumi.Input[int]]:
        """
        The login validity duration.
        """
        return pulumi.get(self, "login_validity_duration")

    @login_validity_duration.setter
    def login_validity_duration(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "login_validity_duration", value)

    @property
    @pulumi.getter(name="nameAssertion")
    def name_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The name assertion.
        """
        return pulumi.get(self, "name_assertion")

    @name_assertion.setter
    def name_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_assertion", value)

    @property
    @pulumi.getter(name="orgAssertion")
    def org_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The org assertion.
        """
        return pulumi.get(self, "org_assertion")

    @org_assertion.setter
    def org_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_assertion", value)

    @property
    @pulumi.getter(name="roleAssertion")
    def role_assertion(self) -> Optional[pulumi.Input[str]]:
        """
        The role assertion.
        """
        return pulumi.get(self, "role_assertion")

    @role_assertion.setter
    def role_assertion(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_assertion", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the SAML configuration.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The workspace id.

        The following arguments are optional:
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)


class WorkspaceSamlConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 editor_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 email_assertion: Optional[pulumi.Input[str]] = None,
                 groups_assertion: Optional[pulumi.Input[str]] = None,
                 idp_metadata_url: Optional[pulumi.Input[str]] = None,
                 idp_metadata_xml: Optional[pulumi.Input[str]] = None,
                 login_assertion: Optional[pulumi.Input[str]] = None,
                 login_validity_duration: Optional[pulumi.Input[int]] = None,
                 name_assertion: Optional[pulumi.Input[str]] = None,
                 org_assertion: Optional[pulumi.Input[str]] = None,
                 role_assertion: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Amazon Managed Grafana workspace SAML configuration resource.

        ## Example Usage

        ### Basic configuration

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        assume = aws.iam.Role("assume",
            name="grafana-assume",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "grafana.amazonaws.com",
                    },
                }],
            }))
        example_workspace = aws.grafana.Workspace("example",
            account_access_type="CURRENT_ACCOUNT",
            authentication_providers=["SAML"],
            permission_type="SERVICE_MANAGED",
            role_arn=assume.arn)
        example = aws.grafana.WorkspaceSamlConfiguration("example",
            editor_role_values=["editor"],
            idp_metadata_url="https://my_idp_metadata.url",
            workspace_id=example_workspace.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Grafana Workspace SAML configuration using the workspace's `id`. For example:

        ```sh
        $ pulumi import aws:grafana/workspaceSamlConfiguration:WorkspaceSamlConfiguration example g-2054c75a02
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_role_values: The admin role values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_organizations: The allowed organizations.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] editor_role_values: The editor role values.
        :param pulumi.Input[str] email_assertion: The email assertion.
        :param pulumi.Input[str] groups_assertion: The groups assertion.
        :param pulumi.Input[str] idp_metadata_url: The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] idp_metadata_xml: The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] login_assertion: The login assertion.
        :param pulumi.Input[int] login_validity_duration: The login validity duration.
        :param pulumi.Input[str] name_assertion: The name assertion.
        :param pulumi.Input[str] org_assertion: The org assertion.
        :param pulumi.Input[str] role_assertion: The role assertion.
        :param pulumi.Input[str] workspace_id: The workspace id.
               
               The following arguments are optional:
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkspaceSamlConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Managed Grafana workspace SAML configuration resource.

        ## Example Usage

        ### Basic configuration

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        assume = aws.iam.Role("assume",
            name="grafana-assume",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "grafana.amazonaws.com",
                    },
                }],
            }))
        example_workspace = aws.grafana.Workspace("example",
            account_access_type="CURRENT_ACCOUNT",
            authentication_providers=["SAML"],
            permission_type="SERVICE_MANAGED",
            role_arn=assume.arn)
        example = aws.grafana.WorkspaceSamlConfiguration("example",
            editor_role_values=["editor"],
            idp_metadata_url="https://my_idp_metadata.url",
            workspace_id=example_workspace.id)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import Grafana Workspace SAML configuration using the workspace's `id`. For example:

        ```sh
        $ pulumi import aws:grafana/workspaceSamlConfiguration:WorkspaceSamlConfiguration example g-2054c75a02
        ```

        :param str resource_name: The name of the resource.
        :param WorkspaceSamlConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkspaceSamlConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 editor_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 email_assertion: Optional[pulumi.Input[str]] = None,
                 groups_assertion: Optional[pulumi.Input[str]] = None,
                 idp_metadata_url: Optional[pulumi.Input[str]] = None,
                 idp_metadata_xml: Optional[pulumi.Input[str]] = None,
                 login_assertion: Optional[pulumi.Input[str]] = None,
                 login_validity_duration: Optional[pulumi.Input[int]] = None,
                 name_assertion: Optional[pulumi.Input[str]] = None,
                 org_assertion: Optional[pulumi.Input[str]] = None,
                 role_assertion: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkspaceSamlConfigurationArgs.__new__(WorkspaceSamlConfigurationArgs)

            __props__.__dict__["admin_role_values"] = admin_role_values
            __props__.__dict__["allowed_organizations"] = allowed_organizations
            if editor_role_values is None and not opts.urn:
                raise TypeError("Missing required property 'editor_role_values'")
            __props__.__dict__["editor_role_values"] = editor_role_values
            __props__.__dict__["email_assertion"] = email_assertion
            __props__.__dict__["groups_assertion"] = groups_assertion
            __props__.__dict__["idp_metadata_url"] = idp_metadata_url
            __props__.__dict__["idp_metadata_xml"] = idp_metadata_xml
            __props__.__dict__["login_assertion"] = login_assertion
            __props__.__dict__["login_validity_duration"] = login_validity_duration
            __props__.__dict__["name_assertion"] = name_assertion
            __props__.__dict__["org_assertion"] = org_assertion
            __props__.__dict__["role_assertion"] = role_assertion
            if workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_id'")
            __props__.__dict__["workspace_id"] = workspace_id
            __props__.__dict__["status"] = None
        super(WorkspaceSamlConfiguration, __self__).__init__(
            'aws:grafana/workspaceSamlConfiguration:WorkspaceSamlConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            editor_role_values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            email_assertion: Optional[pulumi.Input[str]] = None,
            groups_assertion: Optional[pulumi.Input[str]] = None,
            idp_metadata_url: Optional[pulumi.Input[str]] = None,
            idp_metadata_xml: Optional[pulumi.Input[str]] = None,
            login_assertion: Optional[pulumi.Input[str]] = None,
            login_validity_duration: Optional[pulumi.Input[int]] = None,
            name_assertion: Optional[pulumi.Input[str]] = None,
            org_assertion: Optional[pulumi.Input[str]] = None,
            role_assertion: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            workspace_id: Optional[pulumi.Input[str]] = None) -> 'WorkspaceSamlConfiguration':
        """
        Get an existing WorkspaceSamlConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin_role_values: The admin role values.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_organizations: The allowed organizations.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] editor_role_values: The editor role values.
        :param pulumi.Input[str] email_assertion: The email assertion.
        :param pulumi.Input[str] groups_assertion: The groups assertion.
        :param pulumi.Input[str] idp_metadata_url: The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] idp_metadata_xml: The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        :param pulumi.Input[str] login_assertion: The login assertion.
        :param pulumi.Input[int] login_validity_duration: The login validity duration.
        :param pulumi.Input[str] name_assertion: The name assertion.
        :param pulumi.Input[str] org_assertion: The org assertion.
        :param pulumi.Input[str] role_assertion: The role assertion.
        :param pulumi.Input[str] status: The status of the SAML configuration.
        :param pulumi.Input[str] workspace_id: The workspace id.
               
               The following arguments are optional:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WorkspaceSamlConfigurationState.__new__(_WorkspaceSamlConfigurationState)

        __props__.__dict__["admin_role_values"] = admin_role_values
        __props__.__dict__["allowed_organizations"] = allowed_organizations
        __props__.__dict__["editor_role_values"] = editor_role_values
        __props__.__dict__["email_assertion"] = email_assertion
        __props__.__dict__["groups_assertion"] = groups_assertion
        __props__.__dict__["idp_metadata_url"] = idp_metadata_url
        __props__.__dict__["idp_metadata_xml"] = idp_metadata_xml
        __props__.__dict__["login_assertion"] = login_assertion
        __props__.__dict__["login_validity_duration"] = login_validity_duration
        __props__.__dict__["name_assertion"] = name_assertion
        __props__.__dict__["org_assertion"] = org_assertion
        __props__.__dict__["role_assertion"] = role_assertion
        __props__.__dict__["status"] = status
        __props__.__dict__["workspace_id"] = workspace_id
        return WorkspaceSamlConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adminRoleValues")
    def admin_role_values(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The admin role values.
        """
        return pulumi.get(self, "admin_role_values")

    @property
    @pulumi.getter(name="allowedOrganizations")
    def allowed_organizations(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The allowed organizations.
        """
        return pulumi.get(self, "allowed_organizations")

    @property
    @pulumi.getter(name="editorRoleValues")
    def editor_role_values(self) -> pulumi.Output[Sequence[str]]:
        """
        The editor role values.
        """
        return pulumi.get(self, "editor_role_values")

    @property
    @pulumi.getter(name="emailAssertion")
    def email_assertion(self) -> pulumi.Output[str]:
        """
        The email assertion.
        """
        return pulumi.get(self, "email_assertion")

    @property
    @pulumi.getter(name="groupsAssertion")
    def groups_assertion(self) -> pulumi.Output[Optional[str]]:
        """
        The groups assertion.
        """
        return pulumi.get(self, "groups_assertion")

    @property
    @pulumi.getter(name="idpMetadataUrl")
    def idp_metadata_url(self) -> pulumi.Output[Optional[str]]:
        """
        The IDP Metadata URL. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_url")

    @property
    @pulumi.getter(name="idpMetadataXml")
    def idp_metadata_xml(self) -> pulumi.Output[Optional[str]]:
        """
        The IDP Metadata XML. Note that either `idp_metadata_url` or `idp_metadata_xml` (but not both) must be specified.
        """
        return pulumi.get(self, "idp_metadata_xml")

    @property
    @pulumi.getter(name="loginAssertion")
    def login_assertion(self) -> pulumi.Output[str]:
        """
        The login assertion.
        """
        return pulumi.get(self, "login_assertion")

    @property
    @pulumi.getter(name="loginValidityDuration")
    def login_validity_duration(self) -> pulumi.Output[int]:
        """
        The login validity duration.
        """
        return pulumi.get(self, "login_validity_duration")

    @property
    @pulumi.getter(name="nameAssertion")
    def name_assertion(self) -> pulumi.Output[str]:
        """
        The name assertion.
        """
        return pulumi.get(self, "name_assertion")

    @property
    @pulumi.getter(name="orgAssertion")
    def org_assertion(self) -> pulumi.Output[Optional[str]]:
        """
        The org assertion.
        """
        return pulumi.get(self, "org_assertion")

    @property
    @pulumi.getter(name="roleAssertion")
    def role_assertion(self) -> pulumi.Output[Optional[str]]:
        """
        The role assertion.
        """
        return pulumi.get(self, "role_assertion")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the SAML configuration.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The workspace id.

        The following arguments are optional:
        """
        return pulumi.get(self, "workspace_id")

