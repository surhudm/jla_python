import numpy as np
import sys
sys.path.append("install/lib/python2.7/site-packages/")
sys.path.append("../aum/install/lib/python2.7/site-packages/")
import cosmology as cc
import jla
import frogress
import emcee

verbosity=0
likelihood = jla.JLALikelihood(verbosity)
#likelihood.read("data/z_0.20_0.50/jla.dataset")
likelihood.read("data/jla.dataset")
zsn = jla.doubleArray_frompointer(likelihood.getZ())
zhel = jla.doubleArray_frompointer(likelihood.getZhel())
nuisance_parameters = jla.doubleArray(4)
snsize = likelihood.size()
mu = jla.doubleArray(snsize)

#
# Fiducial value for nuisance parameters:
# 0.1410 3.1010 -19.05 -0.070
# 
def loglikelihood(par):
    chisq = computechisq(par)
    return -0.5*chisq

def computechisq(par):
    global zsn, snsize, mu, likelihood
    
    nuis = par[0:4]
    nuisance_parameters[0] = nuis[0] 
    nuisance_parameters[1] = nuis[1] 
    nuisance_parameters[2] = nuis[2] 
    nuisance_parameters[3] = nuis[3] 
    
    mainpar = par[4:]
    aum = cc.cosmology(mainpar[0], mainpar[1], -1.0, 0.0, 0.0476, 0.7, 2.7255, 0.8, 0.96, np.log10(8.0), 1.0)
    for i in range(snsize):
        mu[i] = 25.0+5.0*np.log10((1.+zhel[i])*aum.Dcofz(zsn[i])/0.7)
        #print zsn[i], aum.Dlofz(zsn[i])/0.7
    
    chisq = likelihood.computeLikelihood(mu, nuisance_parameters)  
    if np.isnan(chisq):
        chisq = 1.0E30

    print par, chisq
    return chisq

par = np.array([0.1410, 3.1010, -19.05, -0.070, 0.30, 0.1])

ndim, nwalkers = 6, 20
p0 = [par+0.1*par*np.random.rand(ndim) for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, loglikelihood, threads=24)
sampler.run_mcmc(p0, 1000)
