#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

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

d = sys.argv[1]
num_bytes = pd.read_table(d + '/promoted-or-retained-bytes', delim_whitespace=True)
info_json = os.path.join(d, 'info.json')
info_json = json5.load(open(info_json))
num_bytes = num_bytes[(num_bytes['Timestamp(ns)'] >= info_json['run-start-timestamp(ns)']) & (num_bytes['Timestamp(ns)'] < info_json['run-end-timestamp(ns)'])]

timestamp_start_ns = num_bytes['Timestamp(ns)'].iloc[0]
timestamp = (num_bytes['Timestamp(ns)'] - timestamp_start_ns) / 1e9

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
	os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/promoted-or-retained-bytes.pdf'
plt.plot(timestamp, num_bytes['by-flush'])
plt.plot(timestamp, num_bytes['2sdlast'])
plt.plot(timestamp, num_bytes['2cdfront'])
plt.plot(timestamp, num_bytes['retained'])
plt.legend(['By flush to L0', 'To the last level in SD', 'To shallower levels in CD', 'Retained'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Promoted bytes', fontdict=fonten)
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
	plt.show()
