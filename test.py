import numpy as np
import sys
sys.path.append("install/lib/python2.7/site-packages/")
sys.path.append("../../../cosmic/lib/python2.7/site-packages/")
import cosmology as cc
import jla
import frogress

aum = cc.cosmology(0.30, 0.0, -1.0, 0.0, 0.0476, 0.7, 2.7255, 0.8, 0.96, np.log10(8.0), 1.0)

verbosity=0
likelihood = jla.JLALikelihood(verbosity)
likelihood.read("data/z_0.20_0.50/jla.dataset")
#likelihood.read("data/jla.dataset")
zsn = jla.doubleArray_frompointer(likelihood.getZ())
nuisance_parameters = jla.doubleArray(4)
snsize = likelihood.size()
mu = jla.doubleArray(snsize)
mufid = np.zeros(snsize)

for i in range(snsize):
    mufid[i] = 25.0+5.0*np.log10(aum.Dlofz(zsn[i])/0.7)

zbao = 0.38

#
# Fiducial value for nuisance parameters:
# 0.1410 3.1010 -19.05 -0.070
# 
def loglikelihood(par):
    chisq = computechisq(par)
    return -0.5*chisq

def computechisq(par):
    global mufid, zsn, snsize, mu, likelihood, zbao
    
    nuis = par[0:4]
    nuisance_parameters[0] = nuis[0] 
    nuisance_parameters[1] = nuis[1] 
    nuisance_parameters[2] = nuis[2] 
    nuisance_parameters[3] = nuis[3] 
    
    mainpar = par[4:]
    muz = mufid * 0.0
    for i in range(snsize):
        muz[i] = mainpar[0] * (zsn[i]-zbao)**2 + mainpar[1] * (zsn[i]-zbao) + mainpar[2]

    for i in range(snsize):
        mu[i] = mufid[i] + muz[i]
    
    chisq = likelihood.computeLikelihood(mu, nuisance_parameters)  
    if np.isnan(chisq):
        chisq = 1.0E30

    print par, chisq
    return chisq

par = np.array([0.1410, 3.1010, -19.05, -0.070, 0.0, 0.0, 1.0])

from scipy.optimize import fmin
pbest = fmin(computechisq, par)
print pbest
