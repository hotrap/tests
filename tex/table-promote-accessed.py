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
    num_bytes = pd.read_table(data_dir + '/promoted-or-retained-bytes', delim_whitespace=True)
    num_bytes = num_bytes[(num_bytes['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (num_bytes['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
    assert num_bytes['2sdfront'].max() == 0
    num_bytes = num_bytes.iloc[-1]
    promoted = num_bytes['2fdlast'] + num_bytes['by-flush']
    retained = num_bytes['retained']

    compaction_bytes = run_phase(info, common.read_compaction_bytes(data_dir))
    compaction_bytes['read'] -= compaction_bytes.iloc[0]['read']
    compaction_bytes['write'] -= compaction_bytes.iloc[0]['write']
    compaction_io = compaction_bytes.iloc[-1]['read'] + compaction_bytes.iloc[-1]['write']
    return (promoted, retained, compaction_io)
(hotrap_promoted, hotrap_retained, hotrap_compaction_io) = calc(os.path.join(dir, 'promote-stably-hot'))
(pa_promoted, pa_retained, pa_compaction_io) = calc(os.path.join(dir, 'promote-accessed'))

tex = io.StringIO()
print('\\begin{tabular}{|c|c|c|c|}\n\t\\hline\n\tVersion & Promoted & Retained & Compaction \\\\\n\t\hline', file=tex)
print('\tHotRAP & %.1fGB & %.1fMB & %.1fGB \\\\\n\t\\hline' %(hotrap_promoted / 1e9, hotrap_retained / 1e6, hotrap_compaction_io / 1e9), file=tex)
print('\tpromote-accessed & %.1fGB & %.1fGB & %.1fGB \\\\\n\t\hline' %(pa_promoted / 1e9, pa_retained / 1e9, pa_compaction_io / 1e9), file=tex)
print('\\end{tabular}', file=tex)
tex = tex.getvalue()
print(tex)
open('table-promote-accessed.tex', mode='w').write(tex)

tex = io.StringIO()
print('\defmacro{PromoteAccessedPromotedMore}{%.1f$\\times$}' %(pa_promoted / hotrap_promoted - 1), file=tex)
print('\defmacro{PromoteAccessedCompactionMore}{%.1f$\\times$}' %(pa_compaction_io / hotrap_compaction_io - 1), file=tex)
tex = tex.getvalue()
print(tex)
open('promote-accessed.tex', mode='w').write(tex)
