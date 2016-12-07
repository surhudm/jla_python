#!/usr/bin/env python

"""
setup.py file for jla
"""

from distutils.core import setup, Extension

import numpy
# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

print numpy_include

jla_module = Extension('_jla',
                           sources=['src/jla.i', 'src/jla.cc', 'src/ini.i', 'src/ini.c'],
                           swig_opts=["-c++"],
                           libraries=['m', 'lapack', 'blas'],
                           include_dirs = [numpy_include],
                           )

setup (name        = 'jla',
       version     = '1.0rc',
       author      = "jla",
       url         = "http://supernovae.in2p3.fr/sdss_snls_jla/ReadMe.html",
       author_email= "surhud.more@ipmu.jp <For python support>",
       description = """SDSS SNLS JLA""",
       ext_modules = [jla_module],
       license     = ['GPL'],
       py_modules  = ["jla"],
       package_dir = { '':'src'},
       )

