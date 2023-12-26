#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' instance-id')
    exit(1)

import boto3
client = boto3.client('ec2')

response = client.describe_instances(
    InstanceIds=[
        sys.argv[1],
    ],
)
response = response['Reservations']
assert len(response) == 1
response = response[0]
instances = response['Instances']
assert len(instances) == 1
instance = instances[0]
print(instance['PrivateIpAddress'])