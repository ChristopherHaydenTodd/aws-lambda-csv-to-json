#!/usr/bin/env python3
"""
    Purpose:
        Helper Library for AWS S3 Service. Will provide a
        functions for interacting with the Resource and Client
        APIs through Boto3
"""

# Python Library Imports
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

###
# Manage S3 Resource Functions
###

def create_s3_resource(region_name=None, access_key=None, secret_key=None):
    """
    Purpose:
        Return a S3 resource object.
    Args:
        region_name (String): Name of region to connect to
        access_key (String): access key to use to connect to S3 Resource
        secret_key (String): secret key to use to connect to S3 Resource
    Return:
        s3 (S3 Resource Object): S3 Resource Object
    """

    s3 = None
    try:
        if region_name:
            if access_key and secret_key:
                session = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                )
                s3 = session.resource("s3", region_name)
            else:
                s3 = boto3.resource("s3", region_name)
        else:
            if access_key and secret_key:
                session = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                )
                s3 = session.resource("s3")
            else:
                s3 = boto3.resource("s3")
    except NoCredentialsError as err:
        logging.exception("No Credentials Found for AWS")
        raise

    return s3

###
# Bucket Management Function
###

def get_bucket(s3, bucket_name):
    """
    Purpose:
        Return an S3 Bucket by name
    Args:
        s3 (S3 Resource Object): S3 Object owning the Bucket
        bucket_name (String): Name of bucket to return
    Return:
        bucket (S3 Bucket Object): Bucket object for the bucket in
            S3
    """

    try:
        return s3.Bucket(bucket_name)
    except Exception as err:
        logging.exception(f"Exception Getting Bucket: {err}")
        raise


def get_bucket_names(s3):
    """
    Purpose:
        Return an Bucket Names in S3
    Args:
        s3 (S3 Resource Object): S3 Object owning the Bucket
    Return:
        bucket_names (List of Strings): Name of buckets in S3
    """

    return [bucket.name for bucket in s3.buckets.all()]


def create_bucket(s3, bucket_name, region_name=None):
    """
    Purpose:
        Create an S3 Bucket by name
    Args:
        s3 (S3 Resource Object): S3 Object owning the Bucket
        bucket_name (String): Name of bucket to return
        region_name (String): Region to create bucket in
    Return:
        N/A
    """

    try:
        if region_name:
            # Need to Fix
            # s3.create_bucket(
            #     Bucket=bucket_name,
            #     CreateBucketConfiguration={
            #         "LocationConstraint": region_name,
            #     }
            # )
            response = s3.create_bucket(Bucket=bucket_name)
        else:
            response = s3.create_bucket(Bucket=bucket_name)
    except Exception as err:
        logging.exception(f"Exception Creating Bucket: {err}")
        raise


def delete_bucket(bucket, force=True):
    """
    Purpose:
        Delete an S3 Bucket
    Args:
        bucket (S3 Bucket Object): Bucket to upload file to
        force (Boolean): Whether or not to delete all objects in
            the bucket to force the delete. If false, will try to
            delete and fail if there are objects in the bucket
    Return:
        N/A
    """

    try:
        if force:
            response = bucket.delete_objects()
        response = bucket.delete()
    except Exception as err:
        logging.exception(f"Exception Deleting Bucket: {err}")
        raise

###
# Object Management Functions
###

def download_file(bucket, key, filename=None):
    """
    Purpose:
        Download a File to an S3 bucket
    Args:
        bucket (S3 Bucket Object): Bucket to download file from
        key (String): Name of the object in S3
        filename (String): Path to the file on the local host
    Return:
        N/A
    """
    if not filename:
        filename = f"./{key}"
    logging.info(f"Downloading File {key} to {filename}")

    try:
        bucket.download_file(key, filename)
    except ClientError as client_err:
        error_code = client_err.response.get("Error", {}).get("Code", None)
        if not error_code:
            logging.exception(f"ClientError with no code found: {client_err}")
            raise client_err
        elif int(error_code) == 404:
            error_msg = f"{key} Does Not Exist in Bucket {bucket.name}"
            logging.exception(error_msg)
            raise Exception(error_msg) from client_err
        else:
            logging.exception(
                f"ClientError with code ({error_code}) found: {client_err}"
            )
            raise client_err
    except Exception as err:
        logging.exception(f"General Exception downloading file: {err}")
        raise


def upload_file(bucket, key, filename, encryption=None):
    """
    Purpose:
        Upload a File to an S3 bucket
    Args:
        bucket (S3 Bucket Object): Bucket to upload file to
        key (String): Desired name of the object in S3
        filename (String): Path to the file on the local host
        encryption (String): Server Side Encryption Method
    Return:
        N/A
    """
    logging.info(f"Uploading File {filename} to {key}")

    try:
        if encryption:
            bucket.upload_file(
                filename,
                key,
                ExtraArgs={"ServerSideEncryption": encryption},
            )
        else:
            bucket.upload_file(filename, key)
    except Exception as err:
        logging.exception(f"Exception uploading file: {err}")
        raise


def delete_all_files_in_bucket(bucket):
    """
    Purpose:
        Delete all files in a Bucket
    Args:
        bucket (S3 Bucket Object): Bucket to delete files from
    Return:
        N/A
    """

    logging.info("Not Yet Implemented")

    pass

###
# URL Share Functions
###

def generate_presigned_url(s3, bucket_name, key, url_expire=900):
    """
    Purpose:
        Return a presigned URL to a file
    Args:
        s3 (S3 Resource Object): S3 Resource Object
        bucket_name (String): Name of bucket in S3 with Object
        key (String): Name of the object in S3
        url_expire (int): Number of seconds for the URL to live
    Returns:
        presigned_url (String): Presigned URL
    """
    logging.info(f"Generating Presigned URL For {bucket_name} - {key}")

    try:
        return s3.meta.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": key
            },
            ExpiresIn=url_expire
        )
    except Exception as err:
        logging.exception(f"Exception generating Presigned URL: {err}")
        raise


