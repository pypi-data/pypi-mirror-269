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
    'GetObjectResult',
    'AwaitableGetObjectResult',
    'get_object',
    'get_object_output',
]

@pulumi.output_type
class GetObjectResult:
    """
    A collection of values returned by getObject.
    """
    def __init__(__self__, arn=None, body=None, bucket=None, bucket_key_enabled=None, cache_control=None, checksum_crc32=None, checksum_crc32c=None, checksum_mode=None, checksum_sha1=None, checksum_sha256=None, content_disposition=None, content_encoding=None, content_language=None, content_length=None, content_type=None, etag=None, expiration=None, expires=None, id=None, key=None, last_modified=None, metadata=None, object_lock_legal_hold_status=None, object_lock_mode=None, object_lock_retain_until_date=None, range=None, server_side_encryption=None, sse_kms_key_id=None, storage_class=None, tags=None, version_id=None, website_redirect_location=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if body and not isinstance(body, str):
            raise TypeError("Expected argument 'body' to be a str")
        pulumi.set(__self__, "body", body)
        if bucket and not isinstance(bucket, str):
            raise TypeError("Expected argument 'bucket' to be a str")
        pulumi.set(__self__, "bucket", bucket)
        if bucket_key_enabled and not isinstance(bucket_key_enabled, bool):
            raise TypeError("Expected argument 'bucket_key_enabled' to be a bool")
        pulumi.set(__self__, "bucket_key_enabled", bucket_key_enabled)
        if cache_control and not isinstance(cache_control, str):
            raise TypeError("Expected argument 'cache_control' to be a str")
        pulumi.set(__self__, "cache_control", cache_control)
        if checksum_crc32 and not isinstance(checksum_crc32, str):
            raise TypeError("Expected argument 'checksum_crc32' to be a str")
        pulumi.set(__self__, "checksum_crc32", checksum_crc32)
        if checksum_crc32c and not isinstance(checksum_crc32c, str):
            raise TypeError("Expected argument 'checksum_crc32c' to be a str")
        pulumi.set(__self__, "checksum_crc32c", checksum_crc32c)
        if checksum_mode and not isinstance(checksum_mode, str):
            raise TypeError("Expected argument 'checksum_mode' to be a str")
        pulumi.set(__self__, "checksum_mode", checksum_mode)
        if checksum_sha1 and not isinstance(checksum_sha1, str):
            raise TypeError("Expected argument 'checksum_sha1' to be a str")
        pulumi.set(__self__, "checksum_sha1", checksum_sha1)
        if checksum_sha256 and not isinstance(checksum_sha256, str):
            raise TypeError("Expected argument 'checksum_sha256' to be a str")
        pulumi.set(__self__, "checksum_sha256", checksum_sha256)
        if content_disposition and not isinstance(content_disposition, str):
            raise TypeError("Expected argument 'content_disposition' to be a str")
        pulumi.set(__self__, "content_disposition", content_disposition)
        if content_encoding and not isinstance(content_encoding, str):
            raise TypeError("Expected argument 'content_encoding' to be a str")
        pulumi.set(__self__, "content_encoding", content_encoding)
        if content_language and not isinstance(content_language, str):
            raise TypeError("Expected argument 'content_language' to be a str")
        pulumi.set(__self__, "content_language", content_language)
        if content_length and not isinstance(content_length, int):
            raise TypeError("Expected argument 'content_length' to be a int")
        pulumi.set(__self__, "content_length", content_length)
        if content_type and not isinstance(content_type, str):
            raise TypeError("Expected argument 'content_type' to be a str")
        pulumi.set(__self__, "content_type", content_type)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if expiration and not isinstance(expiration, str):
            raise TypeError("Expected argument 'expiration' to be a str")
        pulumi.set(__self__, "expiration", expiration)
        if expires and not isinstance(expires, str):
            raise TypeError("Expected argument 'expires' to be a str")
        pulumi.set(__self__, "expires", expires)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if object_lock_legal_hold_status and not isinstance(object_lock_legal_hold_status, str):
            raise TypeError("Expected argument 'object_lock_legal_hold_status' to be a str")
        pulumi.set(__self__, "object_lock_legal_hold_status", object_lock_legal_hold_status)
        if object_lock_mode and not isinstance(object_lock_mode, str):
            raise TypeError("Expected argument 'object_lock_mode' to be a str")
        pulumi.set(__self__, "object_lock_mode", object_lock_mode)
        if object_lock_retain_until_date and not isinstance(object_lock_retain_until_date, str):
            raise TypeError("Expected argument 'object_lock_retain_until_date' to be a str")
        pulumi.set(__self__, "object_lock_retain_until_date", object_lock_retain_until_date)
        if range and not isinstance(range, str):
            raise TypeError("Expected argument 'range' to be a str")
        pulumi.set(__self__, "range", range)
        if server_side_encryption and not isinstance(server_side_encryption, str):
            raise TypeError("Expected argument 'server_side_encryption' to be a str")
        pulumi.set(__self__, "server_side_encryption", server_side_encryption)
        if sse_kms_key_id and not isinstance(sse_kms_key_id, str):
            raise TypeError("Expected argument 'sse_kms_key_id' to be a str")
        pulumi.set(__self__, "sse_kms_key_id", sse_kms_key_id)
        if storage_class and not isinstance(storage_class, str):
            raise TypeError("Expected argument 'storage_class' to be a str")
        pulumi.set(__self__, "storage_class", storage_class)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if version_id and not isinstance(version_id, str):
            raise TypeError("Expected argument 'version_id' to be a str")
        pulumi.set(__self__, "version_id", version_id)
        if website_redirect_location and not isinstance(website_redirect_location, str):
            raise TypeError("Expected argument 'website_redirect_location' to be a str")
        pulumi.set(__self__, "website_redirect_location", website_redirect_location)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the object.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def body(self) -> str:
        """
        Object data (see **limitations above** to understand cases in which this field is actually available)
        """
        return pulumi.get(self, "body")

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="bucketKeyEnabled")
    def bucket_key_enabled(self) -> bool:
        """
        (Optional) Whether or not to use [Amazon S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html) for SSE-KMS.
        """
        return pulumi.get(self, "bucket_key_enabled")

    @property
    @pulumi.getter(name="cacheControl")
    def cache_control(self) -> str:
        """
        Caching behavior along the request/reply chain.
        """
        return pulumi.get(self, "cache_control")

    @property
    @pulumi.getter(name="checksumCrc32")
    def checksum_crc32(self) -> str:
        """
        The base64-encoded, 32-bit CRC32 checksum of the object.
        """
        return pulumi.get(self, "checksum_crc32")

    @property
    @pulumi.getter(name="checksumCrc32c")
    def checksum_crc32c(self) -> str:
        """
        The base64-encoded, 32-bit CRC32C checksum of the object.
        """
        return pulumi.get(self, "checksum_crc32c")

    @property
    @pulumi.getter(name="checksumMode")
    def checksum_mode(self) -> Optional[str]:
        return pulumi.get(self, "checksum_mode")

    @property
    @pulumi.getter(name="checksumSha1")
    def checksum_sha1(self) -> str:
        """
        The base64-encoded, 160-bit SHA-1 digest of the object.
        """
        return pulumi.get(self, "checksum_sha1")

    @property
    @pulumi.getter(name="checksumSha256")
    def checksum_sha256(self) -> str:
        """
        The base64-encoded, 256-bit SHA-256 digest of the object.
        """
        return pulumi.get(self, "checksum_sha256")

    @property
    @pulumi.getter(name="contentDisposition")
    def content_disposition(self) -> str:
        """
        Presentational information for the object.
        """
        return pulumi.get(self, "content_disposition")

    @property
    @pulumi.getter(name="contentEncoding")
    def content_encoding(self) -> str:
        """
        What content encodings have been applied to the object and thus what decoding mechanisms must be applied to obtain the media-type referenced by the Content-Type header field.
        """
        return pulumi.get(self, "content_encoding")

    @property
    @pulumi.getter(name="contentLanguage")
    def content_language(self) -> str:
        """
        Language the content is in.
        """
        return pulumi.get(self, "content_language")

    @property
    @pulumi.getter(name="contentLength")
    def content_length(self) -> int:
        """
        Size of the body in bytes.
        """
        return pulumi.get(self, "content_length")

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> str:
        """
        Standard MIME type describing the format of the object data.
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        [ETag](https://en.wikipedia.org/wiki/HTTP_ETag) generated for the object (an MD5 sum of the object content in case it's not encrypted)
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def expiration(self) -> str:
        """
        If the object expiration is configured (see [object lifecycle management](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html)), the field includes this header. It includes the expiry-date and rule-id key value pairs providing object expiration information. The value of the rule-id is URL encoded.
        """
        return pulumi.get(self, "expiration")

    @property
    @pulumi.getter
    def expires(self) -> str:
        """
        Date and time at which the object is no longer cacheable.
        """
        return pulumi.get(self, "expires")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        Last modified date of the object in RFC1123 format (e.g., `Mon, 02 Jan 2006 15:04:05 MST`)
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def metadata(self) -> Mapping[str, str]:
        """
        Map of metadata stored with the object in S3. Keys are always returned in lowercase.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter(name="objectLockLegalHoldStatus")
    def object_lock_legal_hold_status(self) -> str:
        """
        Indicates whether this object has an active [legal hold](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html#object-lock-legal-holds). This field is only returned if you have permission to view an object's legal hold status.
        """
        return pulumi.get(self, "object_lock_legal_hold_status")

    @property
    @pulumi.getter(name="objectLockMode")
    def object_lock_mode(self) -> str:
        """
        Object lock [retention mode](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html#object-lock-retention-modes) currently in place for this object.
        """
        return pulumi.get(self, "object_lock_mode")

    @property
    @pulumi.getter(name="objectLockRetainUntilDate")
    def object_lock_retain_until_date(self) -> str:
        """
        The date and time when this object's object lock will expire.
        """
        return pulumi.get(self, "object_lock_retain_until_date")

    @property
    @pulumi.getter
    def range(self) -> Optional[str]:
        return pulumi.get(self, "range")

    @property
    @pulumi.getter(name="serverSideEncryption")
    def server_side_encryption(self) -> str:
        """
        If the object is stored using server-side encryption (KMS or Amazon S3-managed encryption key), this field includes the chosen encryption and algorithm used.
        """
        return pulumi.get(self, "server_side_encryption")

    @property
    @pulumi.getter(name="sseKmsKeyId")
    def sse_kms_key_id(self) -> str:
        """
        If present, specifies the ID of the Key Management Service (KMS) master encryption key that was used for the object.
        """
        return pulumi.get(self, "sse_kms_key_id")

    @property
    @pulumi.getter(name="storageClass")
    def storage_class(self) -> str:
        """
        [Storage class](http://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html) information of the object. Available for all objects except for `Standard` storage class objects.
        """
        return pulumi.get(self, "storage_class")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags assigned to the object.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> str:
        """
        Latest version ID of the object returned.
        """
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter(name="websiteRedirectLocation")
    def website_redirect_location(self) -> str:
        """
        If the bucket is configured as a website, redirects requests for this object to another object in the same bucket or to an external URL. Amazon S3 stores the value of this header in the object metadata.
        """
        return pulumi.get(self, "website_redirect_location")


class AwaitableGetObjectResult(GetObjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetObjectResult(
            arn=self.arn,
            body=self.body,
            bucket=self.bucket,
            bucket_key_enabled=self.bucket_key_enabled,
            cache_control=self.cache_control,
            checksum_crc32=self.checksum_crc32,
            checksum_crc32c=self.checksum_crc32c,
            checksum_mode=self.checksum_mode,
            checksum_sha1=self.checksum_sha1,
            checksum_sha256=self.checksum_sha256,
            content_disposition=self.content_disposition,
            content_encoding=self.content_encoding,
            content_language=self.content_language,
            content_length=self.content_length,
            content_type=self.content_type,
            etag=self.etag,
            expiration=self.expiration,
            expires=self.expires,
            id=self.id,
            key=self.key,
            last_modified=self.last_modified,
            metadata=self.metadata,
            object_lock_legal_hold_status=self.object_lock_legal_hold_status,
            object_lock_mode=self.object_lock_mode,
            object_lock_retain_until_date=self.object_lock_retain_until_date,
            range=self.range,
            server_side_encryption=self.server_side_encryption,
            sse_kms_key_id=self.sse_kms_key_id,
            storage_class=self.storage_class,
            tags=self.tags,
            version_id=self.version_id,
            website_redirect_location=self.website_redirect_location)


def get_object(bucket: Optional[str] = None,
               checksum_mode: Optional[str] = None,
               key: Optional[str] = None,
               range: Optional[str] = None,
               tags: Optional[Mapping[str, str]] = None,
               version_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetObjectResult:
    """
    The S3 object data source allows access to the metadata and
    _optionally_ (see below) content of an object stored inside S3 bucket.

    > **Note:** The content of an object (`body` field) is available only for objects which have a human-readable `Content-Type` (`text/*` and `application/json`). This is to prevent printing unsafe characters and potentially downloading large amount of data which would be thrown away in favour of metadata.

    ## Example Usage

    The following example retrieves a text object (which must have a `Content-Type`
    value starting with `text/`) and uses it as the `user_data` for an EC2 instance:

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    bootstrap_script = aws.s3.get_object(bucket="ourcorp-deploy-config",
        key="ec2-bootstrap-script.sh")
    example = aws.ec2.Instance("example",
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        ami="ami-2757f631",
        user_data=bootstrap_script.body)
    ```
    <!--End PulumiCodeChooser -->

    The following, more-complex example retrieves only the metadata for a zip
    file stored in S3, which is then used to pass the most recent `version_id`
    to AWS Lambda for use as a function implementation. More information about
    Lambda functions is available in the documentation for
    `lambda.Function`.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    lambda_ = aws.s3.get_object(bucket="ourcorp-lambda-functions",
        key="hello-world.zip")
    test_lambda = aws.lambda_.Function("test_lambda",
        s3_bucket=lambda_.bucket,
        s3_key=lambda_.key,
        s3_object_version=lambda_.version_id,
        name="lambda_function_name",
        role=iam_for_lambda["arn"],
        handler="exports.test")
    ```
    <!--End PulumiCodeChooser -->


    :param str bucket: Name of the bucket to read the object from. Alternatively, an [S3 access point](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-access-points.html) ARN can be specified
    :param str checksum_mode: To retrieve the object's checksum, this argument must be `ENABLED`. If you enable `checksum_mode` and the object is encrypted with KMS, you must have permission to use the `kms:Decrypt` action. Valid values: `ENABLED`
    :param str key: Full path to the object inside the bucket
    :param Mapping[str, str] tags: Map of tags assigned to the object.
    :param str version_id: Specific version ID of the object returned (defaults to latest version)
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    __args__['checksumMode'] = checksum_mode
    __args__['key'] = key
    __args__['range'] = range
    __args__['tags'] = tags
    __args__['versionId'] = version_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:s3/getObject:getObject', __args__, opts=opts, typ=GetObjectResult).value

    return AwaitableGetObjectResult(
        arn=pulumi.get(__ret__, 'arn'),
        body=pulumi.get(__ret__, 'body'),
        bucket=pulumi.get(__ret__, 'bucket'),
        bucket_key_enabled=pulumi.get(__ret__, 'bucket_key_enabled'),
        cache_control=pulumi.get(__ret__, 'cache_control'),
        checksum_crc32=pulumi.get(__ret__, 'checksum_crc32'),
        checksum_crc32c=pulumi.get(__ret__, 'checksum_crc32c'),
        checksum_mode=pulumi.get(__ret__, 'checksum_mode'),
        checksum_sha1=pulumi.get(__ret__, 'checksum_sha1'),
        checksum_sha256=pulumi.get(__ret__, 'checksum_sha256'),
        content_disposition=pulumi.get(__ret__, 'content_disposition'),
        content_encoding=pulumi.get(__ret__, 'content_encoding'),
        content_language=pulumi.get(__ret__, 'content_language'),
        content_length=pulumi.get(__ret__, 'content_length'),
        content_type=pulumi.get(__ret__, 'content_type'),
        etag=pulumi.get(__ret__, 'etag'),
        expiration=pulumi.get(__ret__, 'expiration'),
        expires=pulumi.get(__ret__, 'expires'),
        id=pulumi.get(__ret__, 'id'),
        key=pulumi.get(__ret__, 'key'),
        last_modified=pulumi.get(__ret__, 'last_modified'),
        metadata=pulumi.get(__ret__, 'metadata'),
        object_lock_legal_hold_status=pulumi.get(__ret__, 'object_lock_legal_hold_status'),
        object_lock_mode=pulumi.get(__ret__, 'object_lock_mode'),
        object_lock_retain_until_date=pulumi.get(__ret__, 'object_lock_retain_until_date'),
        range=pulumi.get(__ret__, 'range'),
        server_side_encryption=pulumi.get(__ret__, 'server_side_encryption'),
        sse_kms_key_id=pulumi.get(__ret__, 'sse_kms_key_id'),
        storage_class=pulumi.get(__ret__, 'storage_class'),
        tags=pulumi.get(__ret__, 'tags'),
        version_id=pulumi.get(__ret__, 'version_id'),
        website_redirect_location=pulumi.get(__ret__, 'website_redirect_location'))


@_utilities.lift_output_func(get_object)
def get_object_output(bucket: Optional[pulumi.Input[str]] = None,
                      checksum_mode: Optional[pulumi.Input[Optional[str]]] = None,
                      key: Optional[pulumi.Input[str]] = None,
                      range: Optional[pulumi.Input[Optional[str]]] = None,
                      tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                      version_id: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetObjectResult]:
    """
    The S3 object data source allows access to the metadata and
    _optionally_ (see below) content of an object stored inside S3 bucket.

    > **Note:** The content of an object (`body` field) is available only for objects which have a human-readable `Content-Type` (`text/*` and `application/json`). This is to prevent printing unsafe characters and potentially downloading large amount of data which would be thrown away in favour of metadata.

    ## Example Usage

    The following example retrieves a text object (which must have a `Content-Type`
    value starting with `text/`) and uses it as the `user_data` for an EC2 instance:

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    bootstrap_script = aws.s3.get_object(bucket="ourcorp-deploy-config",
        key="ec2-bootstrap-script.sh")
    example = aws.ec2.Instance("example",
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        ami="ami-2757f631",
        user_data=bootstrap_script.body)
    ```
    <!--End PulumiCodeChooser -->

    The following, more-complex example retrieves only the metadata for a zip
    file stored in S3, which is then used to pass the most recent `version_id`
    to AWS Lambda for use as a function implementation. More information about
    Lambda functions is available in the documentation for
    `lambda.Function`.

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_aws as aws

    lambda_ = aws.s3.get_object(bucket="ourcorp-lambda-functions",
        key="hello-world.zip")
    test_lambda = aws.lambda_.Function("test_lambda",
        s3_bucket=lambda_.bucket,
        s3_key=lambda_.key,
        s3_object_version=lambda_.version_id,
        name="lambda_function_name",
        role=iam_for_lambda["arn"],
        handler="exports.test")
    ```
    <!--End PulumiCodeChooser -->


    :param str bucket: Name of the bucket to read the object from. Alternatively, an [S3 access point](https://docs.aws.amazon.com/AmazonS3/latest/dev/using-access-points.html) ARN can be specified
    :param str checksum_mode: To retrieve the object's checksum, this argument must be `ENABLED`. If you enable `checksum_mode` and the object is encrypted with KMS, you must have permission to use the `kms:Decrypt` action. Valid values: `ENABLED`
    :param str key: Full path to the object inside the bucket
    :param Mapping[str, str] tags: Map of tags assigned to the object.
    :param str version_id: Specific version ID of the object returned (defaults to latest version)
    """
    ...
