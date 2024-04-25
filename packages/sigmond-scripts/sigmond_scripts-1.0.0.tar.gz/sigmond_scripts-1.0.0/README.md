# Sigmond Scripts #

This repository contains a set of scripts used for the analysis of 2-point temporal correlation functions.
They depend on the sigmond analysis package ([https://bitbucket.org/ahanlon/sigmond](https://bitbucket.org/ahanlon/sigmond)),
and you should first have sigmond installed before using these scripts.

These functions are modified for the PyCALQ package.

### Directory structure ###

- analysis - contains the main scripts for running the analysis
    - run_sigmond.py - the driving script (pass -h to see options)
- data_conversion - contains various scripts for converting data to various formats (e.g. hdf5, LapH-binary, sigmond-bins).
- example_yamls - contains some example yaml files that can be passed to run_sigmond.py
- doc - contains documenation for how to use the analysis scripts (not up to date at all)

### What software requirements are there? ###

- Python 3.8 is required
- Many Python modules
    - wheel
    - cython
    - pybind11
    - pyyaml
    - progressbar
    - sortedcontainers
    - pylatex
    - numpy
    - uncertainties
    - aenum
    - tqdm
    - h5py
    - matplotlib

### How do I get started? ###

- You first need data in a format that sigmond can read (either LapH-binary or sigmond-bins).
  The data_conversion scripts can be used for this

