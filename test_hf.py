#! /usr/bin/env python

import subprocess, re, os, time, random
from glob import *

for scan in glob("*.dat"):
    print (scan)
    subprocess.call("python3 harmonic_fit.py " + scan + " > test_hf.log", shell = True)


