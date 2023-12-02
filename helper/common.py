import os
import json5
import numpy as np
import pandas as pd

def read_hit_rates(data_dir):
    first_level_in_cd = int(open(os.path.join(data_dir, 'first-level-in-cd')).read())
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
            if level < first_level_in_cd:
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
    threshold = hit_rates['hit-rate'].max() * 0.95
    return hit_rates[hit_rates['hit-rate'] >= threshold].iloc[0]['Timestamp(ns)']

def timestamp_to_progress(progress, timestamp):
    return progress[progress['Timestamp(ns)'] >= timestamp].iloc[0]['operations-executed']

def warmup_finish_progress(data_dir):
    hit_rates = read_hit_rates(data_dir)
    progress = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
    return timestamp_to_progress(progress, warmup_finish_timestamp(hit_rates))

def progress_to_timestamp(data_dir, progress):
    v = pd.read_table(os.path.join(data_dir, 'progress'), delim_whitespace=True)
    v = v[v['operations-executed'] >= progress]
    if len(v) == 0:
        info = json5.load(open(os.path.join(data_dir, 'info.json')))
        return info['run-end-timestamp(ns)']
    return v.iloc[0]['Timestamp(ns)']

def read_compaction_bytes(path):
    compaction_bytes = []
    compaction_stats = open(path)
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

def read_compaction_bytes_sd_cd(path, first_level_in_cd):
    compaction_bytes = []
    compaction_stats = open(path)
    while True:
        line = compaction_stats.readline()
        if line == '':
            break
        s = line.split(' ')
        assert s[0] == 'Timestamp(ns)'
        timestamp = int(s[1])
        line = compaction_stats.readline()
        assert line == 'Level Read Write\n'
        sd_read = 0
        sd_write = 0
        cd_read = 0
        cd_write = 0
        level = 0
        while True:
            line = compaction_stats.readline()
            if line == ''  or line == '\n':
                break
            s = line.split(' ')
            assert s[0] == 'L' + str(level)
            read = int(s[1])
            write = int(s[2])
            if level < first_level_in_cd:
                sd_read += read
                sd_write += write
            else:
                cd_read += read
                cd_write += write
            level += 1
        compaction_bytes.append(pd.Series([timestamp, sd_read, sd_write, cd_read, cd_write]))
    compaction_bytes = pd.concat(compaction_bytes, axis=1).T
    compaction_bytes.columns = ['Timestamp(ns)', 'sd-read', 'sd-write', 'cd-read', 'cd-write']
    return compaction_bytes

