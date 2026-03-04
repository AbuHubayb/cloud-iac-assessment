#!/bin/bash

echo "Creating S3 bucket..."
awslocal s3 mb s3://analyzer-reports

echo "Uploading analyzer report..."
awslocal s3 cp /tmp/report.json s3://analyzer-reports/report.json

echo "Initialization complete."