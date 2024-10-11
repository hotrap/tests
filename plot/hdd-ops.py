#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' dir')
    exit()
dir = sys.argv[1]
mean_step = 10

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import io
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.gridspec as gridspec

# Paper specific settings
SINGLE_COL_WIDTH = 8.5
DOUBLE_COL_WIDTH = 17.8
def cm_to_inch(value):
    return value/2.54

mpl.rcParams.update({
    'hatch.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })
plt.rcParams['axes.unicode_minus'] = False

figure = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(3.5)), constrained_layout=True)

versions = [
    {
        'name': '(a) HotRAP',
        'path': 'ycsbc_hotspot0.01_110GB_220GB/hotrap',
        'ymax': 4e4,
        'yticks': [0, 1e4, 2e4, 3e4, 4e4],
    },
    {
        'name': '(b) RocksDB-tiered',
        'path': 'ycsbc_hotspot0.01_110GB_1GB/rocksdb-tiered',
        'ymax': 400,
        'yticks': [0, 100, 200, 300, 400],
    }
]
gs = gridspec.GridSpec(1, len(versions), figure=figure)

final_ops = []
for (version_idx, version) in enumerate(versions):
    subfig = plt.subplot(gs[0, version_idx])
    data_dir = os.path.join(dir, version['path'])
    version_data = common.VersionData(data_dir)

    final_ops.append(common.last_10p_ops(version_data))

    time = (version_data.ts_progress()['Timestamp(ns)'] - version_data.info()['run-start-timestamp(ns)']).values / 1e9
    time = time[:-1]
    progress = version_data.ts_progress()['operations-executed']
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
    subfig.text(0.5, -0.4, 'Time (Seconds)', fontsize=8, ha='center', va='center', transform=subfig.transAxes)
    plt.xlabel(version['name'], labelpad=10, fontsize=8)

tex = io.StringIO()
print('\defmacro{HDDHotrapDivRocksdbTiered}{%.0f}' %(final_ops[0] / final_ops[1]), file=tex)
tex = tex.getvalue()
print(tex)
open('hdd-test.tex', mode='w').write(tex)

pdf_path = dir + '/hdd-ops.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
