"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging
import base64
import boto3

from botocore.exceptions import ClientError
from urllib.parse import urlparse
from core.utils.params import get_env
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException


logger = logging.getLogger(__name__)


def get_client_and_resource(
    aws_access_key_id=None,
    aws_secret_access_key=None,
    aws_session_token=None,
    region_name=None,
    s3_endpoint=None
):
    aws_access_key_id = aws_access_key_id or get_env('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = aws_secret_access_key or get_env('AWS_SECRET_ACCESS_KEY')
    aws_session_token = aws_session_token or get_env('AWS_SESSION_TOKEN')
    logger.debug(f'Create boto3 session with '
                 f'access key id={aws_access_key_id}, '
                 f'secret key={aws_secret_access_key[:4] + "..." if aws_secret_access_key else None}, '
                 f'session token={aws_session_token}')
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )
    settings = {
        'region_name': region_name or get_env('S3_region') or 'us-east-1'
    }
    s3_endpoint = s3_endpoint or get_env('S3_ENDPOINT')
    if s3_endpoint:
        settings['endpoint_url'] = s3_endpoint
    client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'), **settings)
    resource = session.resource('s3', config=boto3.session.Config(signature_version='s3v4'), **settings)
    return client, resource


def resolve_s3_url(url, client, presign=True, expires_in=3600):
    r = urlparse(url, allow_fragments=False)
    bucket_name = r.netloc
    key = r.path.lstrip('/')

    # Return blob as base64 encoded string if presigned urls are disabled
    if not presign:
        object = client.get_object(Bucket=bucket_name, Key=key)
        content_type = object['ResponseMetadata']['HTTPHeaders']['content-type']
        object_b64 = "data:" + content_type + ";base64," + base64.b64encode(object['Body'].read()).decode('utf-8')
        return object_b64

    # Otherwise try to generate presigned url
    try:
        presigned_url = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expires_in)
    except ClientError as exc:
        logger.warning(f'Can\'t generate presigned URL. Reason: {exc}')
        return url
    else:
        logger.debug('Presigned URL {presigned_url} generated for {url}'.format(
            presigned_url=presigned_url, url=url))
        return presigned_url


class AWS(object):

    @classmethod
    def get_blob_metadata(cls,
                          url: str,
                          bucket_name: str,
                          client=None,
                          aws_access_key_id=None,
                          aws_secret_access_key=None,
                          aws_session_token=None,
                          region_name=None,
                          s3_endpoint=None
                          ):
        """
        Get blob metadata by url
        :param url: Object key
        :param bucket_name: AWS bucket name
        :param client: AWS client for batch processing
        :param account_key: Azure account key
        :return: Object metadata dict("name": "value")
        """
        if client is None:
            client, _ = get_client_and_resource(aws_access_key_id=aws_access_key_id,
                                                aws_secret_access_key=aws_secret_access_key,
                                                aws_session_token=aws_session_token,
                                                region_name=region_name,
                                                s3_endpoint=s3_endpoint)
        object = client.get_object(Bucket=bucket_name, Key=url)
        metadata = dict(object)
        # remove unused fields
        metadata.pop("Body", None)
        metadata.pop("ResponseMetadata", None)
        return metadata


# def synchronize_s3_import_storage(storage_id):
#     """
#     Synchronize S3 Import Storage by its ID.

#     :param storage_id: ID of the S3ImportStorage to synchronize
#     :return: None or raises an exception if synchronization fails
#     """
#     # Fetch the S3ImportStorage instance
#     storage = get_object_or_404(S3ImportStorageBase, pk=storage_id)

#     # Check if the storage is synchronizable
#     if not hasattr(storage, 'synchronizable') or not storage.synchronizable:
#         raise APIException(f'Storage {storage_id} is not synchronizable')

#     # Validate the connection to the S3 storage
#     try:
#         storage.validate_connection()
#     except Exception as e:
#         raise APIException(f'Validation failed for storage {storage_id}: {e}')

#     # Synchronize the storage
#     try:
#         storage.sync()
#         # Optionally, refresh the instance from the database
#         storage.refresh_from_db()
#         logger.info(f'Successfully synchronized S3 Import Storage with ID {storage_id}')
#     except Exception as e:
#         raise APIException(f'Failed to synchronize storage {storage_id}: {e}')

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException

def synchronize_s3_import_storage(storage_id):
    # Dynamically import the S3ImportStorage model to avoid circular import
    from io_storages.s3.models import S3ImportStorage
    
    storage = get_object_or_404(S3ImportStorage, pk=storage_id)
    
    if not hasattr(storage, 'sync'):
        raise APIException(f'Storage {storage_id} does not support synchronization.')
    
    try:
        storage.sync()
        logger.info(f'Successfully synchronized S3 Import Storage with ID {storage_id}')
    except Exception as e:
        logger.error(f'Failed to synchronize S3 Import Storage with ID {storage_id}: {e}')
        raise APIException(f'Failed to synchronize storage {storage_id}: {e}')
    
    

# def synchronize_s3_export_storage(storage_id):
#     from io_storages.s3.models import S3ExportStorage
#     """
#     Synchronize S3 Export Storage by its ID.

#     :param storage_id: ID of the S3ExportStorage to synchronize
#     :return: None or raises an exception if synchronization fails
#     """
#     # Fetch the S3ExportStorage instance
#     storage = get_object_or_404(S3ExportStorage, pk=storage_id)

#     # Validate the connection to the S3 storage
#     try:
#         storage.validate_connection()
#     except Exception as e:
#         raise APIException(f'Validation failed for storage {storage_id}: {e}')

#     # Synchronize the storage
#     try:
#         # Implement the synchronization logic here
#         # This could involve exporting data to the storage, updating database records, etc.
#         print(f"Synchronization logic for S3 Export Storage {storage_id} goes here.")
#         # Optionally, refresh the instance from the database
#         storage.refresh_from_db()
#         logger.info(f'Successfully synchronized S3 Export Storage with ID {storage_id}')
#     except Exception as e:
#         raise APIException(f'Failed to synchronize storage {storage_id}: {e}')
    
def synchronize_s3_export_storage(storage_id):
    # Dynamically import the S3ExportStorage model to avoid circular import
    from io_storages.s3.models import S3ExportStorage
    
    storage = get_object_or_404(S3ExportStorage, pk=storage_id)
    
    if not hasattr(storage, 'sync'):
        raise APIException(f'Export Storage {storage_id} does not support synchronization.')
    
    try:
        storage.sync()
        logger.info(f'Successfully synchronized S3 Export Storage with ID {storage_id}')
    except Exception as e:
        logger.error(f'Failed to synchronize S3 Export Storage with ID {storage_id}: {e}')
        raise APIException(f'Failed to synchronize export storage {storage_id}: {e}')