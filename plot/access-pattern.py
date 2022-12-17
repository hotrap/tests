#!/usr/bin/env python3

import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
# pip3 install mpl-scatter-density
import mpl_scatter_density

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
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
ax.scatter_density(range(0, len(indexes)), indexes, color='black')
ax.set_xlabel('Time', fontdict=fonten)
ax.set_ylabel('Key rank', fontdict=fonten)
# ax.set_xlim(-0.5, 1.5)
# ax.set_ylim(-0.5, 1.5)
fig.suptitle('Access pattern')
plt.show()
plt.close()
