#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

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
occurrences = pd.read_table(d + '/occurrences', names=['key', 'occurrences'], delim_whitespace=True)
key_hit_level = pd.read_table(d + '/key_hit_level', names=['key', 'hit-level'], delim_whitespace=True)
first_level_in_cd = int(open(d + '/first-level-in-cd').readline().strip())

key_hits = {}
for index, row in key_hit_level.iterrows():
    if row['hit-level'] < first_level_in_cd:
        key = row['key']
        if key in key_hits:
            key_hits[key] += 1
        else:
            key_hits[key] = 1

n = len(occurrences)
percentile=np.linspace(0, 1, n + 1)
occurrences_sum = [0]
for x in occurrences['occurrences']:
	occurrences_sum.append(occurrences_sum[len(occurrences_sum)-1] + x)
assert(len(occurrences_sum) == n + 1)

hit_sum = [0]
for key in occurrences['key']:
    if key in key_hits:
        hit = key_hits[key]
    else:
        hit = 0
    hit_sum.append(hit_sum[len(hit_sum)-1] + hit)

plt.plot(percentile, occurrences_sum)
plt.plot(percentile, hit_sum)
plt.legend(['# accessed', '# hit'], prop={'size': fontsize})
plt.xlabel('Percentile of key ranked by hotness', fontdict=fonten)
plt.ylabel('CDF', fontdict=fonten)
plt.title('Accuracy of hot identification')
plt.show()
