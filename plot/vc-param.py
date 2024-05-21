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
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))
vcsize = pd.read_table(os.path.join(data_dir, 'vc_param'), sep='\s+', header=None)
vcsize = vcsize[(vcsize[0] >= info['run-start-timestamp(ns)']) & (vcsize[0] < info['run-end-timestamp(ns)'])]
time = (vcsize[0] - vcsize[0].iloc[0]) / 1e9

plot_dir = os.path.join(data_dir, 'plot')
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = os.path.join(plot_dir, 'vc_param.pdf')
plt.plot(time, vcsize[1])
plt.legend([1], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (Bytes)', fontdict=fonten)
plt.title('Hot set size of viscnts')
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
