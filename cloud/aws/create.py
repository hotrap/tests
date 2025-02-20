#!/usr/bin/env python3
import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' aws-config machine-config')
    exit(1)

import json5
aws_config = json5.load(open(sys.argv[1]))
machine_config = json5.load(open(sys.argv[2]))

import boto3
client = boto3.client('ec2')

response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'DeleteOnTermination': True,
                'Iops': 10000,
                'VolumeSize': machine_config['SlowDiskGiB'],
                'VolumeType': 'gp3',
                'Throughput': 300, # MiB/s
                'Encrypted': False
            },
        },
    ],
    ImageId=aws_config['ImageId'],
    InstanceType='i4i.2xlarge',
    KeyName=aws_config['KeyName'],
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=[
        aws_config['SecurityGroupId'],
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': aws_config['InstanceName'],
                },
            ],
        },
    ],
    EbsOptimized=True,
)
assert len(response['Instances']) == 1
instance = response['Instances'][0]
print(instance['InstanceId'])
