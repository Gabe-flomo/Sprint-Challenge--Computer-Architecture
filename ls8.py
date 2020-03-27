#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
#filename = sys.argv[1]
filename = "E:\\Documents\\Atom\\Sprint challenges\\Sprint-Challenge--Computer-Architecture\\SCtest.txt"
cpu.load(filename)
cpu.run()