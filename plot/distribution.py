#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
	'font.family': 'sans-serif',
	'font.sans-serif': ['Times New Roman'],
})  # 设置全局字体plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

key_cnts = {}
for line in sys.stdin:
	line = line.strip()
	if line in key_cnts:
		key_cnts[line] += 1
	else:
 		key_cnts[line] = 1
key_cnts = sorted(key_cnts.items())

cnts = []
for (_, cnt) in key_cnts:
	cnts.append(cnt)
for i in range(1, len(cnts)):
	cnts[i] += cnts[i-1]
plt.plot(range(0, len(cnts)), cnts)
plt.xlabel('Key rank', fontdict=fonten)
plt.ylabel('Number of occurrences of smaller keys', fontdict=fonten)
plt.title('Key occurrence distribution')
plt.show()
plt.close()
