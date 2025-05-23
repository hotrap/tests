#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import io
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'common/'))
from io_breakdown import *

dir=sys.argv[1]
(min_portion, max_portion) = draw_io_breakdown(dir, '110GB_220GB_200B', 'fig12-io-breakdown-200B.pdf')

tex = io.StringIO()
print('\defmacro{RaltIoPortionMin}{%.1f\\%%}' %(min_portion * 100), file=tex)
print('\defmacro{RaltIoPortionMax}{%.1f\\%%}' %(max_portion * 100), file=tex)
tex = tex.getvalue()
print(tex)
open('io-breakdown-200B.tex', mode='w').write(tex)
