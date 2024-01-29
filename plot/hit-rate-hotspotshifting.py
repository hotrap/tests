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

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))

hit_rates = common.read_hit_rates(data_dir)
time = (hit_rates['Timestamp(ns)'] - info['run-start-timestamp(ns)']) / 1e9
hit_rates = hit_rates['hit-rate'].values

ax = plt.gca()
plt.plot(time, hit_rates)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Hit rate', fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(np.linspace(0, 1, 6), fontsize=8)

interval = int(len(hit_rates) / 100)
def annotate(i, text_x):
    x = time[i - 1]
    y = hit_rates[i - 1]
    hit_rate = hit_rates[i - interval:i].mean()
    ax.annotate('Final: {:.2f}%'.format(hit_rate * 100), xy=(x, y), xytext=(text_x, 0.6), textcoords='axes fraction', arrowprops=dict(arrowstyle="->"), fontsize=8)
annotate((hit_rates[1:] - hit_rates[:-1]).argmin(), 0.1)
annotate(len(hit_rates), 0.6)
plt.tight_layout()

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/hit-rate-hotspotshifting.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
