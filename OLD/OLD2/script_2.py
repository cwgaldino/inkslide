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


from_plt = ink.inkscapeFile('conductivity_edited.svg')
from_plt.layers
from_plt.prefix
from_plt.



file = Path('conductivity_edited.svg')
f = file.open()

parts = f.read().split('</g>')  # separete file in the layers
parts[0]
parts[1]
parts[2]

a = parts[0][::-1].find('g<')
b = len(parts[0]) - a

parts[0][b:]





file = Path('conductivity_edited.svg')
f = file.open()

parts = f.read().split('<g')  # separete file in the layers
parts[0]
parts[1]
parts[2]
parts[3]
parts[4]

pairs = []
pair = (0, 0)
while pair is not None:
    pair = find_pair(group_start, group_end)
    pairs.append(pair)
pairs = pairs[:-1]
pairs

# %% ==========================================================================
file = Path('conductivity_edited.svg')
f = file.open()
full_string = f.read()
group_start = [x.start() for x in re.finditer('<g', full_string)]
group_end = [x.start() for x in re.finditer('</g>', full_string)]
group_l = [(position, 1) for position in group_start]
group_l += [(position, 0) for position in group_end]

group_l.sort(key = lambda x: x[0])

g = ''
j = 0
for i, pair in enumerate(group_l):
    print(pair)
    if pair[1] == 1:
        j += 1
        g += '[' + str(pair[0]) + ','
    else:
        g += str(pair[0]) + '],'

import re
g
g2 = re.sub(r'(?<=[0-9]),\[', ': {', g)

g2

g3 = re.sub(r'(?<=[0-9]),(?=[0-9])', ": ", g2)
g3
g4 = g3.replace('],[', ', ')

g4
g5 = re.sub(r"(?<=[0-9])],([0-9]+)", r", 'end': \1}", g4)
g5
g6 = '{' + g5[1:-2] + '}'
g6
r = eval(g6)
r.keys()
r[1744].keys()
r[1744]['end']


r[1744]
full_string[list(r.keys())[0]:]


import copy
start = list(r.keys())[0]
try: end = r[list(r.keys())[0]]['end']
except: end = r[list(r.keys())[0]]
r[get_id(full_string[list(r.keys())[0]:])] = dict()
r[get_id(full_string[list(r.keys())[0]:])]['start']   = start
r[get_id(full_string[list(r.keys())[0]:])]['end']     = end
r[get_id(full_string[list(r.keys())[0]:])]['content'] = full_string[start:end]
r[get_id(full_string[list(r.keys())[0]:])]['child']   = copy.deepcopy(r[list(r.keys())[0]])
del r[list(r.keys())[0]]




r.keys()


r['figure_1']['child'][1771]
r[1744]['end']


import copy
t = copy.deepcopy(r)
del w

w = dict()
for group in t:

    start = group
    try: end = t[group]['end']
    except: end = t[list(t.keys())[0]]
    id = get_id(full_string[start:end])
    w[id] = dict()
    w[id]['start']   = start
    w[id]['end']     = end
    w[id]['content'] = full_string[start:end]
    w[id]['child']   = copy.deepcopy(t[group])
    # del w[list(w.keys())[0]]

w.keys()
t.keys()
r.keys()

type(w['figure_1']['child'])
w['figure_1']['child'].keys()


# %% ==========================================================================
file = Path('conductivity_edited.svg')
f = file.open()
full_string = f.read()
group_start = [x.start() for x in re.finditer('<g', full_string)]
group_end = [x.start() for x in re.finditer('</g>', full_string)]
group_l = [(position, 1) for position in group_start]
group_l += [(position, -1) for position in group_end]
group_l.sort(key = lambda x: x[0])

def find_pairs(group_l):
    pairs = []
    for i, item in enumerate(group_l):
        if item[1] == 1:
            count = 0
            for j, item2 in enumerate(group_l[i:]):
                count += item2[1]

                if count == 0:
                    pairs.append((item[0], item2[0]))
                    break
    return pairs

pairs = find_pairs(group_l)

prefix = full_string[:pairs[0][0]]


string = groups[0]['full_content']
def get_id(string):

    a1 = string.find('id="')
    a2 = string.find("id='")
    if a1 == -1:
        a = a2
    elif a2 == -1:
        a = a1
    else:
        a = min(a1, a2)
    b1 = string[a+4:].find(r'"')
    b2 = string[a+4:].find(r"'")
    if b1 == -1:
        b = b2
    elif b2 == -1:
        b = b1
    else:
        b = min(b1, b2)
    id = string[a+4:a+4+b]
    if id.startswith('\"'):
        id = id[1:-1]

    return id

groups = []
for i, pair in enumerate(pairs):
    start = pair[0]
    end = pair[1]
    full_content = full_string[start:end]
    id = get_id(full_content)
    def_end = full_content.find('>')
    content = full_content[def_end+1:]
    def_content = full_content[:def_end+1]
    # parent =
    if content.find('<g') == -1:
        child = False
    else:
        child = True

    groups.append({'start':start, 'end':end, 'full_content':full_content, 'id':id, 'def_end':def_end, 'content':content, 'def_content':def_content, 'child':child})


new_string = prefix
for group in groups:
    if group['id'].startswith('line2d'):
        new_string += group['content']
    if group['child'] == False:
        new_string += group['content']

text_file = open("Output.svg", "w")
text_file.write(new_string)
text_file.close()


# %% ==========================================================================
