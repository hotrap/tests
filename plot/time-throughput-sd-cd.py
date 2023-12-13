#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' dir mean_step')
	exit()

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

d = sys.argv[1]
mean_step = int(sys.argv[2])

first_level_in_cd = int(open(d + '/first-level-in-cd').read())
info_json = os.path.join(d, 'info.json')
info_json = json5.load(open(info_json))

def read_table(file):
    iostat_raw = pd.read_table(file, delim_whitespace=True)
    iostat_raw = iostat_raw[(iostat_raw['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (iostat_raw['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]
    iostat_raw['Time(Seconds)'] = (iostat_raw['Timestamp(ns)'] - iostat_raw['Timestamp(ns)'].iloc[0]) / 1e9
    iostat = iostat_raw[['rkB/s', 'wkB/s']].groupby(iostat_raw.index // mean_step).mean()
    iostat['Time(Seconds)'] = iostat_raw['Time(Seconds)'].groupby(iostat_raw.index // mean_step).first()
    return iostat
sd = read_table(d + '/iostat-sd.txt')
cd = read_table(d + '/iostat-cd.txt')

compaction_bytes = read_compaction_bytes_sd_cd(os.path.join(d, 'compaction-stats'), first_level_in_cd)
timestamps = np.array(compaction_bytes['Timestamp(ns)'])
run_phase = (timestamps >= info_json['run-start-timestamp(ns)']) & (timestamps < info_json['run-end-timestamp(ns)'])
timestamps = timestamps[run_phase]
compaction_bytes = compaction_bytes[run_phase]
time = (timestamps[1:] - timestamps[0]) / 1e9

throughput = compaction_bytes[1:].values - compaction_bytes[:-1].values
throughput = throughput[:,1:] / (throughput[:,0][:, np.newaxis] / 1e9)
throughput = pd.DataFrame(throughput, columns=['sd-read', 'sd-write', 'cd-read', 'cd-write'])
throughput['Time(Seconds)'] = time
throughput = throughput.groupby(throughput.index // mean_step).mean()

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)

pdf_path = plot_dir + '/time-throughput-sd-cd.pdf'
plt.plot(sd['Time(Seconds)'], (sd['rkB/s'] + sd['wkB/s']) / 1e3)
plt.plot(sd['Time(Seconds)'], (cd['rkB/s'] + cd['wkB/s']) / 1e3)
plt.plot(throughput['Time(Seconds)'], (throughput['sd-read'] + throughput['sd-write']) / 1e6)
plt.plot(throughput['Time(Seconds)'], (throughput['cd-read'] + throughput['cd-write']) / 1e6)
plt.legend(['SD', 'CD', 'SD-Compaction', 'CD-Compaction'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Throughput (MB/s)', fontdict=fonten)
plt.title('Throughput of SD and CD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()

pdf_path = plot_dir + '/time-compaction-throughput-rw.pdf'
plt.figure()
plt.plot(throughput['Time(Seconds)'], throughput['sd-read'] / 1e6)
plt.plot(throughput['Time(Seconds)'], throughput['sd-write'] / 1e6)
plt.plot(throughput['Time(Seconds)'], throughput['cd-read'] / 1e6)
plt.plot(throughput['Time(Seconds)'], throughput['cd-write'] / 1e6)
plt.legend(['read (SD)', 'write (SD)', 'read (CD)', 'write (CD)'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Throughput (MB/s)', fontdict=fonten)
plt.title('Compaction throughput of SD and CD')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
