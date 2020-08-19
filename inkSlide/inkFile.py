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


class inkscapeFile(object):
    """ Reads inkscape file.

    Args:
        filePath (str): directory path to .svg file

    Attributes:
        filepath (Pathlib object): svg filepath
        filename (str): svg filename
        prefix (str): text that initialize .svg file
        endOfFile (str): text that ends .svg file
        layers (dict): dict.key() is the layer label, dict.value() is the layer itself

    Methods:
        getLabels(): Return a list of inkscape labels
        exportLayerSet(): export layers
        exportLayerSet2Pdf(): export layers in pdf format
    """
    def __init__(self, filePath):
        self.filepath = Path(filePath)
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

        # end of file
        self.endOfFile = '\n</svg>'


    def getLabels(self):
        """Return a list of inkscape labels."""
        return list(self.layers.keys())


    def exportLayerSet(self, labelList, filepath=Path.cwd()/'exported'):
        """Export a set of layers to a svg file.

        Args:
            labelList (list): list of layer labels
            filepath (string or Path object, optional)): output filepath
        """

        output = copy.copy(self.prefix)

        for label in labelList:
            output += self._turnOnVisibility(self.layers[label])
        output += self.endOfFile

        if Path(filepath).match('*.svg'):  # Check extension
            pass
        else:
            filepath = str(filepath) + '.svg'

        # save
        f = Path(filepath).open('w')
        f.write(output)
        f.close()


    def _pdf(self, filepath, output_filepath=None, converter='inkscape1'):
        """Export inkscape file to .pdf

            Note:
                This function uses inkscape builtin pdf exporter.

            Args:
                filepath (string or Path object): .svg filepath
                output_filepath (string or Path object): output directory.  If
                    None, same directory of filepath is used.
                converter (string, optional): method for converting svg file to pdf.
                    Possible options are: `inkscape1` or `inkscape0.9`, to use the internal
                    inkscape svg to pdf exporter; or `svglib` to use python package svglib
                    (use `pip install svglib` if svg lib is not installed).
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
        if converter == 'inkscape1':
            os.system('inkscape --export-type=pdf {0} -o {1}'.format(str(Path(filepath)), str(output_filepath)))
        elif converter == 'inkscape0.9':
            os.system('inkscape {0} --export-area-page --export-pdf {1}'.format(str(Path(filepath)), str(output_filepath)))
        elif converter == 'svglib':
            drawing = svg2rlg(str(Path(filepath)))
            renderPDF.drawToFile(drawing, str(output_filepath))


    def exportLayerSet2Pdf(self, labelList, filepath=Path.cwd()/'exported', converter='inkscape1'):#, keep_svg=False):
        """Export a set of layers to a svg file.

        Args:
            labelList (list): list of labels
            filepath (string or Path object, optional)): output filepath
            converter (string, optional): method for converting svg file to pdf.
                Possible options are: `inkscape1` or `inkscape0.9`, to use the internal
                inkscape svg to pdf exporter; or `svglib` to use python package svglib
                (use `pip install svglib` if svg lib is not installed).
        """

        output = copy.copy(self.prefix)

        for label in labelList:
            output += self._turnOnVisibility(self.layers[label])
        output += self.endOfFile

        try:
            temp = tempfile.NamedTemporaryFile(suffix='.svg')
            temp.write(output.encode())
            temp.seek(0)

            self._pdf(filepath=temp.name, output_filepath=filepath, converter=converter)
        finally:
            # if keep_svg:
            #     shutil.copytree(temp.name, str(filepath)+'.svg')
            temp.close()




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
    # def _turnOnVisibility(self, string):
    #     """Turn svg object visibility on.
    #
    #     Search for substring like: 'style="display:none"' and remove it.
    #
    #     If string has more than one object, first object with visibility off is turned on.
    #
    #     Args:
    #         string (string): svg text
    #     """
    #     lines = string.splitlines()
    #     for idx, line in enumerate(lines):
    #         if 'display:none' in line and 'style' in line:
    #             lines[idx] = line.replace('display:none', '')
    #             return '\n'.join(lines)
    #     return '\n'.join(lines)
