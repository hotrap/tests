#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
data_dir = sys.argv[1]

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))
data = pd.read_table(os.path.join(data_dir, 'ralt-sizes'), sep='\s+')
data = data[(data['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (data['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
time = (data['Timestamp(ns)'] - data['Timestamp(ns)'].iloc[0]) / 1e9

plt.plot(time, data['real-phy-size'])
plt.plot(time, data['real-hot-size'])
plt.legend(['Physical size', 'Hot set size'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (Bytes)', fontdict=fonten)
plt.title('RALT sizes')

plot_dir = os.path.join(data_dir, 'plot')
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = os.path.join(plot_dir, 'ralt-sizes.pdf')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
