#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' data-dir mean-step')
	exit()
data_dir = sys.argv[1]
mean_step = int(sys.argv[2])

import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
from common import *

import json5
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

first_level_in_cd = int(open(data_dir + '/first-level-in-cd').read())
info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))

def read_table(file):
    iostat_raw = pd.read_table(file, delim_whitespace=True)
    iostat_raw = iostat_raw[(iostat_raw['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (iostat_raw['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
    iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'].iloc[0]) / 1e9
    iostat = iostat_raw[['rkB/s', 'wkB/s']].groupby(iostat_raw.index // mean_step).mean()
    iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
    return iostat
sd = read_table(data_dir + '/iostat-sd.txt')
cd = read_table(data_dir + '/iostat-cd.txt')

compaction_bytes = read_compaction_bytes_sd_cd(data_dir, first_level_in_cd)
timestamps = np.array(compaction_bytes['Timestamp(ns)'])
run_phase = (timestamps >= info['run-start-timestamp(ns)']) & (timestamps < info['run-end-timestamp(ns)'])
timestamps = timestamps[run_phase]
compaction_bytes = compaction_bytes[run_phase]
time = (timestamps[1:] - timestamps[0]) / 1e9

throughput = compaction_bytes[1:].values - compaction_bytes[:-1].values
throughput = throughput[:,1:] / (throughput[:,0][:, np.newaxis] / 1e9)
throughput = pd.DataFrame(throughput, columns=['sd-read', 'sd-write', 'cd-read', 'cd-write'])
throughput['Time(Seconds)'] = time
throughput = throughput.groupby(throughput.index // mean_step).mean()
plt.plot(sd['Time(Seconds)'], (sd['rkB/s'] + sd['wkB/s']) / 1e3)
plt.plot(sd['Time(Seconds)'], (cd['rkB/s'] + cd['wkB/s']) / 1e3)
plt.plot(throughput['Time(Seconds)'], (throughput['sd-read'] + throughput['sd-write']) / 1e6)
plt.plot(throughput['Time(Seconds)'], (throughput['cd-read'] + throughput['cd-write']) / 1e6)

rand_read_bytes = read_rand_read_bytes_sd_cd(data_dir, first_level_in_cd)
rand_read_bytes = rand_read_bytes[(info['run-start-timestamp(ns)'] <= rand_read_bytes['Timestamp(ns)']) & (rand_read_bytes['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
time = (rand_read_bytes['Timestamp(ns)'][1:] - info['run-start-timestamp(ns)']) / 1e9
rand_read_bytes = rand_read_bytes['sd'] + rand_read_bytes['cd']
get_throughput = pd.DataFrame({
        'Time(s)': time,
        'Throughput(B/s)': rand_read_bytes[1:].values - rand_read_bytes[:-1].values,
})
get_throughput = get_throughput.groupby(get_throughput.index // mean_step).mean()
plt.plot(get_throughput['Time(s)'], get_throughput['Throughput(B/s)'] / 1e6)

plot_dir = data_dir + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)

plt.legend(['SD', 'CD', 'SD-Compaction', 'CD-Compaction', 'Get'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Throughput (MB/s)', fontdict=fonten)
plt.title('Throughput of SD and CD')
pdf_path = plot_dir + '/time-throughput-sd-cd.pdf'
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
