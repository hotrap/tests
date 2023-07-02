#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import pandas as pd
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
promoted_bytes_raw = pd.read_table(d + '/promoted-iter-bytes', delim_whitespace=True)
time = (promoted_bytes_raw['Timestamp(ns)'] - promoted_bytes_raw['Timestamp(ns)'][0]) / 1e9
promoted_bytes = promoted_bytes_raw['num-bytes']

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/promoted-bytes.pdf'
plt.plot(time, promoted_bytes)
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Promoted bytes', fontdict=fonten)
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
