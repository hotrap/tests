#!/usr/bin/env python3
import sys
if len(sys.argv) > 2:
    print('Usage: ' + sys.argv[0] + ' [instance-id]')
    exit(1)

import boto3
client = boto3.client('ec2')

import json5

InstanceIds=[]
if len(sys.argv) == 2:
    InstanceIds.append(sys.argv[1])

response = client.describe_instances(InstanceIds=InstanceIds)
print(json5.dumps(
    response,
    indent=4,
    # https://stackoverflow.com/a/36142844/13688160
    default=str
))