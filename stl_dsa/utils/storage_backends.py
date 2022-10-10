# FILE: example/utils/storage_backends.py

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# class StaticStorage(S3Boto3Storage):
#     """Used to manage static files for the web server"""

#     location = settings.STATIC_LOCATION
#     default_acl = settings.STATIC_DEFAULT_ACL


class PublicMediaStorage(S3Boto3Storage):
    """Used to store & serve dynamic media files with no access expiration"""

    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = settings.PUBLIC_MEDIA_DEFAULT_ACL
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """
    Used to store & serve dynamic media files using access keys
    and short-lived expirations to ensure more privacy control
    """

    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = settings.PRIVATE_MEDIA_DEFAULT_ACL
    file_overwrite = False
    custom_domain = False


# def select_private_storage():
#     # important
#     private_storage_class = get_storage_class(settings.PRIVATE_FILE_STORAGE)
#     return private_storage_class()  # instantiate the storage
