import json
import logging
import time
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

class Client:
    client
    def __init__(self, access_key_id, access_key_secret, region_id):
        self.client = client.AcsClient(access_key_id, access_key_secret, region_id)
    # send open api request
    def send_request(self, request):
        request.set_accept_format('json')
        try:
            response_str = self.client.do_action(request)
            response_detail = json.loads(response_str)
            return response_detail
        except Exception as e:
            logging.error(e)

class Instance:
    client: Client
    instance_id: str
    def __init__(self, client, instance_id):
        self.client = client
        self.instance_id = instance_id
    def get_detail(self):
        request = DescribeInstancesRequest()
        request.set_InstanceIds(json.dumps([self.instance_id]))
        response = self.client.send_request(request)
        instance_list = response.get('Instances').get('Instance')
        if len(instance_list) != 1:
            assert len(instance_list) == 0
            return None
        return instance_list[0]
    def get_status(self):
        return self.get_detail().get('Status')
    def wait_to_be(self, status):
        while True:
            if self.get_status() == status:
                break
            time.sleep(10)
