#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' instance-id')
    exit(1)

import boto3
ec2 = boto3.resource('ec2')
instance = ec2.Instance(sys.argv[1])
# It has a low probability that ip.py still complains that instance does not exist even after wait_until_exists
#instance.wait_until_exists()
instance.wait_until_running()
