#!/usr/bin/env python3
"""
    Purpose:
        Lambda Function for Converting .csv files in
        an S3 Bucket to .json and uploading the results
    Version: 1.0.3
"""

# Python Library Imports
from __future__ import print_function
import logging
import sys
import os
import json

# Local Library Imports
from utils import loggers, csv_helpers, s3_helpers, lambda_helpers

# Configure Logging
loggers.clear_log_handlers()
logging = loggers.get_stdout_logging(
    log_level=logging.INFO,
    log_prefix="[csv_to_json]: ",
)

###
# Main Entrypoint
###

def lambda_handler(event, context):
    """
    Purpose:
        Handler function for a Lambda function. Will take in an
        event object that triggers the function call and the context
        related to the event.
    Args:
        event (Dict): Dict with event details from the triggering event
            for the function.
        context (Dict): Metadata and context for the function call triggering
            the lambda function
    Return:
        N/A
    """
    logging.info("Starting Lambda to convert objects from .csv to .json")

    logging.info("Parsing Event")
    bucket_name = lambda_helpers.get_bucket_name_from_s3_event(event)
    csv_key = lambda_helpers.get_object_key_from_s3_event(event)

    logging.info("Setting CSV Filepath")
    csv_filename = f"/tmp/{csv_key}"

    logging.info("Connecting to S3")
    s3 = s3_helpers.create_s3_resource()
    bucket = s3_helpers.get_bucket(s3, bucket_name)

    logging.info("Downloading the created object")
    s3_helpers.download_file(bucket, csv_key, filename=f"/tmp/{csv_key}")

    logging.info("Converting .csv into .json")
    json_filename = csv_helpers.convert_csv_file_to_json(csv_filename)

    logging.info("Uploading .json to S3")
    json_key = csv_key.replace(".csv", ".json")
    s3_helpers.upload_file(bucket, json_key, json_filename)

    logging.info("Lambda to convert objects from .csv to .json Complete")


if __name__ == "__main__":

    try:
        fake_s3_event = {
            "Records": [
                {
                    "eventVersion": "2.1",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "2018-12-28T22:52:34.176Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "AWS:AIDAI7KJHUJEQJE3CKSN6"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "73.178.28.65"
                    },
                    "responseElements": {
                        "x-amz-request-id": "C70026574ED6EB78",
                        "x-amz-id-2":
                            "TUM5rK3q2pt+2rxdfTa8Ew59PSNZgxynAe8pGBNAmBuwWrIRv8a6SkZ6PqrKmArLEZ7sMLot0lI="
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "0e8e7eb9-174f-474a-8a57-6aa2574ce404",
                        "bucket": {
                            "name": "christopher-todd-s3-bucket-for-lambda",
                            "ownerIdentity": {
                                "principalId": "A3DEY3EPPPVGR"
                            },
                            "arn": "arn:aws:s3:::christopher-todd-s3-bucket-for-lambda"
                        },
                        "object": {
                            "key": "test2.csv",
                            "size": 431,
                            "eTag": "ea0c07778c2beb1ba3192c7203d58418",
                            "sequencer": "005C26A9321D3EAF6D"
                        },
                    }
                }
            ]
        }
        fake_context = []
        lambda_handler(fake_s3_event, fake_context)
    except Exception as err:
        logging.exception(
            '{0} failed due to error: {1}'.format(
                os.path.basename(__file__), err
            )
        )
        raise
