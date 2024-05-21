#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import io
import json5
import pandas as pd

def run_phase(info_json, data):
    return data[(data['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]

data_dir = os.path.join(dir, 'ycsbc_hotspot0.01_load_110GB_run_1GB', 'rocksdb-fat')
info = json5.load(open(os.path.join(data_dir, 'info.json')))
progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
progress = run_phase(info, progress)['operations-executed']
run_time = (info['run-end-timestamp(ns)'] - info['run-start-timestamp(ns)']) / 1e9
rocksdb_fat_ops = (progress.iloc[-1] - progress.iloc[0]) / run_time

data_dir = os.path.join(dir, 'ycsbc_hotspot0.01_110GB', 'promote-stably-hot')
info = json5.load(open(os.path.join(data_dir, 'info.json')))
progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
hit_rates = common.read_hit_rates(data_dir)
stable_start_ts = common.warmup_finish_timestamp(hit_rates)
stable_start_progress = common.timestamp_to_progress(progress, stable_start_ts)
stable_time = (info['run-end-timestamp(ns)'] - stable_start_ts) / 1e9
hotrap_ops = (progress.iloc[-1]['operations-executed'] - stable_start_progress) / stable_time

tex = io.StringIO()
print('\defmacro{HDDHotrapDivRocksdbfat}{%.0f}' %(hotrap_ops / rocksdb_fat_ops), file=tex)
tex = tex.getvalue()
print(tex)
open('hdd-test.tex', mode='w').write(tex)
