import os
os.system('title 1')
import sys
from pathlib import Path
import inkscape_utils as ink
from importlib import reload
ink = reload(ink)

# input=================================================
dirname = Path(r'.')
filename = 'presentation.svg'
svg_output_directory = dirname/'presentation_slides(svg)'
pdf_output_directory = dirname/'presentation_slides(pdf)'

master = ['Layer 1']  # list with layers that must appear in all slides

layers2slide = [['Layer 2']
               ,['Layer 3', 'Layer 4']
               ,['Layer 3', 'Layer 5']
               ]

# include master to layers2slide
for idx, item in enumerate(layers2slide):
    layers2slide[idx] = master + item

# =================================================
fullpath = dirname/filename
if not fullpath.match('*.svg'):  # Check filename extension
    filename += '.svg'
    fullpath = dirname/(filename)

presentation = ink.inkscapeFile(fullpath)  # import .svg

presentation.filepath
presentation.filename
presentation.prefix
presentation.endOfFile
presentation.layers
presentation.label2id

presentation.getInkLabels()
presentation.getLayersId()

for idx, list in enumerate(layers2slide):
    ink.exportInkscape_svg(presentation, out_directory=svg_output_directory, out_filename='exported_{0}'.format(idx), layerList=list)
    ink.svg2pdf(svg_output_directory/'exported_{0}.svg'.format(idx), out_directory=pdf_output_directory, out_filename='converted_{0}'.format(idx))

# Merge pdf's
pdf_path_list = list(pdf_output_directory.glob('*.pdf'))[::-1]
ink.merger(pdf_path_list, out_directory=dirname, out_filename='presentation.pdf')
