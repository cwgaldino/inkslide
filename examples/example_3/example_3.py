#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inkSlide example 2."""

from pathlib import Path

import sys
sys.path.append('../..')
from inkSlide.inkSlide import inkAutoSlide
from inkSlide.inkSlide import inkSlide
import inkSlide.inkFile as ink
inkAutoSlide(filepath='presentation_A.svg')


# %% adding external images to a presentation ================


# %% adding movement ================


# %% adding transitions ================


# %% exporting to pdf ================


# %% exporting to jpg ================


# %% exporting to svg ================

#
# presentation = ink.inkscapeFile('presentation_A.svg')  # import .svg
# presentation.filepath
# presentation.filename
# print(presentation.prefix)
# print(presentation.endOfFile)
# presentation.layers
# presentation.getLabels()
#
#
# presentation.layers['+over 2'].attrs
# .replace('##:slideNumber', str(23)))
# print(presentation.layers['*nested slide 2'])
#
# if presentation.layers['*nested slide 2'] in presentation.layers['nested slide']:
#     print('tt')
#
# from bs4 import BeautifulSoup, Comment
# from collections import OrderedDict
# f = open('presentation_A.svg')
# soup = BeautifulSoup(f, features = 'xml')
# f.close()
# script_tags = soup.find_all('g')
# layers = OrderedDict()  # dict.key() is the layer label, dict.value() is the layer itself
# for i in range(len(script_tags)):
#     if 'inkscape:label' in script_tags[i].attrs:
#         del_list = []
#         for j in range(len(script_tags[i].contents)):
#             try:
#                 if 'inkscape:label' in script_tags[i].contents[j].attrs:
#                     del_list.append(j)
#             except AttributeError:
#                 pass
#         del_list = [x-n for n,x in enumerate(del_list)]
#         for j in del_list:
#             del script_tags[i].contents[j]
#
# script_tags[9].attrs['style'] = "display:inline"
# script_tags[21]
#
#
#         # layers[script_tags[i].attrs['inkscape:label']] = script_tags[i].prettify()
#         # try:
#         #     if script_tags[i+1] in script_tags[i].children:
#         #         j = script_tags[i].contents.index(script_tags[i+1])
#         #         del script_tags[i].contents[j]
#         # except IndexError:
#         #     pass
#
# i = 20
# del_list = []
# for j in range(len(script_tags[i].contents)):
#     try:
#         if 'inkscape:label' in script_tags[i].contents[j].attrs:
#             del_list.append(j)
#     except AttributeError:
#         pass
# del_list = [x-n for n,x in enumerate(del_list)]
# for j in del_list:
#     del script_tags[i].contents[j]
#
#
#
#
# script_tags_2 = soup.find_all('svg')
# prefix = script_tags_2[0].parent.prettify().replace(script_tags_2[0].prettify(), '')
# print(script_tags_2[0].prettify())
#
#
# script_tags_2[0].prettify().split('<g')[0]
# script_tags_2[0].prettify().split('<g')[-1]
#
# .index(list(layers.items())[0][1])
#
# for i in range(len(list(script_tags_2[0].children))):
#     try:
#         if list(script_tags_2[0].children)[i].prettify() == list(layers.items())[0][1]:
#             break
#         else:
#             prefix +=list(script_tags_2[0].children)[i].prettify()
#     except AttributeError:
#         pass
#
#
#
#
# script_tags[0].__dir__()
# str(script_tags[0].find_parent().index('xmlns')
# len(script_tags[0].findChildren())
# del script_tags[1].contents[3]
# help(script_tags[0].find())
#
# script_tags = soup.find_all('g')
# layers = OrderedDict()  # dict.key() is the layer label, dict.value() is the layer itself
# for i in range(len(script_tags)):
#     if 'inkscape:label' in script_tags[i].attrs:
#         layers[script_tags[i].attrs['inkscape:label']] = script_tags[i].prettify()
#         try:
#             if script_tags[i+1] in script_tags[i].children:
#                 j = script_tags[i].contents.index(script_tags[i+1])
#                 del script_tags[i].contents[j]
#         except IndexError:
#             pass
#
# script_tags[0].attrs['inkscape:label']
# script_tags[1].attrs['inkscape:label']
# script_tags[2].attrs['inkscape:label']
# if script_tags[2] in script_tags[1].children:
#     i = script_tags[1].contents.index(script_tags[2])
#     del script_tags[1].contents[i]
#
#
#
#     script_tags[1].attrs['inkscape:label']
#
# script_tags[3].attrs['inkscape:label']
# script_tags[4].attrs
# script_tags[5].attrs
# script_tags[6].attrs['inkscape:label']
# script_tags[7].attrs
# script_tags[8].attrs
#
#
#
#
#
# script_tags[1].findChildren()[2]
# script_tags[2]
# script_tags[3]
# script_tags[4]
#
# script_tags = [str(x) for x in soup.find_all('g')]
# len(script_tags)
#
# lines = script_tags[0].split(' ')
# try:
#     print([line for line in lines if line.strip().startswith('inkscape:label=\"')][0].split('\"')[-2])
# except: print(0)
# presentation._getLayerLabel(script_tags[0])
#
