#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inkSlide example 2."""

from pathlib import Path

import sys
sys.path.append('../..')
from inkSlide.inkSlide import inkSlide

# inkSlide(filepath='slidesInstructions.txt', AddSlideNumber=False)
# inkSlide(filepath='slidesInstructions.txt', AddSlideNumber='all')
inkSlide(filepath='slidesInstructions.txt', AddSlideNumber='smart')
