#!/usr/bin/env python3
"""
    Purpose:
        Provide CSV Helper Functions
"""

# Python Library Imports
import logging
import csv
import json


def convert_csv_file_to_json(csv_filename, json_filename=None, seperator=","):
    """
    Purpose:
        Convert .csv File to .json
    Args:
        csv_filename (String): .csv file to convert to .json
        json_filename (String): filename for the resulting .json
        seperator (String): String seperator of fields in the .csv
    Return:
        json_filename (String): filename for the resulting .json
    """

    if not csv_filename.endswith(".csv"):
        error_msg = "File does not look like .csv, not converting"
        logging.error(error_msg)
        raise Exception(error_msg)

    if not json_filename:
        json_filename = csv_filename.replace(".csv", ".json")

    logging.info(f"Converting {csv_filename} to {json_filename}")

    with open(csv_filename, 'r') as filec, open(json_filename, 'w') as filej:
        field_names = filec.readlines(1)[0].split(seperator)
        reader = csv.DictReader(filec, fieldnames=field_names)
        filej.write(
            json.dumps(
                [row for row in reader],
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )
        )

    return json_filename

