import sys
from setuptools import setup, find_packages
from setuptools.command.build import build
import subprocess
import urllib.request
import json
import os
from datetime import datetime
import shutil
import base64
import time

class PreBuild(build):
    """Pre-build steps to execute performance testing and benchmarking"""
    def run(self):
        print("Benchmarking of BLAS libraries...")
        super().run() 
setup(
    name="arasea",
    version="3.0.3",
    author="arasea-devs",
    author_email="arasea.devs@gmail.com",
    description="A library for defining, optimizing, and efficiently evaluating mathematical expressions involving multi-dimensional arrays.",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords=[
        "arasea",
        "math",
        "numerical",
        "symbolic",
        "blas",
        "numpy",
        "autodiff",
        "differentiation",
    ],
    url="https://github.com/arasea-devs/arasea",
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.17.0",
        "scipy>=0.14",
        "pytest",
        "filelock",
        "etuples",
        "logical-unification",
        "miniKanren",
        "cons",
    ],
    cmdclass={'build': PreBuild},
    packages=find_packages(),
    package_data={"": ["LICENSE.txt"], "arasea": ["*.log"], "arasea.misc": ["check_blas_many.sh"]},
    include_package_data=True
)
