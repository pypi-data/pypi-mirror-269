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
    'GetCodeSigningConfigResult',
    'AwaitableGetCodeSigningConfigResult',
    'get_code_signing_config',
    'get_code_signing_config_output',
]

@pulumi.output_type
class GetCodeSigningConfigResult:
    """
    A collection of values returned by getCodeSigningConfig.
    """
    def __init__(__self__, allowed_publishers=None, arn=None, config_id=None, description=None, id=None, last_modified=None, policies=None):
        if allowed_publishers and not isinstance(allowed_publishers, list):
            raise TypeError("Expected argument 'allowed_publishers' to be a list")
        pulumi.set(__self__, "allowed_publishers", allowed_publishers)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if config_id and not isinstance(config_id, str):
            raise TypeError("Expected argument 'config_id' to be a str")
        pulumi.set(__self__, "config_id", config_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if policies and not isinstance(policies, list):
            raise TypeError("Expected argument 'policies' to be a list")
        pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter(name="allowedPublishers")
    def allowed_publishers(self) -> Sequence['outputs.GetCodeSigningConfigAllowedPublisherResult']:
        """
        List of allowed publishers as signing profiles for this code signing configuration.
        """
        return pulumi.get(self, "allowed_publishers")

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> str:
        """
        Unique identifier for the code signing configuration.
        """
        return pulumi.get(self, "config_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Code signing configuration description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        Date and time that the code signing configuration was last modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def policies(self) -> Sequence['outputs.GetCodeSigningConfigPolicyResult']:
        """
        List of code signing policies that control the validation failure action for signature mismatch or expiry.
        """
        return pulumi.get(self, "policies")


class AwaitableGetCodeSigningConfigResult(GetCodeSigningConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCodeSigningConfigResult(
            allowed_publishers=self.allowed_publishers,
            arn=self.arn,
            config_id=self.config_id,
            description=self.description,
            id=self.id,
            last_modified=self.last_modified,
            policies=self.policies)


def get_code_signing_config(arn: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCodeSigningConfigResult:
    """
    Provides information about a Lambda Code Signing Config. A code signing configuration defines a list of allowed signing profiles and defines the code-signing validation policy (action to be taken if deployment validation checks fail).

    For information about Lambda code signing configurations and how to use them, see [configuring code signing for Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html)

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    existing_csc = aws.lambda.get_code_signing_config(arn=f"arn:aws:lambda:{aws_region}:{aws_account}:code-signing-config:csc-0f6c334abcdea4d8b")
    ```
    <!--End PulumiCodeChooser -->


    :param str arn: ARN of the code signing configuration.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:lambda/getCodeSigningConfig:getCodeSigningConfig', __args__, opts=opts, typ=GetCodeSigningConfigResult).value

    return AwaitableGetCodeSigningConfigResult(
        allowed_publishers=pulumi.get(__ret__, 'allowed_publishers'),
        arn=pulumi.get(__ret__, 'arn'),
        config_id=pulumi.get(__ret__, 'config_id'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        last_modified=pulumi.get(__ret__, 'last_modified'),
        policies=pulumi.get(__ret__, 'policies'))


@_utilities.lift_output_func(get_code_signing_config)
def get_code_signing_config_output(arn: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCodeSigningConfigResult]:
    """
    Provides information about a Lambda Code Signing Config. A code signing configuration defines a list of allowed signing profiles and defines the code-signing validation policy (action to be taken if deployment validation checks fail).

    For information about Lambda code signing configurations and how to use them, see [configuring code signing for Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html)

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    existing_csc = aws.lambda.get_code_signing_config(arn=f"arn:aws:lambda:{aws_region}:{aws_account}:code-signing-config:csc-0f6c334abcdea4d8b")
    ```
    <!--End PulumiCodeChooser -->


    :param str arn: ARN of the code signing configuration.
    """
    ...
