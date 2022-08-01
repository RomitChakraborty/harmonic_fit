#! /usr/bin/env python 

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
from scipy.interpolate import interp1d, CubicSpline
import math

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'
plt.rcParams["axes.prop_cycle"]

# Read CSV
csvFileName = sys.argv[1]
scan_var = csvFileName.split('.')[0]
pltFileName = scan_var + '.png'

csvData = []

with open(csvFileName, 'r') as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ' ')
    for csvRow in csvReader:
        csvData.append(csvRow)

# Get X, Y and store in np array

csvData = np.array(csvData)
csvData = csvData.astype(np.float)
X, Y = csvData[:,0], csvData[:,1]

au_to_kJpmol = 2625.5 
Y = np.array([y/2625.5 for y in Y])

# numerical second derivative of interpolant at equilibrium
def comp_k_numeric(X,Y):
    """
    Compute numerical double derivative at equilibrium given X and V[X]
    """
    #x_new = np.linspace(X.min(), X.max(), 65)
    f = interp1d(X, Y, kind='cubic', fill_value="extrapolate")
    xe = 0 
    h = 0.1*10**(-8)
    k_numeric = (1/(2.0*h)) * ((f(xe + 2.0*h) - f(xe))/(2.0*h) - (f(xe) - f(xe - 2.0*h))/(2.0*h))
    return (k_numeric)

def comp_k_numeric_prec(X,Y, n):
    """
    Compute numerical double derivative at equilibrium given X and V[X]
    """
    x_new = np.linspace(X.min(), X.max(), 65)
    f = interp1d(X, Y, kind='cubic')
    xe = 0 
    h = 0.1*10**(-n)
    k_numeric = (1/(2.0*h)) * ((f(xe + 2.0*h) - f(xe))/(2.0*h) - (f(xe) - f(xe - 2.0*h))/(2.0*h))
    return (k_numeric)

# analytic derivative of interpolant at equilibrium
def comp_k_analytic(X,Y):
    """
    Compute the analytic force constant given X, and V(X)    
    """
    N = X.size
    mid = int((N + 1)/2)
    f2 = CubicSpline(X,Y)
    k_analytic = f2(X, 2)[mid]
    return k_analytic, f2

# convert to cm-1
def convert_k_to_cminv(k):
    """
    Import force constant in Hartree/Ang^2
    convert it to cm-1
    """
    mu = 918.553523379183232925595706294
    #ang_to_bohr = 1/(0.529)
    nu = 1/(2*np.pi)*math.sqrt(k/mu)*(1/(137*10**-8))
    return (nu)

def convert_k_to_cminv_rotor(k):
    """
    Convert force constant in Hartree/Radian^2 to cm-1
    this is for h2
    """
    I = 1948.37443393238771437461228584
    nu = 1/(2*np.pi)*math.sqrt(k/I)*(1/(137*5.29*10**-9))
    return nu



k_numeric = comp_k_numeric(X, Y)
nu_numeric = convert_k_to_cminv(k_numeric)
zpve_numeric = nu_numeric/2
k_analytic, f2 = comp_k_analytic(X, Y)
nu_analytic = convert_k_to_cminv(k_analytic)
zpve_analytic = nu_analytic/2

print (scan_var, "Analytic ", k_analytic, nu_analytic, zpve_analytic)
print (scan_var, "Numeric ", k_numeric, nu_numeric, zpve_numeric)

plt.plot(X, Y, 'bo')
plt.plot(X, f2(X), 'b-')
plt.plot(X, f2(X, 1), 'rx--')
plt.plot(X, f2(X, 2), 'co--')

plt.legend(['Points', 'Cubic Spline', r'dV/dq', r"d$^2$V/dq$^2$"], fontsize = 12)
plt.xlabel(scan_var, fontsize = 16)
plt.ylabel("E(a.u) and higher derivs", fontsize = 16)

plt.savefig(pltFileName)
