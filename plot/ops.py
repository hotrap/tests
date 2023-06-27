#!/usr/bin/env python3

import sys

if len(sys.argv) != 3:
	print('Usage: ' + sys.argv[0] + ' dir mean_step')
	exit()

import os
import subprocess
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
progress_raw = pd.read_table(d + '/progress', delim_whitespace=True)
timestamp = (progress_raw['Timestamp(ns)'] - progress_raw['Timestamp(ns)'][0]).values / 1e9
timestamp = timestamp[0:len(timestamp)-1]
progress = progress_raw['operations-executed']
ops = progress[1:len(progress)].values - progress[:len(progress) - 1].values

def mean_every_n(a, n):
	split = len(a) - len(a) % n
	res = a[0:split].reshape(-1, n).mean(axis=1)
	if split != len(a):
		res = np.append(res, a[split:].mean())
	return res

timestamp = mean_every_n(timestamp, mean_step)
ops = mean_every_n(ops, mean_step)

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/ops.pdf'
plt.plot(timestamp, ops)
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('OPS', fontdict=fonten)
plt.title('OPS')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
