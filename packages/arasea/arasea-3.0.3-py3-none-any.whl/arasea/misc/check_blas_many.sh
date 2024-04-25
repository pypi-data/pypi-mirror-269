#!/bin/bash
cat /proc/cpuinfo |grep "model name" |uniq
cat /proc/cpuinfo |grep processor
free
uname -a
#Fred to test distro numpy at LISA: PYTHONPATH=/u/bastienf/repos:/usr/lib64/python2.5/site-packages AESARA_FLAGS=blas__ldflags= OMP_NUM_THREADS=8 time python misc/check_blas.py
