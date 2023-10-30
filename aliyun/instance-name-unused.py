#!/usr/bin/env python3

import sys
if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " config-file instance-name")
    exit(1)

import json
with open(sys.argv[1], "r") as config_file:
    config = json.load(config_file)

instance_name = sys.argv[2]

from common import *

import logging
# configuration the log output formatter, if you want to save the output to file,
# append ",filename='ecs_invoke.log'" after datefmt.
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

if __name__ == '__main__':
    client = Client(config['access_key_id'], config['access_key_secret'], config['region_id'])
    request = DescribeInstancesRequest()
    request.set_InstanceName(instance_name)
    response = client.send_request(request)
    if len(response.get('Instances').get('Instance')) != 0:
        exit(1)
