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

def calc(data_dir):
    info = json5.load(open(os.path.join(data_dir, 'info.json')))
    num_bytes = pd.read_table(data_dir + '/promoted-or-retained-bytes', sep='\s+')
    num_bytes = num_bytes[(num_bytes['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (num_bytes['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
    assert num_bytes['2sdfront'].max() == 0
    num_bytes = num_bytes.iloc[-1]
    promoted_by_compaction = num_bytes['2fdlast']
    promoted_by_flush = num_bytes['by-flush']

    compaction_bytes = run_phase(info, common.read_compaction_bytes(data_dir))
    compaction_bytes['read'] -= compaction_bytes.iloc[0]['read']
    compaction_bytes['write'] -= compaction_bytes.iloc[0]['write']
    compaction_io = compaction_bytes.iloc[-1]['read'] + compaction_bytes.iloc[-1]['write']

    return (promoted_by_compaction, promoted_by_flush, compaction_io)
(hotrap_promoted_by_compaction, hotrap_promoted_by_flush, hotrap_compaction_io) = calc(os.path.join(dir, 'hotrap'))
(nbc_promoted_by_compaction, nbc_promoted_by_flush, nbc_compaction_io) = calc(os.path.join(dir, 'no-promote-by-compaction'))

tex = io.StringIO()
print('\\begin{tabular}{|c|c|c|c|}\n\t\\hline\n\tVersion & By Compaction & By flush & Compaction \\\\\n\t\hline', file=tex)
print('\tHotRAP & %.1fGB & %.1fGB & %.1fGB \\\\\n\t\\hline' %(hotrap_promoted_by_compaction / 1e9, hotrap_promoted_by_flush / 1e9, hotrap_compaction_io / 1e9), file=tex)
print('\tno-by-compaction & %.1fGB & %.1fGB & %.1fGB \\\\\n\t\hline' %(nbc_promoted_by_compaction / 1e9, nbc_promoted_by_flush / 1e9, nbc_compaction_io / 1e9), file=tex)
print('\\end{tabular}', file=tex)
tex = tex.getvalue()
print(tex)
open('table-no-by-compaction.tex', mode='w').write(tex)

tex = io.StringIO()
print('\defmacro{NoByCompactionCompactionMore}{%.1f\\%%}' %((nbc_compaction_io / hotrap_compaction_io - 1) * 100), file=tex)
tex = tex.getvalue()
print(tex)
open('no-by-compaction.tex', mode='w').write(tex)
