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
import pandas as pd

def run_phase(info_json, data):
    return data[(data['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]

def calc(data_dir):
    version_data = common.VersionData(data_dir)

    num_bytes = pd.read_table(data_dir + '/promoted-or-retained-bytes', sep='\s+')
    num_bytes = run_phase(version_data.info(), num_bytes)
    num_bytes = num_bytes.iloc[-1]
    promoted = num_bytes['by-compaction'] + num_bytes['by-flush']

    compaction_bytes = run_phase(version_data.info(), common.read_compaction_bytes(data_dir))
    compaction_bytes['read'] -= compaction_bytes.iloc[0]['read']
    compaction_bytes['write'] -= compaction_bytes.iloc[0]['write']
    compaction_io = compaction_bytes.iloc[-1]['read'] + compaction_bytes.iloc[-1]['write']

    hit_rates = common.read_hit_rates(data_dir)
    final_hit_rate = hit_rates['hit-rate'][int(len(hit_rates) * 0.99):].mean()

    du = pd.read_table(os.path.join(data_dir, 'du.sh.txt'), sep='\s+').iloc[-1]
    disk_usage = du['FD'] + du['SD']

    return (promoted, compaction_io, final_hit_rate, disk_usage)

(hotrap_promoted, hotrap_compaction_io, hotrap_hit_rate, hotrap_disk_usage) = calc(os.path.join(dir, 'hotrap'))
(promoted, compaction_io, hit_rate, disk_usage) = calc(os.path.join(dir, 'no-hotness-aware-compaction'))

tex = io.StringIO()
print('\\begin{tabular}{|@{\hspace{4pt}}c@{\hspace{4pt}}|@{\hspace{4pt}}c@{\hspace{4pt}}|@{\hspace{4pt}}c@{\hspace{4pt}}|@{\hspace{4pt}}c@{\hspace{4pt}}|@{\hspace{4pt}}c@{\hspace{4pt}}|}\n\t\\hline\n\tVersion & Promoted & Compaction & Hit rate & Disk usage \\\\\n\t\hline', file=tex)
print('\t' + common.sysname + ' & %.1fGB & %.1fGB & %.1f\\%% & %.1fGB \\\\\n\t\\hline' %(hotrap_promoted / 1e9, hotrap_compaction_io / 1e9, hotrap_hit_rate * 100, hotrap_disk_usage / 1e9), file=tex)
print('\tno-hot-aware & %.1fGB & %.1fGB & %.1f\\%% & %.1fGB \\\\\n\t\hline' %(promoted / 1e9, compaction_io / 1e9, hit_rate * 100, disk_usage / 1e9), file=tex)
print('\\end{tabular}', file=tex)
tex = tex.getvalue()
print(tex)
open('table-no-hotness-aware-compaction.tex', mode='w').write(tex)
