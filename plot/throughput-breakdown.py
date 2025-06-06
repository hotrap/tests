#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' dir mean-step')
	exit()
dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

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

versions=[
    {
        'name': '(a) RocksDB-FD',
        'path': 'rocksdb-fd',
    },
    {
        'name': '(b) ' + common.sysname,
        'path': 'hotrap',
    },
]

linewidth=0.5
num_marks=5
markersize=1
markersize_x=2

gs = gridspec.GridSpec(1, len(versions), figure=figure)
for (i, version) in enumerate(versions):
    subfig = plt.subplot(gs[0, i])
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(axis='y')
    data_dir = os.path.join(dir, version['path'])
    version_data = common.VersionData(data_dir)
    info = version_data.info()

    first_level_in_sd = int(open(data_dir + '/first-level-in-last-tier').read())
    def read_table(file):
        iostat_raw = pd.read_table(file, sep='\s+')
        iostat_raw = version_data.run_phase(iostat_raw)
        iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'].iloc[0]) / 1e9
        iostat = iostat_raw[['rkB/s', 'wkB/s']].groupby(iostat_raw.index // mean_step).mean()
        iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
        return iostat
    fd = read_table(data_dir + '/iostat-fd.txt')
    sd = read_table(data_dir + '/iostat-sd.txt')

    markevery = int(len(fd['Time(Seconds)']) / num_marks)
    fd_GB = (fd['rkB/s'] + fd['wkB/s']) / 1e6
    sd_GB = (sd['rkB/s'] + sd['wkB/s']) / 1e6
    ax.plot(sd['Time(Seconds)'], fd_GB, marker='o', linewidth=linewidth, markersize=markersize, markevery=markevery)
    ax.plot(sd['Time(Seconds)'], sd_GB, marker='D', linewidth=linewidth, markersize=markersize, markevery=markevery)
    markevery = int(len(sd['Time(Seconds)']) / num_marks)

    compaction_bytes = common.read_compaction_bytes_per_tier(data_dir, first_level_in_sd)
    compaction_bytes = version_data.run_phase(compaction_bytes)
    time = (compaction_bytes[1:]['Timestamp(ns)'].values - info['run-start-timestamp(ns)']) / 1e9

    throughput = compaction_bytes[1:].values - compaction_bytes[:-1].values
    throughput = throughput[:,1:] / (throughput[:,0][:, np.newaxis] / 1e9)
    throughput = pd.DataFrame(throughput, columns=compaction_bytes.columns[1:])
    throughput['Time(Seconds)'] = time
    throughput = throughput.groupby(throughput.index // mean_step).mean()

    fd_compaction_GB = (throughput['0-read'] + throughput['0-write']) / 1e9
    ax.plot(throughput['Time(Seconds)'], fd_compaction_GB, marker='s', linewidth=linewidth, markersize=markersize, markevery=markevery)
    if version['path'] == 'rocksdb-fd':
        sd_compaction_GB = np.zeros(len(throughput['Time(Seconds)']))
    else:
        sd_compaction_GB = (throughput['1-read'] + throughput['1-write']) / 1e9
    ax.plot(throughput['Time(Seconds)'], sd_compaction_GB, marker='x', linewidth=linewidth, markersize=markersize_x, markevery=markevery)

    rand_read_bytes = common.read_rand_read_bytes_per_tier(data_dir, first_level_in_sd)
    rand_read_bytes = version_data.run_phase(rand_read_bytes)
    time = (rand_read_bytes['Timestamp(ns)'][1:] - info['run-start-timestamp(ns)']) / 1e9
    rand_read_bytes = rand_read_bytes.iloc[:,1:].sum(axis=1)
    get_GB = (rand_read_bytes[1:].values - rand_read_bytes[:-1].values) / 1e9
    get_GB = pd.DataFrame({
        'Time(s)': time,
        'Throughput(GB/s)': get_GB,
    })
    get_GB = get_GB.groupby(get_GB.index // mean_step).mean()
    ax.plot(get_GB['Time(s)'], get_GB['Throughput(GB/s)'], color='black', linestyle='dashed', linewidth=linewidth, markersize=markersize, markevery=markevery)
    subfig.text(0.5, -0.35, 'Time (Seconds)', fontsize=9, ha='center', va='center', transform=subfig.transAxes)
    plt.xticks(fontsize=9)
    if 'ticks' in version:
        plt.yticks(version['ticks'], fontsize=9)
    else:
        plt.yticks(fontsize=9)
    ax.set_ylim(bottom=0)
    plt.xlabel(version['name'], labelpad=10, fontsize=9)
    if i == 0:
        plt.ylabel('Throughput (GB/s)', fontsize=9)

figure.legend(['FD', 'SD', 'FD-Compaction', 'SD-Compaction', 'Get'], fontsize=9, ncol=3, loc='center', bbox_to_anchor=(0.5, 1.15))
pdf_path = 'throughput-breakdown.pdf'
plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
