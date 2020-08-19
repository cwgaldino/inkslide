#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inkSlide example 1."""

from pathlib import Path

import sys
sys.path.append('../..')
import inkSlide.inkFile as ink
import importlib
importlib.reload(ink)

# %% export many layers from many files using instructions file ================
filepath = 'layer2export.txt'

f = Path(filepath).open()
text = f.read()
f.close()

# exclude comments
labelLists = []
for line in text.splitlines():
    if line.startswith('#') or line=='':
        pass
    else:
        labelLists.append([label.strip() for label in line.split(',')])

# export
idx = 0
for labelList in labelLists:
    if labelList[0].startswith('file:'):
        presentation = ink.inkscapeFile(labelList[0].split('file:')[-1])
    else:
        filepath = Path(f'test_0/exported_{idx}.svg')
        presentation.exportLayerSet(labelList=labelList, filepath=filepath)
        idx +=1
