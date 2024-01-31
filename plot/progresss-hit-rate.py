#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir = sys.argv[1]

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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(4.7)))

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

ax = plt.gca()
def draw(version, marker, text_y):
    data_dir = os.path.join(dir, version)
    info = os.path.join(data_dir, 'info.json')
    info = json5.load(open(info))

    progress = pd.read_table(data_dir + '/progress', delim_whitespace=True)
    progress = run_phase(info, progress)
    progress['operations-executed'] -= progress.iloc[0]['operations-executed']

    hit_rates = common.read_hit_rates(data_dir)
    hit_rate = Estimater(hit_rates, 'hit-rate')

    x = []
    y = []
    for _, row in progress.iterrows():
        timestamp = row['Timestamp(ns)']
        try:
            y.append(hit_rate.estimate(timestamp))
        except StopIteration:
            break
        x.append(row['operations-executed'])
    plt.plot(x, y, linewidth=0.5, marker=marker, markersize=4, markevery=int(len(x) / 5))

    # hit_rate = hit_rates['hit-rate'][int(len(hit_rates) * 0.99):].mean()
    # ax.annotate('Final: {:.2f}%'.format(hit_rate * 100), xy=(x[-1], hit_rate), xytext=(0.5, text_y), textcoords='axes fraction', arrowprops=dict(arrowstyle="->"), fontsize=8)
draw('promote-stably-hot', 'o', 0.8)
draw('no-retain', '^', 0.4)
plt.xlabel('Completed operation count', fontsize=8, loc='left')
plt.ylabel('Hit rate', fontsize=8)
plt.xticks(fontsize=8)
ax.ticklabel_format(useMathText=True)
ax.xaxis.get_offset_text().set_fontsize(8)
plt.yticks(np.linspace(0, 1, 6), fontsize=8)
plt.legend(['HotRAP', 'no-retain'], frameon=False, fontsize=8)
plt.tight_layout()

pdf_path = dir + '/progress-hit-rate.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
