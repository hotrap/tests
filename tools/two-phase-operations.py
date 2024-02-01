#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5
import pandas as pd

info = json5.load(open('info.json'))
progress = pd.read_table('progress', delim_whitespace=True)
run_start_progress = common.timestamp_to_progress(progress, info['run-start-timestamp(ns)'])
run_end_progress = common.timestamp_to_progress(progress, info['run-end-timestamp(ns)'])
warmup_progress = common.warmup_finish_progress('.')
print('Warm-up phase: ' + str(warmup_progress - run_start_progress))
print('Stable phase: ' + str(run_end_progress - warmup_progress))
