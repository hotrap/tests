#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()

import os
import json5
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(5)))

data_dir = sys.argv[1]
mean_step = 100

def mean_every_n(a, n):
    split = len(a) - len(a) % n
    res = a[0:split].reshape(-1, n).mean(axis=1)
    if split != len(a):
        res = np.append(res, a[split:].mean())
    return res

progress = pd.read_table(data_dir + '/progress', delim_whitespace=True)
info_json = os.path.join(data_dir, 'info.json')
info_json = json5.load(open(info_json))
progress = progress[(progress['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (progress['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]
progress = progress['operations-executed'].values
progress -= progress[0]
ops = progress[1:] - progress[:-1]
progress = progress[:-1]
progress = mean_every_n(progress, mean_step)
ops = mean_every_n(ops, mean_step)

ax = plt.gca()
plt.plot(progress, ops, linewidth=0.5)
plt.axvline(88e7, linewidth=0.5, linestyle='--', color='black')
plt.text(0.46, 1.05, 'Hotspot shifts', transform=ax.transAxes, fontsize=8)

formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax.yaxis.set_major_formatter(formatter)
ax.yaxis.get_offset_text().set_fontsize(8)
ax.set_ylim(bottom=0)
plt.xticks(fontsize=8)
ax.xaxis.get_offset_text().set_fontsize(8)
plt.yticks(fontsize=8)
plt.xlabel('Completed operation count', fontsize=8)
plt.ylabel('Operations per second', fontsize=8)

pdf_path = os.path.join(data_dir, 'plot', 'progress-ops.pdf')
plt.tight_layout()
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
