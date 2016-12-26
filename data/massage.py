#!/usr/bin/env python
# Author: Surhud More
# Email: surhudkicp@gmail.com

import numpy as np
import pandas
import sys

from subprocess import call

zmin = float(sys.argv[1])
zmax = float(sys.argv[2])

dire = "z_%0.2f_%0.2f/" % (zmin, zmax)
call("mkdir %s" % dire, shell=1)

df = pandas.read_csv("jla_lcparams.txt", delim_whitespace=1)
idx = (df.zcmb>zmin) & (df.zcmb<=zmax)
df = df[idx]
df.to_csv("%s/jla_lcparams.txt" % dire, sep=" ", index=0)
idx = idx.values

# Now keep reading the covariance matrices and dumping them out one by one
import glob
for fil in glob.glob("jla_v*_covmatrix.dat"):
    data = np.loadtxt(fil, skiprows=1)
    nn = idx.size
    n = np.sum(idx)
    data = np.reshape(data, (nn, nn))
    data = data[idx].T[idx].T
    data = data.reshape(n*n)
    
    fp = open("%s/%s" % (dire, fil[:]), "w")
    fp.write("%d\n" % n) 
    np.savetxt(fp, data)
    fp.close()
