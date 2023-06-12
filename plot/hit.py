#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import subprocess
import matplotlib as mpl
import matplotlib.pyplot as plt

fontsize=9
fonten = {'family': 'Times New Roman', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Times New Roman'],
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)

d = sys.argv[1]
res_path = d + '/1'
if not os.path.exists(res_path):
	subprocess.call([dname + '/helper/hit', d])
if not os.path.exists(res_path + '/hit.pdf'):
	occurrences_cdf = [int(line) for line in open(res_path + '/occurrences_cdf')]
	hits_cdf = [int(line) for line in open(res_path + '/hits_cdf')]
	assert(len(occurrences_cdf) == len(hits_cdf))

	plt.plot(occurrences_cdf)
	plt.plot(hits_cdf)
	plt.legend(['# accessed', '# hit'], prop={'size': fontsize})
	plt.xlabel('Keys ranked by hotness', fontdict=fonten)
	plt.ylabel('CDF', fontdict=fonten)
	plt.title('Accuracy of hot identification')
	plt.savefig(res_path + '/hit.pdf')
if 'DISPLAY' in os.environ:
	subprocess.call(['evince', res_path + '/hit.pdf'])
