#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' instance-id')
    exit(1)

import boto3
client = boto3.client('ec2')

client.terminate_instances(
    InstanceIds=[
        sys.argv[1],
    ],
)
