#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5

d = common.VersionData('.')
compaction_bytes = common.read_compaction_bytes('.')
compaction_bytes = compaction_bytes[compaction_bytes['Timestamp(ns)'] > d.ts_run_90p()]

compaction_bytes['read'] -= compaction_bytes.iloc[0]['read']
print('read: %f GB' %(compaction_bytes.iloc[-1]['read'] / 1e9))
compaction_bytes['write'] -= compaction_bytes.iloc[0]['write']
print('write: %f GB' %(compaction_bytes.iloc[-1]['write'] / 1e9))
print('total: %f GB' %((compaction_bytes.iloc[-1]['read'] + compaction_bytes.iloc[-1]['write']) / 1e9))
