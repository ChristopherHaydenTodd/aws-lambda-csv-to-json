#!/usr/bin/env bash
#
# Deploy Lambda Function Code
#

echo "$(date +%c): Pushing Zip"
aws lambda update-function-code --function-name=s3-convert-csv-to-json--zip-file=fileb://s3_convert_csv_json.zip
