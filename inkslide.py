#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create pdf presentations from inkscape (works with inkscape 1.0 and 0.92.4)."""

# standard imports
import sys
import os
import shutil
import copy
import warnings
import tempfile
from pathlib import Path
from collections import OrderedDict

# additional imports
from PyPDF2 import PdfFileMerger
from bs4 import BeautifulSoup, Comment

# svg-> pdf converter
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
except:
    pass



class parser(object):
    """Reads inkscape file.

    Args:
        filePath (str): directory path to .svg file

    Attributes:
        filepath (Pathlib object): svg filepath
        filename (str): svg filename
        inkscape_version (str): inkscape version used in the file
        prefix (str): text that initialize .svg file
        endOfFile (str): text that ends .svg file
        layers (dict): dict.key() is the layer label, dict.value() is the layer itself

    Methods:
        get_labels(): Return a list of inkscape labels
        exportLayerSet(): export layers
        exportLayerSet2Pdf(): export layers in pdf format
    """
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filename = self.filepath.name

        self._parse_layers()


    def _parse_layers(self):
        # open file
        f = self.filepath.open()
        soup = BeautifulSoup(f, features = 'xml')
        f.close()

        # layers
        script_tags = soup.find_all('g')
        self.layers = OrderedDict()  # dict.key() is the layer label, dict.value() is the layer itself
        for i in range(len(script_tags)):
            if 'inkscape:label' in script_tags[i].attrs and 'inkscape:groupmode' in script_tags[i].attrs:
                if script_tags[i].attrs['inkscape:groupmode'] == 'layer':
                    del_list = []
                    for j in range(len(script_tags[i].contents)):
                        try:
                            if 'inkscape:groupmode' in script_tags[i].contents[j].attrs:
                                if script_tags[i].attrs['inkscape:groupmode'] == 'layer':
                                    del_list.append(j)
                        except AttributeError:
                            pass
                    del_list = [x-n for n,x in enumerate(del_list)]
                    for j in del_list:
                        del script_tags[i].contents[j]

                    # turn visibility on
                    if 'style' in script_tags[i].attrs:
                        script_tags[i].attrs['style'] = script_tags[i].attrs['style'].replace("display:none", "display:inline")

                    # save slide
                    self.layers[script_tags[i].attrs['inkscape:label']] = str(script_tags[i])#.prettify()

        # prefix
        script_tags = soup.find_all('svg')
        self.prefix = script_tags[0].parent.prettify().replace(script_tags[0].prettify(), '')
        self.prefix += script_tags[0].prettify().split('<g')[0]

        # inkscape version
        if 'inkscape:version' in script_tags[0].attrs:
            self.inkscape_version = script_tags[0].attrs['inkscape:version']
        else:
            self.inkscape_version = None

        # end of file
        self.endOfFile = script_tags[0].prettify().split('</g>')[-1]


    def get_labels(self):
        """Return a list of inkscape labels."""
        return list(self.layers.keys())


    def export_layers(self, labels, output_filepath=None):
        """Export a set of layers to a svg file.

        Args:
            labels (list): list of layer labels
            output_filepath (string or Path object, optional)): output filepath. If,
                None, the svg file will be saved at the current work directory as
                export.svg.

        See Also:
            :py:func:`export_layers_pdf`
        """

        output = copy.copy(self.prefix)

        for label in labels:
            output += self._visibility_on(self.layers[label])
        output += self.endOfFile

        if output_filepath is None:
            output_filepath = Path.cwd()/'exported.svg'
        else:
            output_filepath = Path(output_filepath).with_suffix('.svg')

        # save
        f = Path(output_filepath).open('w')
        f.write(output)
        f.close()


    def _pdf(self, filepath, output_filepath=None, converter=None):
        """Export inkscape file to .pdf

            Args:
                filepath (string or Path object): .svg filepath
                output_filepath (string or Path object): output filepath.  If
                    None, same directory and filename is used.
                converter (string, optional): method for converting svg file to pdf.
                    #. `inkscape1.0`
                        Uses inkscape 1.0 internal pdf converter.
                    #. `inkscape0.9`
                        Uses inkscape 0.9.x internal pdf converter.
                    # `svglib`
                        Uses python package `svglib` (use `pip install svglib`).
                    If None, it will try to use inkscape internal converter from
                    the same inkscape version in the file.
        """
        filepath = Path(filepath)

        if output_filepath is None:
            output_filepath = filepath.with_suffix('.pdf')
        else:
            output_filepath = Path(output_filepath).with_suffix('.pdf')

        # create .pdf
        if converter is None or converter == 'None':
            if self.inkscape_version.startswith("1"):
                converter = 'inkscape1.0'
            else:
                converter = 'inkscape0.9'

        if converter == 'inkscape1.0':
            os.system('inkscape --export-type=pdf {0} -o {1}'.format(str(Path(filepath)), str(output_filepath)))
        elif converter == 'inkscape0.9':
            os.system('inkscape {0} --export-area-page --export-pdf {1}'.format(str(Path(filepath)), str(output_filepath)))
        elif converter == 'svglib':
            drawing = svg2rlg(str(Path(filepath)))
            renderPDF.drawToFile(drawing, str(output_filepath))
        else:
            warnings.warn('converter not found. Trying to use inkscape 1.0 internal pdf export.')
            try:
                os.system('inkscape --export-type=pdf {0} -o {1}'.format(str(Path(filepath)), str(output_filepath)))
            except:
                try:
                    warnings.warn('converter not found. Trying to use inkscape 0.9 internal pdf export.')
                    os.system('inkscape {0} --export-area-page --export-pdf {1}'.format(str(Path(filepath)), str(output_filepath)))
                except:
                    try:
                        warnings.warn('converter not found. Trying to use python svglib package for  pdf export.')
                        drawing = svg2rlg(str(Path(filepath)))
                        renderPDF.drawToFile(drawing, str(output_filepath))
                    except:
                        warnings.warn('Cannot export to pdf. Try installing svglib and reportlab python packages.')


    def export_layers_pdf(self, labels, output_filepath=None, converter=None):#, keep_svg=False):
        """Export a set of layers to a svg file.

        Args:
            labels (list): list of labels
            output_filepath (string or Path object, optional)): output filepath. If,
                None, the pdf file will be saved at the current work directory as
                export.pdf.
            converter (string, optional): method for converting svg file to pdf.
                #. `inkscape1.0`
                    Uses inkscape 1.0 internal pdf converter.
                #. `inkscape0.9`
                    Uses inkscape 0.9.x internal pdf converter.
                # `svglib`
                    Uses python package `svglib` (use `pip install svglib`).
                If None, it will try to use inkscape internal converter from
                the same inkscape version in the file.

        See Also:
            :py:func:`export_layers`
        """
        output = copy.copy(self.prefix)

        if output_filepath is None:
            output_filepath = Path.cwd()/'exported.pdf'

        for label in labels:
            output += self._visibility_on(self.layers[label])
        output += self.endOfFile

        try:
            temp = tempfile.NamedTemporaryFile(suffix='.svg')
            temp.write(output.encode())
            temp.seek(0)

            self._pdf(filepath=temp.name, output_filepath=output_filepath, converter=converter)
        finally:
            # if keep_svg:
            #     shutil.copytree(temp.name, str(filepath)+'.svg')
            temp.close()


    def _visibility_on(self, string):
        """Turn svg object visibility on.

        Search for the first substring like: 'style="display:none"' and remove it.

        Args:
            string (string): svg text
        """
        lines = string.splitlines()
        for idx, line in enumerate(lines):
            if 'display:none' in line and 'style' in line:
                lines[idx] = line.replace('display:none', '')
                return '\n'.join(lines)
        return '\n'.join(lines)


def inkslide(filepath):
    """Create slides from instructions file.

    Args:
        filepath (str): filepath to instructions file

    A instructions file is a simple txt file where each line can be a command or
        a list of layers separated by comma `,` that will form a slide.

    The commands are:

    #. `#  <comments>`
        Lines starting with `#` are ignored.
    #. `save at: <path-to-save-slide>`
        filepath to save slide. If more than one is provided, the last one is used.
        If not provided, slides will be saved at current directory as slides.pdf.
    #. `file: <path-to-svg-file>`
        Filepath of svg file of subsequent layers.
    #. `converter: <converter>`
        method for converting svg file to pdf.
            #. `inkscape1.0`
                Uses inkscape 1.0 internal pdf converter.
            #. `inkscape0.9`
                Uses inkscape 0.9.x internal pdf converter.
            # `svglib`
                Uses python package `svglib` (use `pip install svglib`).
            If None, it will try to use inkscape internal converter from
            the same inkscape version in the file.
    #. `bkg: <layer-to-be-used-as-background>`
        Layer to put underneath subsequent slides. This bkg is used until another
        bkg is assigned.
    #. `over:  <layer-to-be-used-as-overlay>`
        Layer to put over subsequent slides
    #. `slide number: <True, False, all>`
        It replaces the text::
            ##.slidenumber
        by the slide number. There are thre different slide numbering modes:
            #. `All` or `all`
                All layers are counted as different slides.
            #. `True` or `true`
                Layers marked with `*` or `!` do not count as a new slide.
            #. `False` or `false`
                No slide numbering.
    #. `*` or `!`
        use `*` or ``!`` in front of any label to do not count that line as a slide

    """
    f = Path(filepath).open()
    text = f.read()
    f.close()

    #default settings
    show_slide_number = 'False'
    converter = None
    output_filepath = Path.cwd()/'slides.pdf'
    # remove comments, define output_filepath, get converter, get slide number mode, get lines
    lines = []
    for line in text.splitlines():
        if line.startswith('#') or line=='':
            pass
        elif line.startswith('save at:'):
            output_filepath = Path(line.split('save at:')[-1].strip()).with_suffix('.pdf')
        elif line.startswith('converter:'):
            converter = line.split('converter:')[-1].strip()
        elif line.startswith('slide number:'):
            show_slide_number = line.split('slide number:')[-1].strip()
        else:
            lines.append([label.strip() for label in line.split(',')])

    print('Generating slides.......')
    print(f'Instruction file: {filepath}')
    print(f'saving slides at: {output_filepath}')
    print(f'svg->pdf converter: {converter}')
    print(f'Slide number mode: {show_slide_number}')
    print(f'slides:')

    try:
        f = tempfile.TemporaryDirectory()
        pdfs2merge = []
        idx = 0
        slide_number = 0


        bkg = ''
        over = ''

        # interpret line
        for line in lines:
            if line[0].startswith('file:'):
                ink = parser(line[0].split('file:')[-1].strip())
            elif line[0].startswith('bkg:'):
                bkg = ''
                labels = line[0].split('bkg:')[-1].split(',')
                for label in labels:
                    if label == '':
                        pass
                    else:
                        bkg += ink.layers[label]+'\n'
            elif line[0].startswith('over:'):
                over = ''
                labels = line[0].split('over:')[-1].split(',')
                for label in labels:
                    if label == '':
                        pass
                    else:
                        over += ink.layers[label]+'\n'
            else:
                # add bkg and overlayer to the inkscape object
                ink.layers['bkg'] = bkg
                line.insert(0, 'bkg')
                ink.layers['over'] = over
                line.append('over')

                # Change slide number
                if show_slide_number == 'True' or show_slide_number == 'true':
                    if not any(label.startswith('!') for label in line) and not any(label.startswith('*') for label in line):
                        slide_number += 1
                        # if label.startswith('!'):
                        #     if any(s.startswith('!') for s in line_old) or any(s.startswith('*') for s in line_old):
                        #         changeSlideNumber = False
                elif show_slide_number == 'all' or show_slide_number == 'All':
                    slide_number += 1
                else:  # elif show_slide_number == 'False' or show_slide_number == 'false':
                    pass

                # add slide number to slide
                if show_slide_number != 'False' and show_slide_number != 'false':
                    for label in line:
                        ink.layers[label] = ink.layers[label].replace('##.slidenumber', str(slide_number))
                    line_old = copy.copy(line)

                print(f'{idx}: '+ ', '.join(line))
                filepath = Path(f'{f.name}/exported_{idx}.pdf')
                pdfs2merge.append(filepath)
                ink.export_layers_pdf(labels=line, output_filepath=filepath, converter=converter)
                idx +=1

        _merger(filelist=pdfs2merge, output_filepath=output_filepath)

    finally:
        print('Done.')
        f.cleanup()


def create_instructions(filepath):
    """Create instructions file.

    The instructions file is saved with the same filepath as the inkscape file, but
    with extension .inst.

    Settings must be written directly in the inkscape file as text. The possible settings are:

    #. inkslide.save at: <path-to-save-slide>
        filepath to save slide. If more than one is provided, the last one is used.
        If not provided, slides will be saved at current directory as slides.pdf.
    #. `inkslide.converter: <converter>`
        method for converting svg file to pdf.
            #. `inkscape1.0`
                Uses inkscape 1.0 internal pdf converter.
            #. `inkscape0.9`
                Uses inkscape 0.9.x internal pdf converter.
            # `svglib`
                Uses python package `svglib` (use `pip install svglib`).
            If None, it will try to use inkscape internal converter from
            the same inkscape version in the file.
    #. `inkslide.slide number: <True, False, all>`
        It replaces the text::
            ##.slidenumber
        by the slide number. There are thre different slide numbering modes:
            #. `All` or `all`
                All layers are counted as different slides.
            #. `True` or `true`
                Layers marked with `*` or `!` do not count as a new slide.
            #. `False` or `false`
                No slide numbering.

    Each layer can have a personal instruction that must be written at the layer name.
    The layer instructions are:

    #. `#`
        Hide layer (layer does not became a slide)
    #. `@` or `b:`
        Layer is used as a background for subsequent layers until another background layer is set.
    #. `$` or `o:`
        Layer is used as a overlayer for subsequent layers until another overlayer layer is set.
    #. `*`
        Previous layer (or layer sequence) is added as background to the current layer to form one slide.
    #. `-`
        Last slide but the last layer is copied and used is as background to the current layer to form one slide.
        Multiple layers can be deleted by using multiple `-`.
    #. `+`
        Add current layer to the previous one (merging layers).
    #. `=<layer>, <layer2>, <layer3>`
        Copy layer. Current layer is disregarded and <layer> is copied
        (use =, ==, ===, ... to avoid having two layers with the same name). Note that,
        `=` can copy layers that are hidden (`#`).
    #. `goto:<path-to-another-inkscape-file>`
        Defines the filepath of inkscape file of subsequent layers. Presentation
        can be split in multiple files.

    Returns:
        filepath (string) of saved instructions file.
    """
    f = Path(filepath).open()
    text = f.read()
    f.close()

    #default settings
    show_slide_number = 'False'
    converter = None
    output_filepath = Path.cwd()/'slides.pdf'
    # remove comments, define output_filepath, get converter, get slide number mode, get lines
    lines = []
    for line in text.splitlines():
        if 'inkslide.save at:' in line:
            output_filepath = Path(line.split('save at:')[-1].split('<')[0]).with_suffix('.pdf')
        if 'inkslide.converter:' in line:
            converter = line.split('converter:')[-1].split('<')[0].strip()
        if 'inkslide.slide number:' in line:
            show_slide_number = line.split('slide number:')[-1].split('<')[0].strip()

    try:
        def read_layers(filepath):
            """Recursively find all layers and read all instructions."""
            ink = parser(filepath)

            text = ''
            text += '\n\nfile:' + str(filepath)
            for label in ink.get_labels():
                if label.strip().startswith('*'):
                    text += '\n' + text.splitlines()[-1] + ', ' + label
                elif label.strip().startswith('-'):
                    text += '\n' + ', '.join(text.splitlines()[-1].split(',')[:-label.count('-')]) + ', ' + label
                elif label.strip().startswith('='):
                    text += '\n' + label.split('=')[-1]
                elif label.strip().startswith('@') or label.strip().startswith('b:'):
                    text += '\nbkg:' + label
                elif label.strip().startswith('$') or label.strip().startswith('o:'):
                    text += '\nover:' + label
                elif label.strip().startswith('+'):
                    text += ', ' + label
                elif label.strip().startswith('goto:'):
                    nextfile = Path(label.split('goto:')[-1])
                    text += read_layers(nextfile)
                    text += '\n\nfile:' + str(filepath)
                else:
                    text += '\n' + label

            return text

        text = read_layers(filepath)
        text += f'\nsave at: {output_filepath}'
        text += f'\nconverter: {converter}'
        text += f'\nslide number: {show_slide_number}'

        f = Path(Path(filepath).with_suffix('.inst')).open('w+')
        f.write(text)
    finally:
        filepath = f.name
        f.close()
        return filepath


def _merger(filelist, output_filepath=Path.cwd()/'merged.pdf'):
    """Merge pdf files.

        Args:
            filelist (list): list of string (or pathlib.Path object) of pdf files to merge (in order)
            output_filepath (string or Path object): filepath for merged pdf file
    """
    # create merger
    pdf_merger = PdfFileMerger()

    # append to merger
    for pdf in filelist:
        pdf_merger.append(str(Path(pdf)))

    # check .pdf extension
    output_filepath = Path(output_filepath).with_suffix('.pdf')

    #save file
    pdf_merger.write(str(output_filepath))


if __name__ == '__main__':

    instructions = 'Usage: inkslide [OPTION] FILE\n'
    instructions += 'Create slide from inkscape file.'
    instructions += '\n\n'
    instructions += '-h, --help    display this help and exit\n'
    instructions += '-i,           use instructions file as input\n'

    if len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(instructions)
        else:
            inkslide(filepath=create_instructions(sys.argv[1]))
    elif len(sys.argv) > 2:
        if sys.argv[1] == '-i':
            inkslide(filepath=sys.argv[2])
        else:
            print(instructions)
    else:
        print(instructions)
