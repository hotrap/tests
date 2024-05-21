#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' dir mean-step')
    exit()
dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
import json5
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.gridspec as gridspec

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

fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)))

versions = [
    {
        'name': '(a) HotRAP',
        'path': 'ycsbc_hotspot0.01_110GB/promote-stably-hot',
        'ymax': 4e4,
        'yticks': [0, 1e4, 2e4, 3e4, 4e4],
    },
    {
        'name': '(b) RocksDB-fat',
        'path': 'ycsbc_hotspot0.01_load_110GB_run_1GB/rocksdb-fat',
        'ymax': 400,
        'yticks': [0, 100, 200, 300, 400],
    }
]
gs = gridspec.GridSpec(1, len(versions))

for (version_idx, version) in enumerate(versions):
    subfig = plt.subplot(gs[0, version_idx])
    data_dir = os.path.join(dir, version['path'])

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
    plt.ylim(0, version['ymax'])
    plt.xticks(fontsize=8)
    plt.yticks(version['yticks'], fontsize=8)
    if version_idx == 0:
        plt.ylabel('Operation per second', fontsize=8)
    subfig.text(0.5, -0.4, 'Time (Seconds)', fontsize=6, ha='center', va='center', transform=subfig.transAxes)
    plt.xlabel(version['name'], labelpad=8, fontsize=8)

plt.tight_layout()
pdf_path = dir + '/hdd-ops.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
