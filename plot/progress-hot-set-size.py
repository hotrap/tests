#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' data-dir')
	exit()
data_dir = sys.argv[1]

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5
import numpy as np
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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4.7)))

class Estimater:
    it = None
    x0 = None
    x1 = None
    field: str
    def __init__(self, df, field):
        self.it = df.iterrows()
        self.x0 = next(self.it)[1]
        self.x1 = next(self.it)[1]
        self.field = field
    # Raise StopIteration if none
    def __estimate(self, timestamp):
        return self.x0[self.field] + (self.x1[self.field] - self.x0[self.field]) / (self.x1['Timestamp(ns)'] - self.x0['Timestamp(ns)']) * (timestamp - self.x0['Timestamp(ns)'])
    def estimate(self, timestamp):
        while self.x1['Timestamp(ns)'] <= timestamp:
            self.x0 = self.x1
            self.x1 = next(self.it)[1]
        return self.__estimate(timestamp)

def run_phase(info, data):
    return data[(data['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))

progress = pd.read_table(data_dir + '/progress', sep='\s+')
progress = run_phase(info, progress)
progress['operations-executed'] -= progress.iloc[0]['operations-executed']

viscnts_sizes = pd.read_table(os.path.join(data_dir, 'viscnts-sizes'), sep='\s+')
real_hot_size_est = Estimater(viscnts_sizes, 'real-hot-size')

x = []
real_hot_size = []
for _, row in progress.iterrows():
    timestamp = row['Timestamp(ns)']
    try:
        real_hot_size.append(real_hot_size_est.estimate(timestamp))
    except StopIteration:
        break
    x.append(row['operations-executed'])
assert len(real_hot_size) == len(x)
real_hot_size = np.array(real_hot_size)

hotspot_sizes = np.array([
     [0, 0],
     [22e7, 0],
     [22e7 + 1, 1.1e9],
     [44e7, 1.1e9],
     [44e7 + 1, 3.3e9],
     [66e7, 3.3e9],
     [66e7 + 1, 5.5e9],
     [110e7, 5.5e9],
     [110e7 + 1, 4.4e9],
     [132e7, 4.4e9],
     [132e7 + 1, 2.2e9],
     [154e7, 2.2e9],
])

ax = plt.gca()
plt.plot(hotspot_sizes[:,0], hotspot_sizes[:,1] / 1e9, linewidth=0.5, marker='^', markersize=4)
plt.plot(x, real_hot_size / 1e9, linewidth=0.5, marker='o', markersize=4, markevery=int(len(x) / 5))
plt.axvline(88e7, linewidth=0.5, linestyle='--', color='black')
plt.text(0.46, 1.05, 'Hotspot shifts', transform=ax.transAxes, fontsize=8)

plt.xlabel('Completed operation count', fontsize=8, loc='left')
plt.ylabel('Size (GB)', fontsize=8)
plt.xticks(fontsize=8)
ax.ticklabel_format(useMathText=True)
ax.xaxis.get_offset_text().set_fontsize(8)
plt.yticks(fontsize=8)
ax.yaxis.get_offset_text().set_fontsize(8)
plt.legend(['Hotspot size', 'Hot set size'], frameon=False, fontsize=8, loc='upper left', bbox_to_anchor=(0.05, 0.98))
plt.tight_layout()

pdf_path = os.path.join(data_dir, 'plot', 'progress-hot-set-size.pdf')
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
