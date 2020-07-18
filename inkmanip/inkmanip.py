#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of tools to manipulate inkscape files."""

import sys
import os
from pathlib import Path
import copy
import tempfile
from collections import OrderedDict


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

        # open file
        f = self.filepath.open()

        parts = f.read().split('<g')  # separate groups
        self.prefix = parts[0]  # text that initialize .svg file

        if len(parts[-1].split('</g>\n'))==1:
            self.endOfFile = parts[-1].split('/>\n')[-1]    # text that ends .svg file
            parts[-1] = '/>\n'.join(parts[-1].split('/>\n')[:-1]) + '/>\n'
        else:
            self.endOfFile = parts[-1].split('</g>\n')[-1]    # text that ends .svg file
            parts[-1] = '</g>\n'.join(parts[-1].split('</g>\n')[:-1]) + '</g>\n'

        self.layers = OrderedDict()  # dict.key() is the layer id, dict.value() is the layer itself

        # split layers
        for part in parts[1:]:
            if self._getLayerLabel(part):
                self.layers[self._getLayerLabel(part)] = '<g' + part
                last_layer = self._getLayerLabel(part)
            else:
                self.layers[last_layer] += '<g' + part


    def getLabels(self):
        """Return a list of inkscape labels."""
        return list(self.layers.keys())


    def _turnOnVisibility(self, string):
        """Turn svg object visibility on.

        Search for substring like: 'style="display:none"' and remove it.

        If string has more than one object, first object with visibility off is turned on.

        Args:
            string (string): svg text
        """
        lines = string.splitlines()
        for idx, line in enumerate(lines):
            if 'display:none' in line and 'style' in line:
                lines[idx] = line.replace('display:none', '')
                return '\n'.join(lines)
        return '\n'.join(lines)


    def _getLayerLabel(self, string):
        """Search for substring like: inkscape:label="Layer 5". First Label found is returned.

        Args:
            string (string): svg text

        Returns:
            string with layer label or 0 if label was not found.
        """

        lines = string.splitlines()
        try:
            return [line for line in lines if line.strip().startswith('inkscape:label=\"')][0].split('\"')[-2]
        except: return 0


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


    def _svg2pdf(self, filepath, output_filepath=None):
        """Converts .svg files to .pdf

            Note:
                This function uses ikscape builtin pdf exporter.

            Args:
                filepath (string or Path object): .svg filepath
                output_filepath (string or Path object): output directory.  If
                    None, same directory of filepath is used.
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
        os.system('inkscape {0} --export-area-page --export-pdf {1}'.format(str(Path(filepath)), str(output_filepath)))


    def exportLayerSet2Pdf(self, labelList, filepath=Path.cwd()/'exported'):
        """Export a set of layers to a svg file.

        Args:
            labelList (list): list of labels
            filepath (string or Path object, optional)): output filepath
        """

        output = copy.copy(self.prefix)

        for label in labelList:
            output += self._turnOnVisibility(self.layers[label])
        output += self.endOfFile

        try:
            temp = tempfile.NamedTemporaryFile(suffix='.svg')
            temp.write(output.encode())
            temp.seek(0)

            self._svg2pdf(filepath=temp.name, output_filepath=filepath)
        finally:
            temp.close()
