#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5

first_level_in_sd = int(open(os.path.join('first-level-in-last-tier')).read())
d = common.VersionData('.')
compaction_bytes = common.read_compaction_bytes_fd_sd('.', first_level_in_sd)
compaction_bytes = compaction_bytes[compaction_bytes['Timestamp(ns)'] > d.ts_run_90p()]
compaction_bytes -= compaction_bytes.iloc[0]
compaction_bytes = compaction_bytes.iloc[-1]
print('FD read: %f GB' %(compaction_bytes['fd-read'] / 1e9))
print('FD write: %f GB' %(compaction_bytes['fd-write'] / 1e9))
print('SD read: %f GB' %(compaction_bytes['sd-read'] / 1e9))
print('SD write: %f GB' %(compaction_bytes['sd-write'] / 1e9))
