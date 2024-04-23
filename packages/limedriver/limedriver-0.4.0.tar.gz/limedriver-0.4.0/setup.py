from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

import subprocess
import os

from Cython.Build import cythonize

os.environ['CXX'] = 'h5c++ -shlib'

ext_modules = [
    Extension(
        'limedriver.binding',
        sources=['src/limedriver/limedriver.pyx', 'extern/limedriver/src/limedriver.cpp'],
        include_dirs=["extern/limedriver/src/", "/usr/include/hdf5/serial/"], # TODO: This is REALLY ugly.
        libraries=["LimeSuite", "hdf5_cpp", "hdf5"],
        language="c++",
    ),
]

setup(
    name='limedriver',
    ext_modules=cythonize(ext_modules),
)
