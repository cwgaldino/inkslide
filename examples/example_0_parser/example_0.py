#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example 0: inkscape file parser."""

from pathlib import Path
from inkslide import parser

# %% get information from file =================================================
ink = parser('presentation_A.svg')  # import .svg
print(ink.filepath)
print(ink.filename)
print(ink.prefix)
print(ink.endOfFile)
print(ink.layers)
ink.get_labels()

# %% export many layers in one file ============================================
ink = parser('presentation_A.svg')
ink.export_layers(labels=['Title', 'Title flourishing', 'Title flourishing2'], output_filepath='./test_0/exported')

# %% export many layers in many files ==========================================
ink = parser('presentation_A.svg')
labels = [['Title', 'Title flourishing', 'Title flourishing2'],
          ['Slide 2'],
          ['Slide 3'],
          ['Important slide'],
          ['The end']
         ]

for idx, l in enumerate(labels):
    output_filepath = Path(f'test_1/exported_{idx}.svg')
    ink.export_layers(labels=l, output_filepath=filepath)


# %% export many layers to many pdf files ======================================
ink = parser('presentation_A.svg')
labels = [['Title', 'Title flourishing', 'Title flourishing2'],
          ['Slide 2'],
          ['Slide 3'],
          ['Important slide'],
          ['The end']
         ]

for idx, l in enumerate(labels):
    filepath = Path(f'test_3/exported_{idx}')
    # ink.export_layers_pdf(labels=labelList, output_filepath=filepath, converter='inkscape0.9')
    ink.export_layers_pdf(labels=labelList, output_filepath=filepath, converter='inkscape1.0')
    # ink.export_layers_pdf(labels=labelList, output_filepath=filepath, converter='svglib')
