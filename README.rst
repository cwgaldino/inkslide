
=========
inkslide
=========

Slide presentation from inkscape svg files using python. It was tested on ubuntu 20.04 with inkscape 1.0 and 0.9.3. However, it should work fine on windows and mac.

Depencies
==========

The svg parser script relies on

1. beautifulsoup4
2. lxml

They can be installed via pip::

    pip install beautifulsoup4
    pip install lxml

Additionaly, the scripts uses the inkscape internal pdf converter to convert svg files to pdf. In case it fails, it falls back to python libraries to do te conversion     

1. svglib
2. reportlab

They can be installed via pip::

    pip install svglib
    pip install reportlab

Therefore, these aren't really necessary at first. Only if you don't to use inkscape converter or if it fails.

Finally, the slide construction needs a pdf merger ``PdfFileMerger`` that can also be installed via pip::

    pip install PyPDF2


Installation
=============

There are two ways to use (install) this python module.

1) You can download (clone) the repository and use it as a python module (see examples folder).

2) You can put the file ``inkslide.py`` in your ``$HOME/bin`` folder and use it as a command.

    Usage: inkslide [OPTION] FILE
    
    Create slide from inkscape file.

    -h, --help    display this help and exit
    
    -i,           use instructions file as input


Usage
======

You can use it by first creating a instruction file and then building the slide presentation from it or builtin the instructions directly into the inkscape file.

1) Example 1 shows how to create presentation from the a instructions file, where you can see how to write the instructions file.

2) Example 2 shows how instructions can be built in into the inkscape file. A instructions file is created automatically and can be edited afterwards.

Instructions file
===================

A instructions file is a simple txt file where each line can be a command or a list of layers separated by comma ``,`` that will form a slide. Possible special tags, commands, and instructions are:

#. ``#  <comments>``
    Lines starting with ``#`` are ignored.
#. ``save at: <path-to-save-slide>``
    filepath to save slide. If more than one is provided, the last one is used. If not provided, slides will be saved at current directory as slides.pdf.
#. ``file: <path-to-svg-file>``
    Filepath of svg file of subsequent layers.
#. ``converter: <converter>``
    method for converting svg file to pdf.
    
        #. ``inkscape1.0``
            Uses inkscape 1.0 internal pdf converter.
        #. ``inkscape0.9``
            Uses inkscape 0.9.x internal pdf converter.
        # ``svglib``
            Uses python package ``svglib`` (use ``pip install svglib``). If None, it will try to use inkscape internal converter from the same inkscape version in the file.
#. ``bkg: <layer-to-be-used-as-background>``
    Layer to put underneath subsequent slides. This bkg is used until another bkg is assigned.
#. ``over:  <layer-to-be-used-as-overlay>``
    Layer to put over subsequent slides
#. ``slide number: <True, False, all>``
    It replaces the text::
    
        ##.slidenumber
        
    by the slide number. There are thre different slide numbering modes:
    
        #. ``All`` or ``all``
            All layers are counted as different slides.
        #. ``True`` or ``true``
            Layers marked with ``*`` or ``!`` do not count as a new slide.
        #. ``False`` or ``false``
            No slide numbering.
#. ``*`` or ``!``
    use ``*`` or ``!`` in front of any label to do not count that line as a slide


Embedded instructions
=======================

Instructions can be embedded directly into the inkscape file. In this case, a instruction file will be generated automatically. The possible settings are (these must be written in the inkscape file as text --- see example 3):

#. ``inkslide.save at: <path-to-save-slide>``
    filepath to save slide. If more than one is provided, the last one is used. If not provided, slides will be saved at current directory as slides.pdf.
#. ``converter: <converter>``
    method for converting svg file to pdf.
    
        #. ``inkscape1.0``
            Uses inkscape 1.0 internal pdf converter.
        #. ``inkscape0.9``
            Uses inkscape 0.9.x internal pdf converter.
        # ``svglib``
            Uses python package ``svglib`` (use ``pip install svglib``). If None, it will try to use inkscape internal converter from the same inkscape version in the file.
#. ``inkslide.slide number: <True, False, all>``
    It replaces the text::
    
        ##.slidenumber
        
    by the slide number. There are thre different slide numbering modes:
    
        #. ``All`` or ``all``
            All layers are counted as different slides.
        #. ``True`` or ``true``
            Layers marked with ``*`` or ``!`` do not count as a new slide.
        #. ``False`` or ``false``
            No slide numbering.

Each layer can have a personal instruction that must be written at the begging of the layer label. The layer instructions are:

#. ``#``
    Hide layer (layer does not became a slide)
#. ``@`` or ``b:``
    Layer is used as a background for subsequent layers until another background layer is set.
#. ``$`` or ``o:``
    Layer is used as a overlayer for subsequent layers until another overlayer layer is set.
#. ``*``
    Previous layer (or layer sequence) is added as background to the current layer to form one slide.
#. ``-``
    Last slide but the last layer is copied and used is as background to the current layer to form one slide. Multiple layers can be deleted by using multiple ``-``.
#. ``+``
    Add current layer to the previous one (merging layers).
#. ``=<layer>, <layer2>, <layer3>``
    Copy layer. Current layer is disregarded and <layer> is copied (use =, ==, ===, ... to avoid having two layers with the same name). Note that, ``=`` can copy layers that are hidden (``#``).
#. ``goto:<path-to-another-inkscape-file>``
    Defines the filepath of inkscape file of subsequent layers. Presentation can be split in multiple files.




