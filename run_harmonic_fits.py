#! /usr/bin/env python 

import subprocess, re, os, time, random
from glob import *

transdats = ['x_trans.dat', 'y_trans.dat', 'z_trans.dat']

print ("k(Hartree/Ang^2) nu(cm-1) ZPVE(cm-1) for translations")

for dat in transdats:
    subprocess.call("python3 harmonic_fit.py " + dat, shell = True)

rotdat = ['z_phi.dat', 'y_theta.dat']

for dat in rotdat:
    if ('y_theta' in dat):
        subprocess.call("python3 harmonic_fit_rot.py " + dat, shell = True)
    if ('z_phi' in dat):
        subprocess.call("python3 harmonic_fit_rot_phi.py " + dat, shell = True)
