#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inkmanip example 0."""

import sys
sys.path.append('../..')
import inkmanip.inkmanip as ink
import importlib
importlib.reload(ink)


presentation = ink.inkscapeFile('presentation_A.svg')  # import .svg
# presentation.filepath
# presentation.filename
# presentation.prefix
# presentation.endOfFile
# presentation.layers
presentation.getLayersLabel()
presentation._getLayersId()


# %% export one layer ==========================================================
presentation = ink.inkscapeFile('presentation_A.svg')
presentation.exportLayer(labelList=['Title', 'Title flourishing'], filepath='./exported')

# %% export many layers from one file ======================================
presentation = ink.inkscapeFile('presentation_A.svg')
output_folder = 'layers_0'
labelLists = [['Title', 'Title flourishing'],
              ['Slide 2'],
              ['Important slide'],
              ['The end']
             ]

for idx, labelList in enumerate(labelLists):
    filepath = Path(f'{output_folder}/exported_{idx}.svg')
    presentation.exportLayer(labelList=labelList, filepath=filepath)

# %% export many layers from many files =====================================
output_folder = 'layers_1'

presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['Title', 'Title flourishing'],
              ['Slide 2'],
              ['Important slide'],
             ]
idx = 0
for labelList in labelLists:
    filepath = Path(f'{output_folder}/exported_{idx}.svg')
    presentation.exportLayer(labelList=labelList, filepath=filepath)
    idx +=1

presentation = ink.inkscapeFile('presentation_B.svg')
labelLists = [['Slide 1'],
              ['Slide 2'],
             ]
for idx2, labelList in enumerate(labelLists):
    filepath = Path(f'{output_folder}/exported_{idx}.svg')
    presentation.exportLayer(labelList=labelList, filepath=filepath)
    idx +=1

presentation = ink.inkscapeFile('presentation_A.svg')
labelLists = [['The end'],
             ]
for idx3, labelList in enumerate(labelLists):
    filepath = Path(f'{output_folder}/exported_{idx}.svg')
    presentation.exportLayer(labelList=labelList, filepath=filepath)
    idx +=1



# %% export many layers from many files using instructions file ================
filepath = 'layer2slide.txt'
output_folder = 'layers_2'


f = Path(filepath).open()
text = f.read()
f.close()

labelLists = []
for line in text.splitlines():
    if line.startswith('#') or line=='':
        pass
    else:
        labelLists.append([label.strip() for label in line.split(',')])

idx = 0
for labelList in labelLists:
    if labelList[0].startswith('file:'):
        presentation = ink.inkscapeFile(labelList[0].split('file:')[-1])
    else:
        filepath = Path(f'{output_folder}/exported_{idx}.svg')
        presentation.exportLayer(labelList=labelList, filepath=filepath)
        idx +=1


# %% export many layers from many files using instructions file with master files ================
filepath = 'layer2slide_master.txt'
output_folder = 'layers_3'


f = Path(filepath).open()
text = f.read()
f.close()

labelLists = []
for line in text.splitlines():
    if line.startswith('#') or line=='':
        pass
    else:
        labelLists.append([label.strip() for label in line.split(',')])

idx = 0
for labelList in labelLists:
    if labelList[0].startswith('file:'):
        presentation = ink.inkscapeFile(labelList[0].split('file:')[-1])
    elif labelList[0].startswith('master:'):
        master = ''
        for label in labelList[0].split('master:')[-1].split(','):
            if label == '':
                pass
            else:
                master += presentation.layers[label]+'\n'
    else:
        filepath = Path(f'{output_folder}/exported_{idx}.svg')
        presentation.layers['master'] = master
        # labelList.insert(0, 'master')
        labelList.append('master')
        presentation.exportLayer(labelList=labelList, filepath=filepath)
        idx +=1

# %% export many layers from many files using instructions file with master files and numbered slides ================


# %% adding external images to a presentation ================

# %% adding movement ================


# %% adding transitions ================


# %% exporting to pdf ================


# %% exporting to jpg ================


# %% exporting to svg ================
