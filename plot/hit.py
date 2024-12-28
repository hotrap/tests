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
fonten = {'family': 'Linux Libertine O', 'size': fontsize}

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Linux Libertine O'],
})
plt.rcParams['axes.unicode_minus'] = False

d = sys.argv[1]
rank_reads_hits = pd.read_table(d + '/hit', sep='\s+')

plt.plot(rank_reads_hits['key-rank'], rank_reads_hits['reads'])
legends = ['# accessed']
plt.plot(rank_reads_hits['key-rank'], rank_reads_hits['hits'])
legends.append('# hit')
plt.legend(legends, prop={'size': fontsize})
plt.xlabel('Keys ranked by hotness', fontdict=fonten)
plt.ylabel('CDF', fontdict=fonten)

expected_num_reads_of_hot = 110 * 0.1 / 10
last_rank = 0
last_total_reads = 0
for _, row in rank_reads_hits.iterrows():
    rank = row['key-rank']
    num_keys = rank - last_rank
    total_reads = row['reads']
    reads = total_reads - last_total_reads
    if reads / num_keys < expected_num_reads_of_hot:
        break
    last_rank = rank
    last_total_reads = total_reads
plt.axvline(last_rank, linewidth=0.5, linestyle='--', color='black')

plot_dir = d + '/plot'
if not os.path.exists(plot_dir):
    os.system('mkdir -p ' + plot_dir)
pdf_path = plot_dir + '/hit.pdf'
plt.savefig(pdf_path)
print('Plot saved to ' + pdf_path)
if 'DISPLAY' in os.environ:
    plt.show()
