import common

import os
import json5
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
from matplotlib.patches import Patch

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

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(DOUBLE_COL_WIDTH), cm_to_inch(4.5)))

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.75_insert_0.25', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['RO', 'RW', 'WH', 'UH']
    colors_left = [
        plt.get_cmap('Paired')(1), plt.get_cmap('Paired')(3),
        plt.get_cmap('Paired')(5), plt.get_cmap('Paired')(7),
        plt.get_cmap('Paired')(9),
        'white',
    ]
    colors_right = [
        plt.get_cmap('Paired')(0), plt.get_cmap('Paired')(2),
        plt.get_cmap('Paired')(4), plt.get_cmap('Paired')(6),
        'white',
    ]
    promote_stably_hot = {
        'path': 'promote-stably-hot',
        'colors': colors_left,
        'legend-colors': colors_left,
    }
    rocksdb_sd = {
        'path': 'rocksdb-sd',
        'colors': colors_right,
        'legend-colors': [colors_right[i] for i in [1, 3, 4]],
    }
    rocksdb_fat = {
        'path': 'rocksdb-fat',
        'colors': colors_right,
        'legend-colors': colors_right,
    }
    patterns = ['///', '\\\\\\', '......', 'XXX', '', '']

    gs = gridspec.GridSpec(1, 3)

    versions=[promote_stably_hot, rocksdb_sd]
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)
    subfig_anchor_y = 1.1

    def start_progress_fn(data_dir):
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return common.timestamp_to_progress(progress, info['run-start-timestamp(ns)'])
    def end_progress_fn(data_dir):
        progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
        return progress.iloc[-1]['operations-executed']

    def draw_io(start_progress_fn, end_progress_fn):
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.grid(axis='y')
        for (pivot, ycsb) in enumerate(ycsb_configs):
            workload_dir = os.path.join(dir, ycsb + '_' + workload + '_' + size)
            data_dir = os.path.join(workload_dir, 'promote-stably-hot')
            start_progress = start_progress_fn(data_dir)
            end_progress = end_progress_fn(data_dir)
            for (version_idx, version) in enumerate(versions):
                data_dir = os.path.join(workload_dir, version['path'])
                x = pivot - cluster_width / 2 + bar_width / 2 + version_idx * bar_width
                timestamp_start = common.progress_to_timestamp(data_dir, start_progress)
                timestamp_end = common.progress_to_timestamp(data_dir, end_progress)
                first_level_in_cd = int(open(os.path.join(data_dir, 'first-level-in-cd')).read())
                def run_time_io_kB(fname):
                    iostat = pd.read_table(os.path.join(data_dir, fname), delim_whitespace=True)
                    iostat = iostat[(timestamp_start <= iostat['Timestamp(ns)']) & (iostat['Timestamp(ns)'] < timestamp_end)]
                    return iostat[['rkB/s', 'wkB/s']].sum().sum()
                device_io = (run_time_io_kB('iostat-sd.txt') + run_time_io_kB('iostat-cd.txt')) / 1e9

                bottom = 0

                rand_read_bytes = common.read_rand_read_bytes_sd_cd(data_dir, first_level_in_cd)
                rand_read_bytes = rand_read_bytes[(timestamp_start <= rand_read_bytes['Timestamp(ns)']) & (rand_read_bytes['Timestamp(ns)'] < timestamp_end)]
                rand_read_bytes = rand_read_bytes.iloc[-1] - rand_read_bytes.iloc[0]

                if version['path'] == 'rocksdb-sd':
                    assert rand_read_bytes['cd'] == 0
                else:
                    height = rand_read_bytes['cd'] / 1e12
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = rand_read_bytes['sd'] / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[1], color=version['colors'][1], edgecolor='black', linewidth=0.5)
                bottom += height

                compaction_bytes = common.read_compaction_bytes_sd_cd(data_dir, first_level_in_cd)
                compaction_bytes = compaction_bytes[(timestamp_start <= compaction_bytes['Timestamp(ns)']) & (compaction_bytes['Timestamp(ns)'] < timestamp_end)]
                compaction_bytes = compaction_bytes.iloc[-1] - compaction_bytes.iloc[0]

                if version['path'] == 'rocksdb-sd':
                    assert compaction_bytes['cd-read'] == 0
                    assert compaction_bytes['cd-write'] == 0
                else:
                    height = (compaction_bytes['cd-read'] + compaction_bytes['cd-write']) / 1e12
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[2], color=version['colors'][2], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = (compaction_bytes['sd-read'] + compaction_bytes['sd-write']) / 1e12
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[3], color=version['colors'][3], edgecolor='black', linewidth=0.5)
                bottom += height

                if version['path'] == 'promote-stably-hot':
                    viscnts_io = pd.read_table(os.path.join(data_dir, 'viscnts-io'), delim_whitespace=True)
                    viscnts_io = viscnts_io[(timestamp_start <= viscnts_io['Timestamp(ns)']) & (viscnts_io['Timestamp(ns)'] < timestamp_end)]
                    viscnts_io = viscnts_io.iloc[-1] - viscnts_io.iloc[0]
                    height = (viscnts_io['read'] + viscnts_io['write']) / 1e12
                    ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[4], color=version['colors'][4], edgecolor='black', linewidth=0.5)
                    bottom += height

                height = device_io - bottom
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[-1], color=version['colors'][-1], edgecolor='black', linewidth=0.5)
        plt.xticks(range(0, len(cluster_labels)), cluster_labels, fontsize=8)
        plt.yticks(fontsize=8)
        plt.ylabel('I/O (TB)', fontsize=8)

    subfig = plt.subplot(gs[0, 0])
    draw_io(start_progress_fn, common.warmup_finish_progress)
    plt.xlabel('(a) Warm-up phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=promote_stably_hot['legend-colors']),
            common.MulticolorPatch(colors=rocksdb_sd['legend-colors']),
        ],
        ['HotRAP', 'RocksDB(FD)'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    subfig = plt.subplot(gs[0, 1])
    draw_io(common.warmup_finish_progress, end_progress_fn)
    plt.xlabel('(b) Stable phase of hotspot-5%', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=promote_stably_hot['legend-colors']),
            common.MulticolorPatch(colors=rocksdb_sd['legend-colors']),
        ],
        ['HotRAP', 'RocksDB(FD)'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    workload='uniform'
    versions = [promote_stably_hot, rocksdb_fat]
    subfig = plt.subplot(gs[0, 2])
    draw_io(start_progress_fn, end_progress_fn)
    plt.xlabel('(c) Run phase of uniform', fontsize=8)
    subfig.legend(
        [
            common.MulticolorPatch(colors=promote_stably_hot['legend-colors']),
            common.MulticolorPatch(colors=rocksdb_fat['legend-colors']),
        ],
        ['HotRAP', 'RocksDB-fat'],
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=6, ncol=2, loc='center', bbox_to_anchor=(0.6, subfig_anchor_y), columnspacing=1,
    )

    def get_fig_legend(i):
        return common.MulticolorPatch(colors=[colors_left[i], colors_right[i]], pattern=patterns[i])
    labels = []
    handles = []
    labels.append(r'Get in SD')
    handles.append(get_fig_legend(0))
    labels.append(r'Get in FD')
    handles.append(get_fig_legend(1))
    labels.append('Compaction in SD')
    handles.append(get_fig_legend(2))
    labels.append('Compaction in FD')
    handles.append(get_fig_legend(3))
    labels.append('RALT')
    handles.append(common.MulticolorPatch(colors=[colors_left[4]], pattern=patterns[4]))
    labels.append('Others')
    assert colors_left[-1] == colors_right[-1]
    handles.append(common.MulticolorPatch(colors=[colors_left[-1]], pattern=patterns[-1]))
    fig.legend(
        handles, labels,
        handler_map={common.MulticolorPatch: common.MulticolorPatchHandler()},
        fontsize=8, ncol=6, loc='center', bbox_to_anchor=(0.5, 0.96)
    )

    plt.tight_layout()
    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()
