import asyncio
import math
from collections.abc import AsyncGenerator, Coroutine
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import botocore.exceptions
from google.api_core.exceptions import (
    NotFound,
)
from latch_o11y.o11y import trace_function_with_span
from opentelemetry.trace import Span, get_tracer
from types_aiobotocore_s3.type_defs import (
    CompletedPartTypeDef,
)

from .aws.aws import max_presigned_url_age
from .aws.client_pool import s3_pool
from .gcp.client_pool import gcp_pool

tracer = get_tracer(__name__)

MP_THRESHOLD = 25000000
MP_CHUNK_SIZE = 25000000


class EmptyMountResponseError(Exception):
    pass


@dataclass
class BlobMeta:
    bucket: str
    key: str
    content_type: Any
    size: int
    version: Any
    update_time: datetime | None


class S3MountClient:
    @staticmethod
    @trace_function_with_span(tracer)
    async def head(s: Span, bucket_name: str, key: str) -> BlobMeta:
        s.set_attributes({"bucket_name": bucket_name, "key": key})
        blob = None
        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            try:
                obj = await s3.head_object(Bucket=bucket_name, Key=key)
                if key.endswith("/"):
                    obj["ContentType"] = "dir"
                    obj["ContentLength"] = 0
            except botocore.exceptions.ClientError as e:
                s.record_exception(e)
                res = e.response
                if res.get("Error", {}).get("Code") != "404":
                    raise e

                try:
                    res = await s3.list_objects_v2(
                        Bucket=bucket_name,
                        Prefix=key,
                        MaxKeys=1,
                    )
                    if "Contents" in res:
                        key = key.rstrip("/") + "/"
                        obj = {
                            "ContentType": "dir",
                            "ContentLength": 0,
                            "LastModified": None,
                            "VersionId": None,
                        }
                    else:
                        raise EmptyMountResponseError()
                except botocore.exceptions.ClientError as e:
                    s.record_exception(e)
                    raise EmptyMountResponseError from e

            blob = BlobMeta(
                bucket=bucket_name,
                key=key,
                content_type=obj["ContentType"],
                size=obj["ContentLength"],
                version=obj.get("VersionId"),
                update_time=obj.get("LastModified"),
            )
        return blob

    @staticmethod
    @trace_function_with_span(tracer)
    async def get_blob_bytes(
        s: Span,
        bucket_name: str,
        key: str,
        start: int | None = None,
        end: int | None = None,
    ) -> bytes:
        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            meta = await S3MountClient.head(bucket_name=bucket_name, key=key)

            start = start if start is not None else 0
            end = end if end is not None else meta.size - 1

            response = await s3.get_object(
                Bucket=bucket_name,
                Key=key,
                Range=f"bytes={start}-{end}",
            )

            return await response["Body"].read()

    @staticmethod
    @trace_function_with_span(tracer)
    async def list_keys(
        s: Span,
        bucket_name: str,
        prefix: str | None = None,
        delimiter: str = "/",
        page_size: int = 100,
    ) -> AsyncGenerator[list[str], Any]:
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "prefix": str(prefix),
                "delimeter": delimiter,
                "page_size": page_size,
            }
        )

        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            paginator = s3.get_paginator("list_objects_v2")

            params = {
                "Bucket": bucket_name,
                "Delimiter": delimiter,
            }
            if prefix is not None:
                params["Prefix"] = prefix

            data: list[str] = []
            async for page in paginator.paginate(**params):
                for x in [y["Key"] for y in page.get("Contents", [])] + [
                    y["Prefix"] for y in page.get("CommonPrefixes", [])
                ]:
                    if prefix is None or x.rstrip("/") != prefix.rstrip("/"):
                        data.append(x)

                    if len(data) > page_size:
                        yield data
                        data = []

            yield data

    @staticmethod
    @trace_function_with_span(tracer)
    async def put_blob(
        s: Span,
        bucket_name: str,
        key: str,
        body: bytes = b"",
        content_type: str = "text/plain",
        acl: str = "bucket-owner-full-control",
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "key": key,
                "body": body,
                "content_type": str(content_type),
            }
        )

        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            res = await s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=body,
                ContentType=content_type,
                ACL=acl,
            )

            return BlobMeta(
                bucket=bucket_name,
                key=key,
                content_type=content_type,
                size=len(body),
                version=res["VersionId"],
                update_time=datetime.now(),
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def copy_blob(
        s: Span,
        src_key: str,
        src_bucket: str,
        dest_key: str,
        dest_bucket: str,
    ):
        s.set_attributes(
            {
                "src_key": src_key,
                "src_bucket": src_bucket,
                "dest_key": dest_key,
                "dest_bucket": dest_bucket,
            }
        )

        blob = await S3MountClient.head(src_bucket, src_key)
        if blob is None:
            return
        async with s3_pool.s3_client_for_bucket(dest_bucket) as s3:
            await s3.copy_object(
                CopySource={
                    "Bucket": src_bucket,
                    "Key": src_key,
                },
                Bucket=dest_bucket,
                Key=dest_key,
                ContentType=blob.content_type,
                ACL="bucket-owner-full-control",
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_copy_blob(
        s: Span,
        src_key: str,
        src_bucket: str,
        dest_key: str,
        dest_bucket: str,
    ):
        s.set_attributes(
            {
                "src_key": src_key,
                "src_bucket": src_bucket,
                "dest_key": dest_key,
                "dest_bucket": dest_bucket,
            }
        )

        blob = await S3MountClient.head(src_bucket, src_key)
        if blob is None:
            raise EmptyMountResponseError()

        async with s3_pool.s3_client_for_bucket(dest_bucket) as s3:
            upload_id = await S3MountClient.multipart_initiate_upload(
                dest_bucket,
                dest_key,
                blob.content_type,
                "bucket-owner-full-control",
            )

            parts = math.ceil(blob.size / MP_CHUNK_SIZE)
            s.set_attribute("copy.nrof_parts", parts)

            async def run_upload_chunk(
                byte_range: str, index: int
            ) -> CompletedPartTypeDef:
                res = await s3.upload_part_copy(
                    CopySource={
                        "Bucket": src_bucket,
                        "Key": src_key,
                    },
                    Bucket=dest_bucket,
                    Key=dest_key,
                    PartNumber=index + 1,
                    UploadId=upload_id,
                    CopySourceRange=byte_range,
                )
                if "CopyPartResult" not in res or "ETag" not in res["CopyPartResult"]:
                    raise ValueError("Etag not in response")

                return {
                    "ETag": res["CopyPartResult"]["ETag"],
                    "PartNumber": index + 1,
                }

            upload_chunk_requests: list[Coroutine[Any, Any, CompletedPartTypeDef]] = []

            upload_chunk_responses: list[CompletedPartTypeDef] = []
            for i in range(parts):
                byte_start = i * MP_CHUNK_SIZE
                byte_end = (i + 1) * MP_CHUNK_SIZE - 1
                byte_end = min(byte_end, blob.size - 1)
                byte_range = f"bytes={byte_start}-{byte_end}"

                upload_chunk_requests.append(run_upload_chunk(byte_range, i))

                if len(upload_chunk_requests) >= 50:
                    upload_chunk_responses.extend(
                        await asyncio.gather(*upload_chunk_requests)
                    )
                    upload_chunk_requests = []

            upload_chunk_responses.extend(await asyncio.gather(*upload_chunk_requests))

            await S3MountClient.multipart_complete_upload(
                dest_bucket, dest_key, upload_id, upload_chunk_responses
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def delete_blob(
        s: Span,
        bucket_name: str,
        key: str,
    ):
        s.set_attributes({"bucket_name": bucket_name, "key": key})
        try:
            async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
                await s3.delete_object(
                    Bucket=bucket_name,
                    Key=key,
                )
        except botocore.exceptions.ClientError as e:
            res = e.response
            if res.get("Error", {}).get("Code") != "404":
                raise e

            return

    @staticmethod
    @trace_function_with_span(tracer)
    async def generate_presigned_url(
        s: Span,
        bucket_name: str,
        key: str | None,
        content_disposition: str | None = None,
        content_type: str | None = None,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "key": str(key),
                "content_disposition": str(content_disposition),
                "content_type": str(content_type),
            }
        )

        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            return s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": key,
                    # todo(maximsmol): add extra validation
                    # "ExpectedBucketOwner": "",
                    # "IfMatch": "",
                    # "VersionId": ""
                }
                | (
                    {"ResponseContentDisposition": content_disposition}
                    if content_disposition is not None
                    else {}
                )
                | (
                    {"ResponseContentType": content_type}
                    if content_type is not None
                    else {}
                ),
                ExpiresIn=max_presigned_url_age,
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_initiate_upload(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        content_type: str,
        acl: str = "bucket-owner-full-control",
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "content_type": content_type,
                "acl": acl,
            }
        )
        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            multipart_res = await s3.create_multipart_upload(
                Bucket=bucket_name,
                Key=bucket_key,
                ACL=acl,
                ContentType=content_type,
                # todo(maximsmol): add extra validation
                # "ExpectedBucketOwner": "",
            )
            return multipart_res["UploadId"]

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_upload_part(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        part_number: int,
        data: bytes,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "part_number": part_number,
            }
        )

        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            ret = await s3.upload_part(
                Bucket=bucket_name,
                Key=bucket_key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=data,
            )
            return ret["ETag"]

    @staticmethod
    @trace_function_with_span(tracer)
    async def generate_presigned_part_upload_url(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        part_number: int,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "part_number": part_number,
            }
        )

        async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
            return await s3.generate_presigned_url(
                "upload_part",
                Params={
                    "Bucket": bucket_name,
                    "Key": bucket_key,
                    "UploadId": upload_id,
                    "PartNumber": part_number,
                    # todo(maximsmol): add extra validation
                    # "ExpectedBucketOwner": "",
                },
                ExpiresIn=max_presigned_url_age,
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_complete_upload(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        parts: list[CompletedPartTypeDef],
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "upload_id": upload_id,
            }
        )

        try:
            async with s3_pool.s3_client_for_bucket(bucket_name) as s3:
                res = await s3.complete_multipart_upload(
                    Bucket=bucket_name,
                    Key=bucket_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                    # todo(maximsmol): add extra validation
                    # "ExpectedBucketOwner": "",
                )

                return res["VersionId"]
        except botocore.exceptions.ClientError as e:
            err_res = e.response
            if "Error" not in err_res:
                raise e

            if "Code" not in err_res["Error"]:
                raise e

            if err_res["Error"]["Code"] != "EntityTooSmall":
                raise e

            raise ValueError("Upload size is less than minimum allowed") from e


class GCPMountClient:
    @staticmethod
    @trace_function_with_span(tracer)
    async def head(s: Span, bucket_name: str, key: str) -> BlobMeta:
        s.set_attributes({"bucket_name": bucket_name, "key": key})
        async with gcp_pool.gcp_client() as gcp:
            client = gcp.storage_client()
            blob = await client.get_blob_meta(bucket_name, key)

            if blob is None:
                raise EmptyMountResponseError()

            blob = BlobMeta(
                bucket=bucket_name,
                key=key,
                content_type=blob.content_type,
                size=blob.size,
                version=blob.generation,
                update_time=blob.update_time,
            )

            return blob

    @staticmethod
    @trace_function_with_span(tracer)
    async def get_blob_bytes(
        s: Span,
        bucket_name: str,
        key: str,
        start: int | None = None,
        end: int | None = None,
    ) -> bytes:
        s.set_attributes({"bucket_name": bucket_name, "key": key})
        async with gcp_pool.gcp_client() as gcp:
            client = gcp.storage_client()

            try:
                return await client.get_blob_bytes(
                    bucket_name, key, start=start, end=end
                )
            except NotFound as e:
                raise EmptyMountResponseError() from e

    @staticmethod
    @trace_function_with_span(tracer)
    async def list_keys(
        s: Span,
        bucket_name: str,
        prefix: str | None = None,
        delimiter: str = "/",
        page_size: int = 100,
    ) -> AsyncGenerator[list[str], Any]:
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "prefix": str(prefix),
                "delimeter": delimiter,
                "page_size": page_size,
            }
        )
        async with gcp_pool.gcp_client() as gcp:
            client = gcp.storage_client()

            iterator = client.list_blobs(
                bucket_name,
                prefix=prefix,
                delimiter=delimiter,
            )

            data = []
            async for obj in iterator:
                # don't add the prefix itself to the list
                if prefix is None or obj.name.rstrip("/") != prefix.rstrip("/"):
                    data.append(obj.name)

                if len(data) >= page_size:
                    yield data
                    data = []

            # all the prefixes are present after executing iterator above
            blob_prefixes = set(iterator.prefixes)

            for p in blob_prefixes:
                if prefix is None or p.rstrip("/") != prefix.rstrip("/"):
                    data.append(obj)
                if len(data) >= page_size:
                    yield data
                    data = []

            if len(data) > 0:
                yield data

    @staticmethod
    @trace_function_with_span(tracer)
    async def put_blob(
        s: Span,
        bucket_name: str,
        key: str,
        body: bytes = b"",
        content_type: str | None = None,
        acl: str = "bucket-owner-full-control",
    ):
        s.set_attributes({"bucket_name": bucket_name, "key": key})

        async with gcp_pool.gcp_client() as gcp:
            client = gcp.storage_client()

            content_type = content_type if content_type else "text/plain"

            obj = await client.put_blob(
                bucket_name, key, body, content_type=content_type
            )

            return BlobMeta(
                bucket=bucket_name,
                key=key,
                content_type=content_type,
                size=len(body),
                version=obj.generation,
                update_time=obj.update_time,
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def copy_blob(
        s: Span,
        src_key: str,
        src_bucket_name: str,
        dest_key: str,
        dest_bucket_name: str,
    ):
        s.set_attributes(
            {
                "src_key": src_key,
                "src_bucket_name": src_bucket_name,
                "dest_key": dest_key,
                "dest_bucket_name": dest_bucket_name,
            }
        )

        async with gcp_pool.gcp_client() as gcp:
            client = gcp.storage_client()

            try:
                await client.copy_blob(
                    src_bucket_name=src_bucket_name,
                    src_bucket_key=src_key,
                    dest_bucket_name=dest_bucket_name,
                    dest_bucket_key=dest_key,
                )
            except NotFound as e:
                s.record_exception(e)
                raise EmptyMountResponseError from e

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_copy_blob(
        s: Span,
        src_key: str,
        src_bucket: str,
        dest_key: str,
        dest_bucket: str,
    ):
        s.set_attributes(
            {
                "src_key": src_key,
                "src_bucket": src_bucket,
                "dest_key": dest_key,
                "dest_bucket": dest_bucket,
            }
        )
        await GCPMountClient.copy_blob(src_key, src_bucket, dest_key, dest_bucket)

    @staticmethod
    @trace_function_with_span(tracer)
    async def delete_blob(
        s: Span,
        bucket_name: str,
        key: str,
    ):
        s.set_attributes({"bucket_name": bucket_name, "key": key})
        async with gcp_pool.gcp_client() as gcp:
            await gcp.storage_client().delete_blob(bucket_name, key)

    @staticmethod
    @trace_function_with_span(tracer)
    async def generate_presigned_url(
        s: Span,
        bucket_name: str,
        key: str | None,
        content_disposition: str | None = None,
        content_type: str | None = None,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "key": str(key),
                "content_disposition": str(content_disposition),
                "content_type": str(content_type),
            }
        )
        async with gcp_pool.gcp_client() as gcp:
            url = gcp.storage_client().get_signed_url(
                bucket_name=bucket_name,
                key=key,
                content_disposition=content_disposition,
                content_type=content_type,
            )

            async def generate_signed_url():
                return url

            return generate_signed_url()

    @staticmethod
    @trace_function_with_span(tracer)
    async def generate_presigned_part_upload_url(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        part_number: int,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "idx": part_number,
            }
        )

        async with gcp_pool.gcp_client() as gcp:
            return await gcp.storage_client().get_signed_upload_url(
                bucket_name=bucket_name,
                key=bucket_key,
                upload_id=upload_id,
                part_number=part_number,
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_initiate_upload(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        content_type: str,
        acl: str = "storageAdmin",
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "key": bucket_key,
                "content_type": content_type,
                "acl": acl,
            }
        )
        async with gcp_pool.gcp_client() as gcp:
            return await gcp.storage_client().multipart_initiate_upload(
                bucket_name, bucket_key, content_type
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_upload_part(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        part_number: int,
        data: bytes,
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
                "part_number": part_number,
            }
        )

        async with gcp_pool.gcp_client() as gcp:
            return await gcp.storage_client().multipart_upload_part(
                bucket_name, bucket_key, upload_id, part_number, data
            )

    @staticmethod
    @trace_function_with_span(tracer)
    async def multipart_complete_upload(
        s: Span,
        bucket_name: str,
        bucket_key: str,
        upload_id: str,
        parts: list[CompletedPartTypeDef],
    ):
        s.set_attributes(
            {
                "bucket_name": bucket_name,
                "bucket_key": bucket_key,
            }
        )
        async with gcp_pool.gcp_client() as gcp:
            return await gcp.storage_client().multipart_complete_upload(
                bucket_name, bucket_key, upload_id, parts
            )
