#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
from common import *

import json5

data_dir = '.'
info_json = os.path.join(data_dir, 'info.json')
info_json = json5.load(open(info_json))

def run_phase(info_json, data):
    return data[(data['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]

compaction_bytes = run_phase(info_json, read_compaction_bytes(os.path.join(data_dir, 'compaction-stats')))
compaction_bytes['read'] -= compaction_bytes.iloc[0]['read']
compaction_bytes['write'] -= compaction_bytes.iloc[0]['write']
print('total: %f GB' %((compaction_bytes.iloc[-1]['read'] + compaction_bytes.iloc[-1]['write']) / 1e9))