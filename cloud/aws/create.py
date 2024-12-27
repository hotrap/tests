#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' config-file')
    exit(1)

import json5
config = json5.load(open(sys.argv[1]))

import boto3
client = boto3.client('ec2')

response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'DeleteOnTermination': True,
                'Iops': 10000,
                'VolumeSize': 2048, # GiBs
                'VolumeType': 'gp3',
                'Throughput': 300, # MiB/s
                'Encrypted': False
            },
        },
    ],
    ImageId=config['ImageId'],
    InstanceType='i4i.2xlarge',
    KeyName=config['KeyName'],
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=[
        config['SecurityGroupId'],
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': config['InstanceName'],
                },
            ],
        },
    ],
    EbsOptimized=True,
)
assert len(response['Instances']) == 1
instance = response['Instances'][0]
print(instance['InstanceId'])
