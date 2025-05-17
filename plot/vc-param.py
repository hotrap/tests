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

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

fontsize=9
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

info = os.path.join(data_dir, 'info.json')
info = json5.load(open(info))
vcsize = pd.read_table(os.path.join(data_dir, 'vc_param'), sep='\s+')
vcsize = vcsize[(vcsize['Timestamp(ns)'] >= info['run-start-timestamp(ns)']) & (vcsize['Timestamp(ns)'] < info['run-end-timestamp(ns)'])]
time = (vcsize['Timestamp(ns)'] - vcsize['Timestamp(ns)'].iloc[0]) / 1e9

plot_dir = os.path.join(data_dir, 'plot')
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = os.path.join(plot_dir, 'vc_param.pdf')
plt.plot(time, vcsize['hot-set-size-limit'])
plt.legend([1], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Size (Bytes)', fontdict=fonten)
plt.title('Hot set size of ralt')
plt.savefig(pdf_path, metadata={'CreationDate': None})
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
