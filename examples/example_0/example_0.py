#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inkSlide example 0."""

from pathlib import Path
from PyPDF2 import PdfFileMerger

import sys
sys.path.append('../..')
import inkSlide.inkFile as ink
import importlib
importlib.reload(ink)

# %% get information from file =================================================
presentation = ink.inkscapeFile('presentation_A.svg')  # import .svg
presentation.filepath
presentation.filename
presentation.prefix
presentation.endOfFile
presentation.layers
presentation.getLabels()

# %% export one layer ==========================================================
presentation = ink.inkscapeFile('presentation_A.svg')
presentation.exportLayerSet(labelList=['Title', 'Title flourishing', 'Title flourishing2'], filepath='./test_0/exported')

# %% export many layers from one file ==========================================
presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['Title', 'Title flourishing', 'Title flourishing2'],
              ['Slide 2'],
              ['Slide 3'],
              ['Important slide'],
              ['The end']
             ]

for idx, labelList in enumerate(labelLists):
    filepath = Path(f'test_1/exported_{idx}.svg')
    presentation.exportLayerSet(labelList=labelList, filepath=filepath)

# %% export many layers from many files =====================================
output_folder = 'layers_1'

presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['Title', 'Title flourishing', 'Title flourishing2'],
              ['Slide 2'],
              ['Slide 3'],
             ]
idx = 0
for labelList in labelLists:
    filepath = Path(f'test_2/exported_{idx}.svg')
    presentation.exportLayerSet(labelList=labelList, filepath=filepath)
    idx +=1

presentation = ink.inkscapeFile('presentation_B.svg')
labelLists = [['Slide 1'],
              ['Slide 2'],
             ]
for idx2, labelList in enumerate(labelLists):
    filepath = Path(f'test_2/exported_{idx}.svg')
    presentation.exportLayerSet(labelList=labelList, filepath=filepath)
    idx +=1

presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['The end'],
             ]
for idx3, labelList in enumerate(labelLists):
    filepath = Path(f'test_2/exported_{idx}.svg')
    presentation.exportLayerSet(labelList=labelList, filepath=filepath)
    idx +=1


# %% export many layers to pdf file ============================================
presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['Title', 'Title flourishing', 'Title flourishing2'],
              ['Slide 2'],
              ['Slide 3'],
              ['Important slide'],
              ['The end']
             ]

for idx, labelList in enumerate(labelLists):
    filepath = Path(f'test_3/exported_{idx}')
    # presentation.exportLayerSet2Pdf(labelList=labelList, filepath=filepath, converter='inkscape0.9')
    # presentation.exportLayerSet2Pdf(labelList=labelList, filepath=filepath, converter='inkscape1')
    presentation.exportLayerSet2Pdf(labelList=labelList, filepath=filepath, converter='svglib')
