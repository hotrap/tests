from common import *

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter

def draw_cputime_breakdown(dir, size, pdf_name):
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

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(4.5)))

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['RO', 'RW', 'WH', 'UH']
    colors_left = [
        plt.get_cmap('Paired')(1),
        plt.get_cmap('Paired')(3),
        plt.get_cmap('Paired')(5),
        plt.get_cmap('Paired')(7),
        plt.get_cmap('Paired')(9),
        'white',
    ]
    colors_right = [
        plt.get_cmap('Paired')(0),
        plt.get_cmap('Paired')(2),
        plt.get_cmap('Paired')(4),
        'white',
    ]

    flush_stably_hot = {
        'path': 'flush-stably-hot',
        'colors': colors_left,
    }
    rocksdb_sd = {
        'path': 'rocksdb-sd',
        'colors': colors_right,
    }
    rocksdb_fat = {
        'path': 'rocksdb-fat',
        'colors': colors_right,
    }
    patterns = ['///', '\\\\\\', 'XXX', '......', 'ooo', '']

    gs = gridspec.GridSpec(1, 3)

    versions=[flush_stably_hot, rocksdb_sd]
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)
    subfig_anchor_y = 1.1

    def start_progress_fn(data_dir):
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return timestamp_to_progress(progress, info['run-start-timestamp(ns)'])
    def end_progress_fn(data_dir):
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return progress.iloc[-1]['operations-executed']

    def draw_cputime(start_progress_fn, end_progress_fn):
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.grid(axis='y')
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_powerlimits((-3, 3))
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.get_offset_text().set_fontsize(8)
        for (pivot, ycsb) in enumerate(ycsb_configs):
            workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
            data_dir = os.path.join(workload_dir, 'flush-stably-hot')
            start_progress = start_progress_fn(data_dir)
            end_progress = end_progress_fn(data_dir)
            for (version_idx, version) in enumerate(versions):
                data_dir = os.path.join(workload_dir, version['path'])
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                cputimes = pd.read_table(os.path.join(data_dir, 'cputimes'), delim_whitespace=True)
                timestamp_start = progress_to_timestamp(data_dir, start_progress)
                timestamp_end = progress_to_timestamp(data_dir, end_progress)
                cputimes = cputimes[(timestamp_start <= cputimes['Timestamp(ns)']) & (cputimes['Timestamp(ns)'] < timestamp_end)]
                cputimes = cputimes['cputime(s)'].iloc[-1] - cputimes['cputime(s)'].iloc[0]
                timers = pd.read_table(os.path.join(data_dir, 'timers'), delim_whitespace=True)
                timers = timers[(timestamp_start <= timers['Timestamp(ns)']) & (timers['Timestamp(ns)'] < timestamp_end)]
                timers = timers.iloc[-1] - timers.iloc[0]
                bottom = 0

                height = timers['get-cpu-nanos'] / 1e9
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                bottom += height

                height = timers['put-cpu-nanos'] / 1e9
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[1], color=version['colors'][1], edgecolor='black', linewidth=0.5)
                bottom += height

                height = timers['compaction-cpu-micros'] / 1e6
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[2], color=version['colors'][2], edgecolor='black', linewidth=0.5)
                bottom += height
                if version_idx == 0:
                    first_level_in_cd = int(open(os.path.join(data_dir, 'first-level-in-cd')).read())
                    checker = pd.read_table(os.path.join(data_dir, 'checker-' + str(first_level_in_cd - 1) + '-cputimes'), delim_whitespace=True)
                    checker = checker[(timestamp_start <= checker['Timestamp(ns)']) & (checker['Timestamp(ns)'] < timestamp_end)]
                    height = (checker.iloc[-1] - checker.iloc[0])['cputime(s)']
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[3], color=version['colors'][3], edgecolor='black', linewidth=0.5)
                    bottom += height

                    height = (timers['viscnts.compaction.cpu.nanos'] + timers['viscnts.flush.cpu.nanos'] + timers['viscnts.decay.scan.cpu.nanos'] + timers['viscnts.decay.write.cpu.nanos']) / 1e9
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[4], color=version['colors'][4], edgecolor='black', linewidth=0.5)
                    bottom += height
                height = cputimes - bottom
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[-1], color=version['colors'][-1], edgecolor='black', linewidth=0.5)
        plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.locator_params(axis='y', nbins=4)
        plt.ylabel('CPU time (seconds)', fontsize=8)

    subfig = plt.subplot(gs[0, 0])
    draw_cputime(start_progress_fn, warmup_finish_progress)
    plt.xlabel('(a) Warm-up phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_sd['colors']),
        ],
        ['HotRAP', 'RocksDB(SD)'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    subfig = plt.subplot(gs[0, 1])
    draw_cputime(warmup_finish_progress, end_progress_fn)
    plt.xlabel('(b) Stable phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_sd['colors']),
        ],
        ['HotRAP', 'RocksDB(SD)'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    workload='uniform'
    versions = [flush_stably_hot, rocksdb_fat]
    subfig = plt.subplot(gs[0, 2])
    draw_cputime(start_progress_fn, end_progress_fn)
    plt.xlabel('(c) Run phase of uniform', fontsize=8)
    subfig.legend(
        [
            MulticolorPatch(colors=flush_stably_hot['colors']),
            MulticolorPatch(colors=rocksdb_fat['colors']),
        ],
        ['HotRAP', 'RocksDB-fat'],
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    labels = []
    handles = []
    def all_versions(i):
        handles.append(MulticolorPatch(
            colors=[
                colors_left[i],
                colors_right[i],
            ],
            pattern=patterns[i],
        ))
    labels.append('Read')
    all_versions(0)
    labels.append('Insert')
    all_versions(1)
    labels.append('Compaction')
    all_versions(2)
    labels.append('Checker')
    handles.append(MulticolorPatch(colors=[flush_stably_hot['colors'][3]], pattern=patterns[3]))
    labels.append('RALT')
    handles.append(MulticolorPatch(colors=[flush_stably_hot['colors'][4]], pattern=patterns[4]))
    labels.append('Others')
    all_versions(-1)
    fig.legend(
        handles, labels,
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=8, ncol=6, loc='center', bbox_to_anchor=(0.5, 0.96), columnspacing=1
    )
    plt.tight_layout()
    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
