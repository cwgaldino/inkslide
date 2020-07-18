import sys
import os
from pathlib import Path
from PyPDF2 import PdfFileMerger


class inkscapeFile(object):
    '''
    reads inkscape file and create a class

    Args:
        filePath (str): directory path to .svg file

    Attributes:
        prefix (str): text that initialize .svg file
        endOfFile (str): text that ends .svg file
        layers (dict): dict.key() is the layer id, dict.value() is the layer itself
        label2id (dict): dict to convert between inkscape label and layer id

    Methods:
        getLayersId(): Return a list with layers id's
        getInkLabels(): Return a list with inkscape labels
    '''
    def __init__(self, filePath):
        self.filepath = Path(filePath)
        self.filename = self.filepath.name

        try:
            f = self.filepath.open()
        except:
            print('FILE NOT FOUND!')
            return

        parts = f.read().split('<g')  # separete file in the layers
        self.prefix = parts[0]  # text that initialize .svg file
        self.endOfFile = parts[-1].split('</g>\n')[1]    # text that ends .svg file
        parts[-1] = parts[-1].split('</g>\n')[0] + '</g>\n'
        self.layers = dict()  # dict.key() is the layer id, dict.value() is the layer itself
        self.label2id = dict()  # dict to convert between inkscape label and layer id

        for part in parts:
            if getLayerId(part):
                part = '<g\n' + part
                part = layerTurnOnVisibility(part)
                print(part)
                print('=====================================================')
                self.layers[getLayerId(part)] = part
                self.label2id[getInkscapeLabel(part)] = getLayerId(part)


    def getLayersId(self):
        '''
        Return a list with layers id's
        '''
        return list(self.layers.keys())

    def getInkLabels(self):
        '''
        Return a list with inkscape labels
        '''
        return list(self.label2id.keys())

def getLayerId(string):
    '''
    It looks for the substring id="layer1". First id found is returned.

    :param string: (string) svg chunk of text
    :return: layer id as a string (return 0 if id not found)
    '''

    lines = string.split('\n')
    try:
        return [line for line in lines if line.startswith('     id=\"layer')][0].split('\"')[-2]
    except: return 0

def getInkscapeLabel(string):
    '''
    It looks for the Inkscape Label of a layer, eg, inkscape:label="Layer 5".
    First Label found is returned.

    :param string: (string) svg chunk of text
    :return: layer id as a string (return 0 if id not found)
    '''

    lines = string.split('\n')
    try:
        return [line for line in lines if line.startswith('     inkscape:label=\"')][0].split('\"')[-2]
    except: return 0


def layerTurnOnVisibility(string):
    '''
        Turn on layers visibility. First layer with visibility off is turned on.

        :param string: (string) svg chunk of text
    '''
    lines = string.split('\n')
    if '     style="display:none">' in lines:
        idx = lines.index('     style="display:none">')
        lines[idx-1] = lines[idx-1]+'>'
        lines.remove('     style="display:none">')
    elif '     style="display:none"' in lines:
        lines.remove('     style="display:none"')
    return '\n'.join(lines)


def exportInkscape_svg(inkscapeFile_object, out_directory=Path.cwd(), out_filename='exported', layerList='all'):
    '''
        extract layers from inkscape .svg and save in another .svg file

        :param inkscapeFile_object: inkscapeFile object
        :param out_directory: (string or Path object) output directory
        :param out_filename: (string) new .svg filename
        :param layerList: list of inkscape layer labels as strings
    '''

    # create .sgv
    inkscape_out = inkscapeFile_object.prefix

    if layerList=='all':
        layerList = inkscapeFile_object.getInkLabels()

    for layerLabel in layerList:
        inkscape_out += inkscapeFile_object.layers[inkscapeFile_object.label2id[layerLabel]]
    inkscape_out += inkscapeFile_object.endOfFile

    if not (out_directory/out_filename).match('*.svg'):  # Check extension
        out_filename += '.svg'

    # save
    f = open(out_directory/out_filename, 'w')
    f.write(inkscape_out)
    f.close()

    return 1


def svg2pdf(inkscape_filepath, out_directory=Path.cwd(), out_filename='converted.pdf'):
    '''
        Converts inkscape .svg file in .pdf

        :param inkscape_filepath: (string or Path object) .svg file path
        :param out_directory: (string or Path object) output directory
        :param out_filename: string pdf filename
    '''
    out_directory = Path(out_directory)

    if not (out_directory/out_filename).match('*.pdf'):  # Check extension
        out_filename += '.pdf'

    # create .pdf
    os.system('inkscape {0} --export-area-page --export-pdf {1}'.format(str(Path(inkscape_filepath)), str(out_directory/out_filename)))

    return 1


def merger(pdf_path_list, out_directory=Path.cwd(), out_filename='merged.pdf'):
    '''
        Merge pdf's.

        :param pdf_path_list: list of (string or Path object) with all pdf's to merge (in order)
        :param out_directory: (string or Path object) output directory
        :param out_filename: string pdf filename
    '''
    # create merger
    pdf_merger = PdfFileMerger()

    # append to merger
    for pdf in pdf_path_list:
        pdf_merger.append(str(Path(pdf)))

    # check .pdf extension
    out_fullpath = Path(out_directory)/out_filename
    if not out_fullpath.match('*.pdf'):  # Check filename extension
        out_filename += '.svg'
    out_fullpath = Path(out_directory)/out_filename

    #save file
    # with open(out_directory, 'wb') as f:
    pdf_merger.write(str(out_fullpath))
