#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of tools to manipulate inkscape files."""

from pathlib import Path
from PyPDF2 import PdfFileMerger
import tempfile
import copy
import shutil

import inkSlide.inkFile as ink

# import sys
# sys.path.append('/home/galdino/github/inkmanip')
# sys.path.append(str(Path(r'C:\Users\carlo\Desktop\inkmanip')))
# import inkmanip.inkmanip as ink
# import importlib
# importlib.reload(ink)



def inkSlide(filepath, AddSlideNumber=False):#, keep_svg=False):
    """
    #           comments
    save at:    filepath of final pdf (if more than one is provided, the last one is used)
                    if not provided, final pdf will be saved at current directory as slides.pdf
    file:       svg file of subsequent layers
    bkg:        layer to put underneath subsequent slides
    over:       layer to put over subsequent slides

    *           do not count as a new slide (use * in front of any label to do not count that slide)

    AddSlideNumber = False, 'all', 'smart'
    add text to inkscape '##:slideNumber'. ## is replaced by the slide number

    PdfFileMerger
    pip install PyPDF2
    """
    f = Path(filepath).open()
    text = f.read()
    f.close()
    output_filepath = Path.cwd()/'slides.pdf'

    labelLists = []
    for line in text.splitlines():
        if line.startswith('#') or line=='':
            pass
        elif line.startswith('save at:'):
            output_filepath = Path(line.split('save at:')[-1])
        else:
            labelLists.append([label.strip() for label in line.split(',')])

    try:
        f = tempfile.TemporaryDirectory()
        pdf_filepathlist = []

        idx = 0
        slideNumber = 0
        changeSlideNumber = False
        bkg = ''
        over = ''
        for labelList in labelLists:
            if labelList[0].startswith('file:'):
                presentation = ink.inkscapeFile(labelList[0].split('file:')[-1])
            elif labelList[0].startswith('bkg:'):
                bkg = ''
                for label in labelList[0].split('bkg:')[-1].split(','):
                    if label == '':
                        pass
                    else:
                        bkg += presentation.layers[label]+'\n'
            elif labelList[0].startswith('over:'):
                print(labelList)
                over = ''
                for label in labelList:
                    label = label.split('over:')[-1]
                    if label == '':
                        pass
                    else:
                        over += presentation.layers[label]+'\n'
            else:

                filepath = Path(f'{f.name}/exported_{idx}.pdf')
                pdf_filepathlist.append(filepath)



                presentation.layers['bkg'] = bkg
                labelList.insert(0, 'bkg')
                presentation.layers['over'] = over
                labelList.append('over')

                # add slide number
                if AddSlideNumber:
                    if AddSlideNumber == 'smart':
                        changeSlideNumber = True
                        for label in labelList:
                            if label.startswith('*'):
                                changeSlideNumber = False
                                break
                            if label.startswith('!'):
                                if any(s.startswith('!') for s in labelList_old) or any(s.startswith('*') for s in labelList_old):
                                    changeSlideNumber = False
                        if changeSlideNumber:
                            slideNumber += 1
                        for label in labelList:
                            presentation.layers[label] = presentation.layers[label].replace('##:slideNumber', str(slideNumber))
                        labelList_old = copy.copy(labelList)
                    else:
                        slideNumber += 1
                        for label in labelList:
                            presentation.layers[label] = presentation.layers[label].replace('##:slideNumber', str(slideNumber))

                print(labelList)
                # presentation.exportLayerSet(labelList=labelList, filepath=f'exported_{idx}.svg')
                presentation.exportLayerSet2Pdf(labelList=labelList, filepath=filepath)
                idx +=1

        _merger(filepathlist=pdf_filepathlist, filepath=output_filepath)
    # except Exception as e:
    #     print("rrr")
    # #     print(e)
    # # except UnboundLocalError as e:
    #     raise Exception(e + '\n' + 'Maybe, \'file:\' is missing from the instruction file.')
    finally:
        # if keep_svg:
        #     shutil.copytree(f.name, str(output_filepath)+'_svg')
        #
        # else:
            f.cleanup()



def inkAutoSlide(filepath):
    """
        pdf is saved with the same name as the file


        add text to inkscape '##:slideNumber'. ## is replaced by the slide number

        gotofile:
        #           hide layer
        @           background
        $           over
        *           copy previous slide and add current layer
        !           copy previous slide, exclude layers (the number of layers
            excluded is the same as the number of !(, and add current layer
        +           add current layer to previous slide
        =           Copy layer (use =, ==, ===, ... to avoid having two layers
            with the same name)
        = ,         Copy multipe layers (=<layer1>, <layer2>, <layer3>)

        Note:
            = can copy layers with #

        PdfFileMerger
        pip install PyPDF2
    """
    try:
        # f = tempfile.NamedTemporaryFile(dir=Path.cwd())
        f = Path(Path.cwd() / 'slidesInstructions.txt').open('w+')
        # f.write(f'file:{filepath}')

        def slideList(filepath):
            presentation = ink.inkscapeFile(filepath)

            text = ''
            text += '\n\nfile:' + str(filepath)
            for label in presentation.getLabels():
                if label.strip().startswith('*'):
                    text += '\n' + text.splitlines()[-1] + ', ' + label
                # elif label.strip().startswith('!'):
                #     if text.splitlines()[-1].split(',')[-1].strip().startswith('!'):
                #         text += '\n' + ', '.join(text.splitlines()[-1].split(',')[:-1]) + ', ' + label
                #     else:
                #         text += ', ' + label
                elif label.strip().startswith('!'):
                    text += '\n' + ', '.join(text.splitlines()[-1].split(',')[:-label.count('!')]) + ', ' + label
                elif label.strip().startswith('='):
                    text += '\n' + label.split('=')[-1]
                elif label.strip().startswith('@'):
                    text += '\nbkg:' + label
                elif label.strip().startswith('$'):
                    text += '\nover:' + label
                elif label.strip().startswith('+'):
                    text += ', ' + label
                elif label.strip().startswith('gotofile:'):
                    nextfile = Path(label.split('gotofile:')[-1])
                    text += slideList(nextfile)
                    text += '\n\nfile:' + str(filepath)
                else:
                    text += '\n' + label

            return text

        text = slideList(filepath)

        f.write(text)
    finally:
        filepath = f.name
        f.close()
        inkSlide(filepath, AddSlideNumber='smart')


def _merger(filepathlist, filepath=Path.cwd()/'merged.pdf'):
    """Merge pdf's.

        Args:
            filepathlist (list): list of (string or Path object) with all pdf's to merge (in order)
            filepath (string or Path object): filepath for merged pdf file
    """
    # create merger
    pdf_merger = PdfFileMerger()

    # append to merger
    for pdf in filepathlist:
        pdf_merger.append(str(Path(pdf)))

    # check .pdf extension
    if Path(filepath).match('*.pdf'):  # Check filename extension
        pass
    else:
        filepath = str(filepath) + '.pdf'
    filepath = Path(filepath)

    #save file
    pdf_merger.write(str(filepath))


if __name__ == '__main__':

    instructions = 'Usage 1 : inkSlide <filepath to instruction file>\nUsage 2 : inkSlide auto <filepath to svg file>'
    if len(sys.argv) == 2:
        inkSlide(filepath=sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'auto':
            inkAutoSlide(filepath=sys.argv[2])
        else:
            print(instructions)
    else:
        print(instructions)
