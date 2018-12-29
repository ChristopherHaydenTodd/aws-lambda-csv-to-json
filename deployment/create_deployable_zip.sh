#!/usr/bin/env bash
#
# Create Lambda Function Zip for Deploying Function
#

echo "$(date +%c): Moving to Base Directory Previous Build"
cd ../

echo "$(date +%c): Removing Previous Build"
rm -rf deployment/s3_convert_csv_json.zip

echo "$(date +%c): Creating Zip and Adding Files"
zip -r deployment/s3_convert_csv_json.zip lambda_entrypoint.py utils/*.py
