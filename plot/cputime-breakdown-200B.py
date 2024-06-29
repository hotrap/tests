#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()
dir=sys.argv[1]

import io
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'common/'))
from cputime_breakdown import *

(min_portion, max_portion) = draw_cputime_breakdown(dir, '110GB_220GB_200B', 'cputime-breakdown-200B.pdf')

tex = io.StringIO()
print('\defmacro{RaltCpuPortionMin}{%.1f\\%%}' %(min_portion * 100), file=tex)
print('\defmacro{RaltCpuPortionMax}{%.1f\\%%}' %(max_portion * 100), file=tex)
tex = tex.getvalue()
print(tex)
open('cpu-breakdown-200B.tex', mode='w').write(tex)
