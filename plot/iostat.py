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
    })  # 设置全局字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

d = sys.argv[1]
iostat = pd.read_table(d + '/iostat.sh.txt', delim_whitespace=True)

iostat['Time(Seconds)'] = (iostat['Timestamp(ns)'] - iostat['Timestamp(ns)'][0]) / 1e9
plt.plot(iostat['Time(Seconds)'], iostat['sd_tps'])
plt.plot(iostat['Time(Seconds)'], iostat['cd_tps'])
plt.legend(['SD', 'CD'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('TPS', fontdict=fonten)
plt.title('TPS of SD and CD')
plt.show(block=False)
plt.figure()

plt.plot(iostat['Time(Seconds)'], iostat['sd_kB_read/s'] / 1e3)
plt.plot(iostat['Time(Seconds)'], iostat['sd_kB_wrtn/s'] / 1e3)
plt.plot(iostat['Time(Seconds)'], iostat['cd_kB_read/s'] / 1e3)
plt.plot(iostat['Time(Seconds)'], iostat['cd_kB_wrtn/s'] / 1e3)
plt.legend(['read (SD)', 'write (SD)', 'read (CD)', 'write (CD)'], prop={'size': fontsize})
plt.xlabel('Time (Seconds)', fontdict=fonten)
plt.ylabel('Throughput (MB/s)', fontdict=fonten)
plt.title('Throughput of SD and CD')
plt.show()
