
=========
inkslide
=========

Slide presentation from Inkscape svg files using python. It was tested on Ubuntu 20.04 with Inkscape 1.0 and 0.9.3. However, it should work fine on windows and mac (let me know).

.. image:: https://github.com/cwgaldino/inkslide/blob/master/figs/fig_1.png?sanitize=true

Export presentation:

.. image:: https://github.com/cwgaldino/inkslide/blob/master/figs/fig_2.png?sanitize=true
  :width: 50px

.. image:: https://github.com/cwgaldino/inkslide/blob/master/figs/fig_3.png?sanitize=true

Please, report issues and enhancement ideas on GitHub. The script is in a early stage of development so every comment helps.

Dependencies
============

The svg parser script relies on

1. beautifulsoup4
2. lxml

They can be installed via pip::

    pip install beautifulsoup4
    pip install lxml

Additionally, the scripts uses the Inkscape internal pdf converter to convert svg files to pdf. In case it fails, it falls back to python libraries to do te conversion

1. svglib
2. reportlab

They can be installed via pip::

    pip install svglib
    pip install reportlab

Therefore, these aren't really necessary at first. Only if you don't to use Inkscape converter or if it fails.

Finally, the slide construction needs a pdf merger ``PdfFileMerger`` that can also be installed via pip::

    pip install PyPDF2


Installation and usage
======================

There two ways to use (install) this python module.

1) You can download (clone) the repository and use it as a python module (see python scripts in the tutorial folder).

or

2) You can download (clone) the repository and put the file ``inkslide.py`` in your ``$HOME/bin`` folder and use it as a command.

    Usage: inkslide.py [OPTION] FILE

    Create slide from Inkscape file.

    -h, --help    display this help and exit

    -i            use instructions file as input


Tutorials and examples
======================

Tutorial file 0 will give you examples how to use the svg file ``parser`` class, which is useful if you want to do your own tinkering with Inkscape svg files.

Tutorial files 1 and 2 will give examples on how to create presentations from Inkscape files by importing ``inkslide.py`` as a module. Note that one can generate a presentation from a instructions file or embedded the instructions directly into the Inkscape file. In the later, a instructions file will be generated automatically. In addition to that, one can also use ``inkslide.py`` as a command. For instance, presentations in the Examples folder were created by calling ``inkslide.py`` from the terminal.


Embedded instructions
=======================

Instructions can be embedded directly into the Inkscape file. In this case, a instruction file will be generated automatically. The possible settings are (these must be written in the Inkscape file as text --- see example 3):

#. ``inkslide.save at: <path-to-save-slide>``
    filepath to save slide. If more than one is provided, the last one is used. If not provided, slides will be saved at current directory as slides.pdf.
#. ``converter: <converter>``
    method for converting svg file to pdf.

        #. ``inkscape1.0``
            Uses Inkscape 1.0 internal pdf converter.
        #. ``inkscape0.9``
            Uses Inkscape 0.9.x internal pdf converter.
        #. ``svglib``
            Uses python package ``svglib`` (use ``pip install svglib``). If None, it will try to use Inkscape internal converter from the same Inkscape version in the file.
#. ``inkslide.slide number: <True, False, all>``
    It replaces the text::

        ##.slidenumber

    by the slide number. There are three different slide numbering modes:

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
    Defines the filepath of Inkscape file of subsequent layers. Presentation can be split in multiple files.


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
            Uses Inkscape 1.0 internal pdf converter.
        #. ``inkscape0.9``
            Uses Inkscape 0.9.x internal pdf converter.
        #. ``svglib``
            Uses python package ``svglib`` (use ``pip install svglib``). If None, it will try to use Inkscape internal converter from the same Inkscape version in the file.
#. ``bkg: <layer-to-be-used-as-background>``
    Layer to put underneath subsequent slides. This bkg is used until another bkg is assigned.
#. ``over:  <layer-to-be-used-as-overlay>``
    Layer to put over subsequent slides
#. ``slide number: <True, False, all>``
    It replaces the text::

        ##.slidenumber

    by the slide number. There are three different slide numbering modes:

        #. ``All`` or ``all``
            All layers are counted as different slides.
        #. ``True`` or ``true``
            Layers marked with ``*`` or ``!`` do not count as a new slide.
        #. ``False`` or ``false``
            No slide numbering.
#. ``*`` or ``!``
    use ``*`` or ``!`` in front of any label to do not count that line as a slide
