from common import *

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

# https://stackoverflow.com/a/77614517/13688160
# define an object that will be used by the legend
class MulticolorPatch(object):
    def __init__(self, colors, pattern=None):
        self.colors = colors
        self.pattern = pattern
class MulticolorPatchHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        width, height = handlebox.width, handlebox.height
        for i, c in enumerate(orig_handle.colors):
            patch = plt.Rectangle(
                [
                    width/len(orig_handle.colors) * i - handlebox.xdescent,
                    -handlebox.ydescent,
                ],
                width / len(orig_handle.colors),
                height, 
                facecolor=c, 
                edgecolor='black',
                hatch=orig_handle.pattern,
            )
            if i == 0:
                ret = patch
            handlebox.add_artist(patch)
        return ret

def draw_io_breakdown(dir, size, pdf_name):
    # Paper specific settings
    STANDARD_WIDTH = 17.8
    SINGLE_COL_WIDTH = STANDARD_WIDTH / 2
    DOUBLE_COL_WIDTH = STANDARD_WIDTH
    def cm_to_inch(value):
        return value/2.54

    mpl.rcParams.update({
        'hatch.linewidth': 0.5,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Times New Roman'],
    })
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(4)))

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['i-0%', 'i-50%', 'u-50%']
    flush_stably_hot = {
        'path': 'flush-stably-hot',
        # #66C2A5
        'colors': ['#016048', '#329176', '#67c3a6', '#9af7d8'],
    }
    rocksdb_sd = {
        'path': 'rocksdb-sd',
        # #8DA0CB
        'colors': ['#50648c', '#8c9fca', '#cde0ff'],
    }
    rocksdb_fat = {
        'path': 'rocksdb-fat',
        # #FC8D62
        'colors': ['#892c08', '#bc562f', '#ef8258', '#ffc092'],
    }
    patterns = ['///', 'XXX', '......', '|||', 'OOO']

    gs = gridspec.GridSpec(1, 3)

    versions=[flush_stably_hot, rocksdb_sd]
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)

    def start_progress_fn(data_dir):
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return timestamp_to_progress(progress, info['run-start-timestamp(ns)'])
    def end_progress_fn(data_dir):
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return progress.iloc[-1]['operations-executed']

    def draw_io(start_progress_fn, end_progress_fn):
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.grid(axis='y')
        for (pivot, ycsb) in enumerate(ycsb_configs):
            workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
            data_dir = os.path.join(workload_dir, 'flush-stably-hot')
            start_progress = start_progress_fn(data_dir)
            end_progress = end_progress_fn(data_dir)
            for (version_idx, version) in enumerate(versions):
                data_dir = os.path.join(workload_dir, version['path'])
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                timestamp_start = progress_to_timestamp(data_dir, start_progress)
                timestamp_end = progress_to_timestamp(data_dir, end_progress)
                def run_time_io_kB(fname):
                    iostat = pd.read_table(os.path.join(data_dir, fname), delim_whitespace=True)
                    iostat = iostat[(timestamp_start <= iostat['Timestamp(ns)']) & (iostat['Timestamp(ns)'] < timestamp_end)]
                    return iostat[['rkB/s', 'wkB/s']].sum().sum()
                device_io = (run_time_io_kB('iostat-sd.txt') + run_time_io_kB('iostat-cd.txt')) / 1e9

                bottom = 0

                progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
                progress = progress[(timestamp_start <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < timestamp_end)]
                get = (progress.iloc[-1] - progress.iloc[0])['get']
                height = get * 16 * 1024 / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                bottom += height

                compaction_bytes = read_compaction_bytes(data_dir)
                compaction_bytes = compaction_bytes[(timestamp_start <= compaction_bytes['Timestamp(ns)']) & (compaction_bytes['Timestamp(ns)'] < timestamp_end)]
                compaction_bytes = compaction_bytes.iloc[-1] - compaction_bytes.iloc[0]
                height = (compaction_bytes['read'] + compaction_bytes['write']) / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[1], color=version['colors'][1], edgecolor='black', linewidth=0.5)
                bottom += height

                height = device_io - bottom
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[-1], color=version['colors'][-1], edgecolor='black', linewidth=0.5)
        plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.ylabel('I/O (TB)', fontsize=8)

    subfig = plt.subplot(gs[0, 0])
    draw_io(start_progress_fn, warmup_finish_progress)
    plt.xlabel('(a) Warm-up phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_sd['colors']),
        ],
        ['HotRAP', 'RocksDB(SD)'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, 1.15), columnspacing=1,
    )

    subfig = plt.subplot(gs[0, 1])
    draw_io(warmup_finish_progress, end_progress_fn)
    plt.xlabel('(b) Stable phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_sd['colors']),
        ],
        ['HotRAP', 'RocksDB(SD)'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, 1.15), columnspacing=1,
    )

    workload='uniform'
    versions = [flush_stably_hot, rocksdb_fat]
    subfig = plt.subplot(gs[0, 2])
    draw_io(start_progress_fn, end_progress_fn)
    plt.xlabel('(c) Run phase of uniform', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_fat['colors']),
        ],
        ['HotRAP', 'RocksDB-fat'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, 1.15), columnspacing=1,
    )

    labels = []
    handles = []
    labels.append(r'Get $\times$ 16KiB')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][0], versions[1]['colors'][0]], pattern=patterns[0]))
    labels.append('Compaction')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][1], versions[1]['colors'][1]], pattern=patterns[1]))
    labels.append('RALT')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][2]], pattern=patterns[2]))
    labels.append('Others')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][-1], versions[1]['colors'][-1]], pattern=patterns[-1]))
    fig.legend(
        handles, labels,
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=8, ncol=4, loc='center', bbox_to_anchor=(0.5, 0.94)
    )

    plt.tight_layout()
    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
