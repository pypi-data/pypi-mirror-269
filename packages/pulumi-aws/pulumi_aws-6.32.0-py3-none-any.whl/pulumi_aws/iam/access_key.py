# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccessKeyArgs', 'AccessKey']

@pulumi.input_type
class AccessKeyArgs:
    def __init__(__self__, *,
                 user: pulumi.Input[str],
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AccessKey resource.
        :param pulumi.Input[str] user: IAM user to associate with this access key.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        :param pulumi.Input[str] status: Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        """
        pulumi.set(__self__, "user", user)
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def user(self) -> pulumi.Input[str]:
        """
        IAM user to associate with this access key.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: pulumi.Input[str]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _AccessKeyState:
    def __init__(__self__, *,
                 create_date: Optional[pulumi.Input[str]] = None,
                 encrypted_secret: Optional[pulumi.Input[str]] = None,
                 encrypted_ses_smtp_password_v4: Optional[pulumi.Input[str]] = None,
                 key_fingerprint: Optional[pulumi.Input[str]] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 secret: Optional[pulumi.Input[str]] = None,
                 ses_smtp_password_v4: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccessKey resources.
        :param pulumi.Input[str] create_date: Date and time in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8) that the access key was created.
        :param pulumi.Input[str] encrypted_secret: Encrypted secret, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted secret may be decrypted using the command line.
        :param pulumi.Input[str] encrypted_ses_smtp_password_v4: Encrypted SES SMTP password, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted password may be decrypted using the command line.
        :param pulumi.Input[str] key_fingerprint: Fingerprint of the PGP key used to encrypt the secret. This attribute is not available for imported resources.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        :param pulumi.Input[str] secret: Secret access key. This attribute is not available for imported resources. Note that this will be written to the state file. If you use this, please protect your backend state file judiciously. Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext, at the cost of preventing the use of the secret key in automation.
        :param pulumi.Input[str] ses_smtp_password_v4: Secret access key converted into an SES SMTP password by applying [AWS's documented Sigv4 conversion algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert). This attribute is not available for imported resources. As SigV4 is region specific, valid Provider regions are `ap-south-1`, `ap-southeast-2`, `eu-central-1`, `eu-west-1`, `us-east-1` and `us-west-2`. See current [AWS SES regions](https://docs.aws.amazon.com/general/latest/gr/rande.html#ses_region).
        :param pulumi.Input[str] status: Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        :param pulumi.Input[str] user: IAM user to associate with this access key.
        """
        if create_date is not None:
            pulumi.set(__self__, "create_date", create_date)
        if encrypted_secret is not None:
            pulumi.set(__self__, "encrypted_secret", encrypted_secret)
        if encrypted_ses_smtp_password_v4 is not None:
            pulumi.set(__self__, "encrypted_ses_smtp_password_v4", encrypted_ses_smtp_password_v4)
        if key_fingerprint is not None:
            pulumi.set(__self__, "key_fingerprint", key_fingerprint)
        if pgp_key is not None:
            pulumi.set(__self__, "pgp_key", pgp_key)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)
        if ses_smtp_password_v4 is not None:
            pulumi.set(__self__, "ses_smtp_password_v4", ses_smtp_password_v4)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> Optional[pulumi.Input[str]]:
        """
        Date and time in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8) that the access key was created.
        """
        return pulumi.get(self, "create_date")

    @create_date.setter
    def create_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_date", value)

    @property
    @pulumi.getter(name="encryptedSecret")
    def encrypted_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Encrypted secret, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted secret may be decrypted using the command line.
        """
        return pulumi.get(self, "encrypted_secret")

    @encrypted_secret.setter
    def encrypted_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted_secret", value)

    @property
    @pulumi.getter(name="encryptedSesSmtpPasswordV4")
    def encrypted_ses_smtp_password_v4(self) -> Optional[pulumi.Input[str]]:
        """
        Encrypted SES SMTP password, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted password may be decrypted using the command line.
        """
        return pulumi.get(self, "encrypted_ses_smtp_password_v4")

    @encrypted_ses_smtp_password_v4.setter
    def encrypted_ses_smtp_password_v4(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted_ses_smtp_password_v4", value)

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        Fingerprint of the PGP key used to encrypt the secret. This attribute is not available for imported resources.
        """
        return pulumi.get(self, "key_fingerprint")

    @key_fingerprint.setter
    def key_fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_fingerprint", value)

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> Optional[pulumi.Input[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        """
        return pulumi.get(self, "pgp_key")

    @pgp_key.setter
    def pgp_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pgp_key", value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[str]]:
        """
        Secret access key. This attribute is not available for imported resources. Note that this will be written to the state file. If you use this, please protect your backend state file judiciously. Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext, at the cost of preventing the use of the secret key in automation.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret", value)

    @property
    @pulumi.getter(name="sesSmtpPasswordV4")
    def ses_smtp_password_v4(self) -> Optional[pulumi.Input[str]]:
        """
        Secret access key converted into an SES SMTP password by applying [AWS's documented Sigv4 conversion algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert). This attribute is not available for imported resources. As SigV4 is region specific, valid Provider regions are `ap-south-1`, `ap-southeast-2`, `eu-central-1`, `eu-west-1`, `us-east-1` and `us-west-2`. See current [AWS SES regions](https://docs.aws.amazon.com/general/latest/gr/rande.html#ses_region).
        """
        return pulumi.get(self, "ses_smtp_password_v4")

    @ses_smtp_password_v4.setter
    def ses_smtp_password_v4(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ses_smtp_password_v4", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        IAM user to associate with this access key.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class AccessKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an IAM access key. This is a set of credentials that allow API requests to be made as an IAM user.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        lb_user = aws.iam.User("lb",
            name="loadbalancer",
            path="/system/")
        lb = aws.iam.AccessKey("lb",
            user=lb_user.name,
            pgp_key="keybase:some_person_that_exists")
        lb_ro = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=["ec2:Describe*"],
            resources=["*"],
        )])
        lb_ro_user_policy = aws.iam.UserPolicy("lb_ro",
            name="test",
            user=lb_user.name,
            policy=lb_ro.json)
        pulumi.export("secret", lb.encrypted_secret)
        ```
        <!--End PulumiCodeChooser -->

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.iam.User("test",
            name="test",
            path="/test/")
        test_access_key = aws.iam.AccessKey("test", user=test.name)
        pulumi.export("awsIamSmtpPasswordV4", test_access_key.ses_smtp_password_v4)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import IAM Access Keys using the identifier. For example:

        ```sh
        $ pulumi import aws:iam/accessKey:AccessKey example AKIA1234567890
        ```
        Resource attributes such as `encrypted_secret`, `key_fingerprint`, `pgp_key`, `secret`, `ses_smtp_password_v4`, and `encrypted_ses_smtp_password_v4` are not available for imported resources as this information cannot be read from the IAM API.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        :param pulumi.Input[str] status: Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        :param pulumi.Input[str] user: IAM user to associate with this access key.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an IAM access key. This is a set of credentials that allow API requests to be made as an IAM user.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        lb_user = aws.iam.User("lb",
            name="loadbalancer",
            path="/system/")
        lb = aws.iam.AccessKey("lb",
            user=lb_user.name,
            pgp_key="keybase:some_person_that_exists")
        lb_ro = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=["ec2:Describe*"],
            resources=["*"],
        )])
        lb_ro_user_policy = aws.iam.UserPolicy("lb_ro",
            name="test",
            user=lb_user.name,
            policy=lb_ro.json)
        pulumi.export("secret", lb.encrypted_secret)
        ```
        <!--End PulumiCodeChooser -->

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.iam.User("test",
            name="test",
            path="/test/")
        test_access_key = aws.iam.AccessKey("test", user=test.name)
        pulumi.export("awsIamSmtpPasswordV4", test_access_key.ses_smtp_password_v4)
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Using `pulumi import`, import IAM Access Keys using the identifier. For example:

        ```sh
        $ pulumi import aws:iam/accessKey:AccessKey example AKIA1234567890
        ```
        Resource attributes such as `encrypted_secret`, `key_fingerprint`, `pgp_key`, `secret`, `ses_smtp_password_v4`, and `encrypted_ses_smtp_password_v4` are not available for imported resources as this information cannot be read from the IAM API.

        :param str resource_name: The name of the resource.
        :param AccessKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pgp_key: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessKeyArgs.__new__(AccessKeyArgs)

            __props__.__dict__["pgp_key"] = pgp_key
            __props__.__dict__["status"] = status
            if user is None and not opts.urn:
                raise TypeError("Missing required property 'user'")
            __props__.__dict__["user"] = user
            __props__.__dict__["create_date"] = None
            __props__.__dict__["encrypted_secret"] = None
            __props__.__dict__["encrypted_ses_smtp_password_v4"] = None
            __props__.__dict__["key_fingerprint"] = None
            __props__.__dict__["secret"] = None
            __props__.__dict__["ses_smtp_password_v4"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["secret", "sesSmtpPasswordV4"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(AccessKey, __self__).__init__(
            'aws:iam/accessKey:AccessKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_date: Optional[pulumi.Input[str]] = None,
            encrypted_secret: Optional[pulumi.Input[str]] = None,
            encrypted_ses_smtp_password_v4: Optional[pulumi.Input[str]] = None,
            key_fingerprint: Optional[pulumi.Input[str]] = None,
            pgp_key: Optional[pulumi.Input[str]] = None,
            secret: Optional[pulumi.Input[str]] = None,
            ses_smtp_password_v4: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None) -> 'AccessKey':
        """
        Get an existing AccessKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_date: Date and time in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8) that the access key was created.
        :param pulumi.Input[str] encrypted_secret: Encrypted secret, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted secret may be decrypted using the command line.
        :param pulumi.Input[str] encrypted_ses_smtp_password_v4: Encrypted SES SMTP password, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted password may be decrypted using the command line.
        :param pulumi.Input[str] key_fingerprint: Fingerprint of the PGP key used to encrypt the secret. This attribute is not available for imported resources.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        :param pulumi.Input[str] secret: Secret access key. This attribute is not available for imported resources. Note that this will be written to the state file. If you use this, please protect your backend state file judiciously. Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext, at the cost of preventing the use of the secret key in automation.
        :param pulumi.Input[str] ses_smtp_password_v4: Secret access key converted into an SES SMTP password by applying [AWS's documented Sigv4 conversion algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert). This attribute is not available for imported resources. As SigV4 is region specific, valid Provider regions are `ap-south-1`, `ap-southeast-2`, `eu-central-1`, `eu-west-1`, `us-east-1` and `us-west-2`. See current [AWS SES regions](https://docs.aws.amazon.com/general/latest/gr/rande.html#ses_region).
        :param pulumi.Input[str] status: Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        :param pulumi.Input[str] user: IAM user to associate with this access key.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessKeyState.__new__(_AccessKeyState)

        __props__.__dict__["create_date"] = create_date
        __props__.__dict__["encrypted_secret"] = encrypted_secret
        __props__.__dict__["encrypted_ses_smtp_password_v4"] = encrypted_ses_smtp_password_v4
        __props__.__dict__["key_fingerprint"] = key_fingerprint
        __props__.__dict__["pgp_key"] = pgp_key
        __props__.__dict__["secret"] = secret
        __props__.__dict__["ses_smtp_password_v4"] = ses_smtp_password_v4
        __props__.__dict__["status"] = status
        __props__.__dict__["user"] = user
        return AccessKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> pulumi.Output[str]:
        """
        Date and time in [RFC3339 format](https://tools.ietf.org/html/rfc3339#section-5.8) that the access key was created.
        """
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter(name="encryptedSecret")
    def encrypted_secret(self) -> pulumi.Output[str]:
        """
        Encrypted secret, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted secret may be decrypted using the command line.
        """
        return pulumi.get(self, "encrypted_secret")

    @property
    @pulumi.getter(name="encryptedSesSmtpPasswordV4")
    def encrypted_ses_smtp_password_v4(self) -> pulumi.Output[str]:
        """
        Encrypted SES SMTP password, base64 encoded, if `pgp_key` was specified. This attribute is not available for imported resources. The encrypted password may be decrypted using the command line.
        """
        return pulumi.get(self, "encrypted_ses_smtp_password_v4")

    @property
    @pulumi.getter(name="keyFingerprint")
    def key_fingerprint(self) -> pulumi.Output[str]:
        """
        Fingerprint of the PGP key used to encrypt the secret. This attribute is not available for imported resources.
        """
        return pulumi.get(self, "key_fingerprint")

    @property
    @pulumi.getter(name="pgpKey")
    def pgp_key(self) -> pulumi.Output[Optional[str]]:
        """
        Either a base-64 encoded PGP public key, or a keybase username in the form `keybase:some_person_that_exists`, for use in the `encrypted_secret` output attribute. If providing a base-64 encoded PGP public key, make sure to provide the "raw" version and not the "armored" one (e.g. avoid passing the `-a` option to `gpg --export`).
        """
        return pulumi.get(self, "pgp_key")

    @property
    @pulumi.getter
    def secret(self) -> pulumi.Output[str]:
        """
        Secret access key. This attribute is not available for imported resources. Note that this will be written to the state file. If you use this, please protect your backend state file judiciously. Alternatively, you may supply a `pgp_key` instead, which will prevent the secret from being stored in plaintext, at the cost of preventing the use of the secret key in automation.
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter(name="sesSmtpPasswordV4")
    def ses_smtp_password_v4(self) -> pulumi.Output[str]:
        """
        Secret access key converted into an SES SMTP password by applying [AWS's documented Sigv4 conversion algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert). This attribute is not available for imported resources. As SigV4 is region specific, valid Provider regions are `ap-south-1`, `ap-southeast-2`, `eu-central-1`, `eu-west-1`, `us-east-1` and `us-west-2`. See current [AWS SES regions](https://docs.aws.amazon.com/general/latest/gr/rande.html#ses_region).
        """
        return pulumi.get(self, "ses_smtp_password_v4")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Access key status to apply. Defaults to `Active`. Valid values are `Active` and `Inactive`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        IAM user to associate with this access key.
        """
        return pulumi.get(self, "user")

