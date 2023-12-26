#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' instance-id')
    exit(1)

import boto3
ec2 = boto3.resource('ec2')
instance = ec2.Instance(sys.argv[1])
instance.wait_until_exists()