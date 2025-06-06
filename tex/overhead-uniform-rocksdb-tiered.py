#!/usr/bin/env python3
import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' dir')
    exit()
dir=sys.argv[1]

import os
import io
import math
import json5

ops1KiB = json5.load(open(os.path.join(dir, 'ycsb-sweep.json')))
ops200B = json5.load(open(os.path.join(dir, 'ops-200B.json')))
overhead = max(ops1KiB['OverheadUniformRocksdbTiered1KiB'], ops200B['OverheadUniformRocksdbTiered200B'])

overhead_pct = io.StringIO()
print("%.1f" %(overhead * 100), file=overhead_pct, end='')
overhead_pct = overhead_pct.getvalue()

tex = io.StringIO()
print('% Max overhead under uniform workloads compared to RocksDB-tiering', file=tex)
print('\defmacro{OverheadUniformRocksdbTiered}{' + overhead_pct + '\\%}', file=tex)
print('\defmacro{OverheadUniformRocksdbTieredCeil}{%d\\%%}' %math.ceil(float(overhead_pct)), file=tex)
tex = tex.getvalue()
print(tex)
open(os.path.join(dir, 'overhead-uniform-rocksdb-tiered.tex'), mode='w').write(tex)
