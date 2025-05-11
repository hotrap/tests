#!/usr/bin/env python3
import sys
if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' data-dir mean-step')
    exit()
data_dir = sys.argv[1]
mean_step = int(sys.argv[2])

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
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH) * 0.33, cm_to_inch(5)))

progress = pd.read_table(data_dir + '/progress', sep='\s+')
info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))
progress = progress[(progress['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (progress['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]

time = (progress['Timestamp(ns)'] - info['run-start-timestamp(ns)']).values / 1e9
time = time[:-1]
progress = progress['operations-executed']
ops = progress[1:len(progress)].values - progress[:len(progress) - 1].values

def mean_every_n(a, n):
    split = len(a) - len(a) % n
    res = a[0:split].reshape(-1, n).mean(axis=1)
    if split != len(a):
        res = np.append(res, a[split:].mean())
    return res

time = mean_every_n(time, mean_step)
ops = mean_every_n(ops, mean_step)

ax = plt.gca()
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 4))
ax.yaxis.set_major_formatter(formatter)
ax.yaxis.get_offset_text().set_fontsize(8)
plt.plot(time, ops, linewidth=0.5)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax.set_ylim(bottom=0)
plt.xlabel('Time (Seconds)', fontsize=8)
plt.ylabel('Operation per second', fontsize=8)
plt.tight_layout()

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
    os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/ops.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
