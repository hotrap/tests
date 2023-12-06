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

def draw_hotspot_cputime(dir, size, pdf_name):
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

    fig = plt.figure(dpi = 300, figsize = (cm_to_inch(SINGLE_COL_WIDTH), cm_to_inch(4)))

    workload='hotspot0.05'
    ycsb_configs=['ycsbc', 'read_0.5_insert_0.5', 'ycsba']
    cluster_labels = ['i-0%', 'i-50%', 'u-50%']
    versions=[
        {
            'path': 'flush-stably-hot',
            # #66C2A5
            'colors': ['#01654d', '#208369', '#44a185', '#64c0a3', '#83e0c2', '#a8ffe6'],
        },
        {
            'path': 'rocksdb-sd',
            # #8DA0CB
            'colors': ['#2d4469', '#5c7098', '#8da0cb', '#c0d3ff'],
        },
    ]
    patterns = ['///', '\\\\\\', 'XXX', '|||', '......', 'OOO']

    gs = gridspec.GridSpec(1, 2)
    bar_width = 1 / (len(versions) + 1)
    cluster_width = bar_width * len(versions)

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

                height = timers['read-cpu-nanos'] / 1e9
                ax.bar(x, height, bottom=bottom, width=bar_width, hatch=patterns[0], color=version['colors'][0], edgecolor='black', linewidth=0.5)
                bottom += height

                height = timers['insert-cpu-nanos'] / 1e9
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
    plt.xlabel('(a) CPU time of warm-up phase', fontsize=8)

    subfig = plt.subplot(gs[0, 1])
    draw_cputime(warmup_finish_progress, end_progress_fn)
    plt.xlabel('(b) CPU time of stable phase', fontsize=8)

    labels = []
    handles = []
    labels.append('HotRAP')
    handles.append(MulticolorPatch(colors=versions[0]['colors']))
    labels.append('RocksDB(SD)')
    handles.append(MulticolorPatch(colors=versions[1]['colors']))
    labels.append('Read')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][0], versions[1]['colors'][0]], pattern=patterns[0]))
    labels.append('Insert')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][1], versions[1]['colors'][1]], pattern=patterns[1]))
    labels.append('Compaction')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][2], versions[1]['colors'][2]], pattern=patterns[2]))
    labels.append('Checker')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][3]], pattern=patterns[3]))
    labels.append('RALT')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][4]], pattern=patterns[4]))
    labels.append('Others')
    handles.append(MulticolorPatch(colors=[versions[0]['colors'][-1], versions[1]['colors'][-1]], pattern=patterns[-1]))
    fig.legend(
        handles, labels,
        handler_map={MulticolorPatch: MulticolorPatchHandler()},
        fontsize=8, ncol=4, loc='center', bbox_to_anchor=(0.5, 1.03), columnspacing=1
    )
    plt.tight_layout()
    pdf_path = os.path.join(dir, pdf_name)
    plt.savefig(pdf_path, bbox_inches='tight', pad_inches=0.01)
    print('Plot saved to ' + pdf_path)
    if 'DISPLAY' in os.environ:
        plt.show()