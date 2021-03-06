#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of tools to manipulate inkscape files."""

import sys
import os
from pathlib import Path
import copy
import tempfile
from collections import OrderedDict
from bs4 import BeautifulSoup, Comment

try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
except:
    pass
filepath = '/home/galdino/github/inkslide/examples/example_3/presentation_B.svg'
# from inkslide.parser import parser

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
            if 'inkscape:label' in script_tags[i].attrs:
                del_list = []
                for j in range(len(script_tags[i].contents)):
                    try:
                        if 'inkscape:label' in script_tags[i].contents[j].attrs:
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

        # Check extension
        if Path(output_filepath).match('*.svg'):
            pass
        else:
            output_filepath = str(output_filepath) + '.svg'

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
            if Path(filepath.name).match('*.svg'):
                name = ''.join(filepath.name.split('.svg')[:-1])
            output_filepath = Path(filepath.parent)/name

        if Path(output_filepath).match('*.pdf'):  # Check extension
            pass
        else:
            output_filepath = str(output_filepath) + '.pdf'

        # create .pdf
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


    def export_layers_pdf(self, labels, output_filepath=None, converter=None):#, keep_svg=False):
        """Export a set of layers to a svg file.

        Args:
            labels (list): list of labels
            output_filepath (string or Path object, optional)): output filepath
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


    #
    #
    # def _fix_group_tag(self):
    #     """Obsolete."""
    #     for label, layer in self.layers.items():
    #         n = layer.count('<g') - layer.count('</g>')
    #         if n>0:
    #             self.layers[label] += '</g>\n'*abs(n)
    #         elif n<0:
    #             self.layers[label] = '<g\n'*abs(n) + self.layers[label]
    #
    #
    # def _internal_parser(self):
    #     """Obsolete."""
    #     # open file
    #     f = self.filepath.open()
    #
    #     parts = f.read().split('<g')  # separate groups
    #     self.prefix = parts[0]  # text that initialize .svg file
    #
    #     if len(parts[-1].split('</g>\n'))==1:
    #         self.endOfFile = parts[-1].split('/>\n')[-1]    # text that ends .svg file
    #         parts[-1] = '/>\n'.join(parts[-1].split('/>\n')[:-1]) + '/>\n'
    #     else:
    #         self.endOfFile = parts[-1].split('</g>\n')[-1]    # text that ends .svg file
    #         parts[-1] = '</g>\n'.join(parts[-1].split('</g>\n')[:-1]) + '</g>\n'
    #
    #     self.layers = OrderedDict()  # dict.key() is the layer label, dict.value() is the layer itself
    #
    #     # split layers
    #     for part in parts[1:]:
    #         if self._getLayerLabel(part):
    #             label = self._getLayerLabel(part)
    #
    #             self.layers[label] = '<g' + part
    #             previous_layer = label
    #         else:
    #             self.layers[previous_layer] += '<g' + part
    #
    #
    # def _getLayerLabel(self, string):
    #     """Obsolete."""
    #     # """Search for substring like: inkscape:label="Layer 5". First Label found is returned.
    #     #
    #     # Args:
    #     #     string (string): svg text
    #     #
    #     # Returns:
    #     #     string with layer label or 0 if label was not found.
    #     # """
    #
    #     # lines = string.splitlines()
    #     lines = string.split(' ')
    #     try:
    #         return [line for line in lines if line.strip().startswith('inkscape:label=\"')][0].split('\"')[-2]
    #     except: return 0
    #
    #
