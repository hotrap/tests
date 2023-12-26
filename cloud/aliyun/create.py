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
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.AllocatePublicIpAddressRequest import AllocatePublicIpAddressRequest
# configuration the log output formatter, if you want to save the output to file,
# append ",filename='ecs_invoke.log'" after datefmt.
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

instance_type = 'ecs.i3g.2xlarge'

# create one after pay ecs instance.
def create_after_pay_instance(client, instance_name):
    request = CreateInstanceRequest()
    request.set_InstanceName(instance_name)
    request.set_HostName(instance_name)
    request.set_InternetChargeType('PayByTraffic')
    request.set_InternetMaxBandwidthIn(100)
    request.set_InternetMaxBandwidthOut(100)
    request.set_KeyPairName(config['key_pair_name'])
    request.set_ImageId(config['image_id'])
    request.set_SecurityGroupId(config['security_group_id'])
    request.set_InstanceType(instance_type)
    request.set_IoOptimized('optimized')
    request.set_VSwitchId(config['vswitch_id'])
    request.set_SystemDiskCategory('cloud_essd')
    request.set_SystemDiskPerformanceLevel('PL0')
    request.set_SystemDiskSize(1024)
    response = client.send_request(request)
    instance_id = response.get('InstanceId')
    return instance_id

if __name__ == '__main__':
    client = Client(config['access_key_id'], config['access_key_secret'], config['region_id'])
    instance_id = create_after_pay_instance(client, instance_name)
    instance = Instance(client, instance_id)

    request = AllocatePublicIpAddressRequest()
    request.set_InstanceId(instance_id)
    client.send_request(request)

    print(instance_id)
