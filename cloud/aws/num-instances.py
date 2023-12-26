#!/usr/bin/env python3

import boto3
client = boto3.client('ec2')

response = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'pending',
                'running',
                'shutting-down',
                'stopping',
                'stopped',
            ]
        },
    ],
)
reservations = response['Reservations']
print(len(reservations))
for reservation in reservations:
    assert len(reservation['Instances']) == 1