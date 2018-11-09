#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simf-python-gui",
    version="0.0.2",
    author="A.J. Fite, Sara Kipps",
    author_email="me@ajfite.com, skipps@calpoly.edu",
    description="A GUI controller for the closed source SIMF camera capture utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.nclf.net/SIMF/simf-python-gui",
    packages=setuptools.find_packages(),
    package_data={'simf-python-gui': ['*.ui']},
    entry_points={
        'gui_scripts': ['simf-gui=simf-python-gui.main:main'],
    },
    data_files=[('', ['LICENSE.md'])],
    install_requires=['PyQt5', 'watchdog'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)