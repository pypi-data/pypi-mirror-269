# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:41:28 2018

@author: Michael Green, Xiaobo Chen
The University of Missouri-Kansas City

---

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

questions regarding implementation can be directed towards magwwc@mail.umkc.edu or chenxiaobo@umkc.edu

---
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from scipy.integrate import quad
import sys

#file_string = 'Sample GC data 1 pt acetone 1 pt cyclohexane.csv'

data_set = pd.read_csv(sys.argv[1]).to_numpy()

initials = [
    [4.5, 13, 1], 
    [2.5, 19, 1]
]

n_value = len(initials)

def gaussian(x,a,b,c):
    return a*np.exp((-(x-b)**2.0)/c**2.0)

def GaussSum(x, p, n):
    return sum(gaussian(x, p[3*k], p[3*k+1], p[3*k+2]) for k in range(n))

def residuals(p, y, x, n):
    return y - GaussSum(x,p,n)  

cnsts =  leastsq(
            residuals, 
            initials, 
            args=(
                data_set[:,1],          # y data
                data_set[:,0],          # x data
                n_value                 # n value
            )
        )[0]

areas = dict()

for i in range(n_value):
    areas[i] = quad(
        gaussian,
        data_set[0,0],      # lower integration bound
        data_set[-1,0],     # upper integration bound
        args=(
            cnsts[3*i], 
            cnsts[3*i+1], 
            cnsts[3*i+2]
        )
    )[0]


x = np.linspace(data_set[0,0],data_set[-1,0],200)

fig, ax = plt.subplots(dpi = 100)

ax.tick_params(direction = 'in', pad = 15)
ax.set_xlabel('time / s', labelpad = 20, fontsize = 15)
ax.set_ylabel('Intensity / a.u.', labelpad = 20, fontsize = 15)

ax.plot(data_set[:,0], data_set[:,1], 'ko')
ax.plot(x,GaussSum(x,cnsts, n_value))

for i in range(n_value):
    ax.plot(
        x, 
        gaussian(
            x, 
            cnsts[3*i], 
            cnsts[3*i+1], 
            cnsts[3*i+2]
        )
    )

ledger = ['Data', 'Resultant']
for i in range(n_value):
    ledger.append(
        str(round(cnsts[3*i+1], 2)) + 
        '$e^{(x-' + str(round(cnsts[3*i], 2)) + 
        ')^2 / ' + str(round(cnsts[3*i + 2], 2)) + 
        '^2}$' + ' \n Area = ' + str(round(areas[i], 3))
    ) 

ax.legend(ledger)

plt.tight_layout()

def main():
 plt.savefig('result.png')
 plt.show()
if __name__ == "__main__":
 main()

