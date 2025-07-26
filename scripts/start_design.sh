#!/bin/bash
cd ../src/boto3
python ./aws_bedrock_test.py > output.log 2>&1

if [ $? -ne 0 ]; then
    echo "Error: Failed to run the Python script."
    exit 1
fi