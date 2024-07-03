import os
import json5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def read_hit_rates(data_dir):
    first_level_in_sd = int(open(os.path.join(data_dir, 'first-level-in-sd')).read())
    last_tier0 = 0
    last_total = 0
    hit_rates = []
    for line in open(os.path.join(data_dir, 'num-accesses')):
        res = line.split(' ')
        timestamp = int(res[0])
        tier0 = 0
        total = 0
        for (level, num_accesses) in enumerate(res[1:]):
            num_accesses = int(num_accesses)
            total += num_accesses
            if level < first_level_in_sd:
                tier0 += num_accesses
        if total - last_total != 0:
            hit_rate = (tier0 - last_tier0) / (total - last_total)
            hit_rates.append(pd.Series([timestamp, hit_rate]))
            last_tier0 = tier0
            last_total = total
    hit_rates = pd.concat(hit_rates, axis=1).T
    hit_rates.columns = ['Timestamp(ns)', 'hit-rate']
    return hit_rates

def warmup_finish_timestamp(hit_rates):
    # Reguard 99% percentile hit rate as max, which should be stable
    threshold = np.quantile(hit_rates['hit-rate'], 0.99) * 0.95
    return hit_rates[hit_rates['hit-rate'] >= threshold].iloc[0]['Timestamp(ns)']

def timestamp_to_progress(progress, timestamp):
    return progress[progress['Timestamp(ns)'] >= timestamp].iloc[0]['operations-executed']

def warmup_finish_progress(data_dir):
    hit_rates = read_hit_rates(data_dir)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    return timestamp_to_progress(progress, warmup_finish_timestamp(hit_rates))

def progress_to_timestamp(data_dir, progress):
    v = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    v = v[v['operations-executed'] >= progress]
    if len(v) == 0:
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        return info['run-end-timestamp(ns)']
    return v.iloc[0]['Timestamp(ns)']

def ops_during_interval(data_dir, start_progress, end_progress):
    timestamp_start = progress_to_timestamp(data_dir, start_progress)
    timestamp_end = progress_to_timestamp(data_dir, end_progress)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), sep='\s+')
    progress = progress[(timestamp_start <= progress['Timestamp(ns)']) & (progress['Timestamp(ns)'] < timestamp_end)]
    operations_executed = progress.iloc[-1]['operations-executed'] - progress.iloc[0]['operations-executed']
    seconds = (progress.iloc[-1]['Timestamp(ns)'] - progress.iloc[0]['Timestamp(ns)']) / 1e9
    return operations_executed / seconds

def read_compaction_bytes(data_dir):
    compaction_bytes = []
    compaction_stats = open(os.path.join(data_dir, 'compaction-stats'))
    while True:
        line = compaction_stats.readline()
        if line == '':
            break
        s = line.split(' ')
        assert s[0] == 'Timestamp(ns)'
        timestamp = int(s[1])
        line = compaction_stats.readline()
        assert line == 'Level Read Write\n'
        read = 0
        write = 0
        level = 0
        while True:
            line = compaction_stats.readline()
            if line == ''  or line == '\n':
                break
            s = line.split(' ')
            assert s[0] == 'L' + str(level)
            read += int(s[1])
            write += int(s[2])
            level += 1
        compaction_bytes.append(pd.Series([timestamp, read, write]))
    compaction_bytes = pd.concat(compaction_bytes, axis=1).T
    compaction_bytes.columns = ['Timestamp(ns)', 'read', 'write']
    return compaction_bytes

def read_compaction_bytes_fd_sd(data_dir, first_level_in_sd):
    compaction_bytes = []
    compaction_stats = open(os.path.join(data_dir, 'compaction-stats'))
    while True:
        line = compaction_stats.readline()
        if line == '':
            break
        s = line.split(' ')
        assert s[0] == 'Timestamp(ns)'
        timestamp = int(s[1])
        line = compaction_stats.readline()
        assert line == 'Level Read Write\n'
        fd_read = 0
        fd_write = 0
        sd_read = 0
        sd_write = 0
        level = 0
        while True:
            line = compaction_stats.readline()
            if line == ''  or line == '\n':
                break
            s = line.split(' ')
            assert s[0] == 'L' + str(level)
            read = int(s[1])
            write = int(s[2])
            if level < first_level_in_sd:
                fd_read += read
                fd_write += write
            else:
                sd_read += read
                sd_write += write
            level += 1
        compaction_bytes.append(pd.Series([timestamp, fd_read, fd_write, sd_read, sd_write]))
    compaction_bytes = pd.concat(compaction_bytes, axis=1).T
    compaction_bytes.columns = ['Timestamp(ns)', 'fd-read', 'fd-write', 'sd-read', 'sd-write']
    return compaction_bytes

def read_rand_read_bytes_fd_sd(data_dir, first_level_in_sd):
    rand_read_bytes = []
    for line in open(os.path.join(data_dir, 'rand-read-bytes')):
        if line == '':
            break
        s = line.split(' ')
        fd = 0
        sd = 0
        timestamp_ns = int(s[0])
        for level, bytes in enumerate(s[1:]):
            bytes = int(bytes)
            if level < first_level_in_sd:
                fd += bytes
            else:
                sd += bytes
        rand_read_bytes.append(pd.Series([timestamp_ns, fd, sd]))
    rand_read_bytes = pd.concat(rand_read_bytes, axis=1).T
    rand_read_bytes.columns = ['Timestamp(ns)', 'fd', 'sd']
    return rand_read_bytes
