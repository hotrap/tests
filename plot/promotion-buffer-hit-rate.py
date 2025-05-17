#!/usr/bin/env python3
import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' data-dir mean-step')
    exit()
data_dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import os
import json5
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# Paper specific settings
STANDARD_WIDTH = 17.8
SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
DOUBLE_COL_WIDTH = STANDARD_WIDTH
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(5)), constrained_layout=True)

version_data = common.VersionData(data_dir)
report = pd.read_table(os.path.join(data_dir, 'report.csv'), sep=',')
report = report.groupby(report.index // mean_step).mean()
report['pb-hit-rate'] = report['hotrap.promotion_buffer.get.hit'] / report['num-reads']
time = (report['Timestamp(ns)'] - version_data.info()['run-start-timestamp(ns)']).values / 1e9
plt.plot(time, report['hotrap.promotion_buffer.get.hit'] / report['num-reads'])
plt.ylabel('Hit rate', fontsize=9)
plt.yticks(fontsize=9)

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
    os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/promotion-buffer-hit-rate.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
