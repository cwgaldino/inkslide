#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inkSlide example 2."""

from pathlib import Path
from inkslide import create_instructions, inkslide

inkslide(filepath=create_instructions('presentation_A.svg'))
