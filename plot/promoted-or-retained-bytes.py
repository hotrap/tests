#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()
data_dir = sys.argv[1]

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(5)))
num_marks = 5
markersize = 3

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))

num_bytes = pd.read_table(data_dir + '/promoted-or-retained-bytes', delim_whitespace=True)
num_bytes = num_bytes[(num_bytes['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (num_bytes['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
time = (num_bytes['Timestamp(ns)'] - info['run-start-timestamp(ns)']) / 1e9

assert num_bytes['2cdfront'].max() == 0
ax = plt.gca()
markevery = int(len(time) / num_marks)
plt.plot(time, num_bytes['2sdlast'], linewidth=0.5, marker='^', markersize=markersize, markevery=markevery)
plt.plot(time, num_bytes['by-flush'], linewidth=0.5, marker='o', markersize=markersize, markevery=markevery)
plt.plot(time, num_bytes['retained'], linewidth=0.5, marker='s', markersize=markersize, markevery=markevery)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax.ticklabel_format(useMathText=True)
ax.yaxis.get_offset_text().set_fontsize(8)
plt.legend(['By compaction', 'By flush', 'Retained'], frameon=False, fontsize=8, loc=(0, 0.55))
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Promoted/retained bytes', fontsize=8)
plt.tight_layout()

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/promoted-or-retained-bytes.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
