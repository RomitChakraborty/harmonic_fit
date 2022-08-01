#! /usr/bin/env python 

import subprocess, re, os, time, random
import math
import numpy as np


def convert_k_to_cminv(k):
    """
    Import force constant in Hartree/Ang^2
    convert it to cm-1
    """
    mu = 918.553523379183232925595706294
    #ang_to_bohr = 1/(0.529)
    nu = 1/(2*np.pi)*math.sqrt(k/mu)*(1/(137*10**-8))
    return (nu)

k_list = [0.018960310761731762, 0.018634725, 0.009231205575136386, 0.007623297, 0.013665928861826174, 0.019693516]

for k in k_list:
    nu = convert_k_to_cminv(k)
    print (nu)

def convert_k_to_cminv_rotor(k):
    """
    Convert force constant in Hartree/Radian^2 to cm-1
    this is for h2
    """
    I = 1948.37443393238771437461228584
    nu = 1/(2*np.pi)*math.sqrt(k/I)*(1/(137*5.29*10**-9))
    return nu

k_rotor_list = [0.032352748, 0.007038849]

for k in k_rotor_list:
    nu = convert_k_to_cminv_rotor(k)
    print (nu)

