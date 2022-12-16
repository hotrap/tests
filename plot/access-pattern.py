#!/usr/bin/env python3

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
	'font.family': 'sans-serif',
	'font.sans-serif': ['Times New Roman'],
})  # 设置全局字体plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

keys = []
for line in sys.stdin:
	key = line.strip()
	keys.append(key)
keys_sorted = sorted(set(keys))
indexes = []
for key in keys:
	indexes.append(keys_sorted.index(key))
# plt.scatter(range(0, len(indexes)), indexes, marker='.')
plt.scatter(range(0, len(indexes)), indexes, marker=',', s=0.5)
plt.xlabel('Time', fontdict=fonten)
plt.ylabel('Key rank', fontdict=fonten)
plt.title('Access pattern')
plt.show()
plt.close()
