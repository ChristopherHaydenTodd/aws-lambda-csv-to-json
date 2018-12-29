#!/usr/bin/env python3
"""
    Purpose:
        Helper Library for AWS Lambda Service. Will provide a
        functions for interacting with the Resource and Client
        APIs through Boto3
"""

# Python Library Imports
import logging


###
# Parse Event
###

def get_bucket_name_from_s3_event(event):
    """
    Purpose:
        Get the S3 Bucket name from an event triggered by the creation
        of an object in S3
    Args:
        event (Dict): Dict with event details from the triggering event
            for the function.
    Return:
        bucket_name (String): Bucket name of the object creation triggering
            the call to the Lambda function
    """

    bucket_name =\
        event.get("Records", {})[0].get("s3", {}).get("bucket", {}).get("name", None)
    if not bucket_name:
        error_msg = "Event did not have a bucket name; cannot process event"
        logging.error(error_msg)
        raise Exception(error_msg)

    return event.get("Records", {})[0].get("s3", {}).get("bucket", {}).get("name", None)


def get_object_key_from_s3_event(event):
    """
    Purpose:
        Get the S3 Bucket name from an event triggered by the creation
        of an object in S3
    Args:
        event (Dict): Dict with event details from the triggering event
            for the function.
    Return:
        bucket_name (String): Bucket name of the object creation triggering
            the call to the Lambda function
    """

    key = event.get("Records", {})[0].get("s3", {}).get("object", {}).get("key", None)
    if not key:
        error_msg = "Event did not have a object key in S3; cannot process event"
        logging.error(error_msg)
        raise Exception(error_msg)

    return key

###
# Test Lambda
###

def test_lamda_function(lambda_handler, test_event={}, test_context=[]):
    """

    """

    try:
        lambda_handler(test_event, test_context)
    except Exception as err:
        logging.exception(f"Lambda failed due to error: {err}")
        raise
