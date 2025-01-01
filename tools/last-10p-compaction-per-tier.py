#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5

first_level_in_sd = int(open(os.path.join('first-level-in-last-tier')).read())
d = common.VersionData('.')
compaction_bytes = common.read_compaction_bytes_per_tier('.', first_level_in_sd)
compaction_bytes = compaction_bytes[compaction_bytes['Timestamp(ns)'] > d.ts_run_90p()]
compaction_bytes -= compaction_bytes.iloc[0]
compaction_bytes = compaction_bytes.iloc[-1]
print('0-read: %f GB' %(compaction_bytes['0-read'] / 1e9))
print('0-write: %f GB' %(compaction_bytes['0-write'] / 1e9))
print('1-read: %f GB' %(compaction_bytes['1-read'] / 1e9))
print('1-write: %f GB' %(compaction_bytes['1-write'] / 1e9))
