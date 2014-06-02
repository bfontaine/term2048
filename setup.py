# -*- coding: UTF-8 -*-

from os.path import dirname
import sys

import setuptools
from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='term2048/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='term2048',
    version=verstr,
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    packages=['term2048'],
    url='https://github.com/bfontaine/term2048',
    license=open('LICENSE', 'r').read(),
    description='2048 in your terminal',
    long_description=open('README.rst', 'r').read(),
    install_requires=[
        'colorama >= 0.2.7',
        'argparse >= 1.1',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts':[
            'term2048 = term2048.ui:start_game'
        ]
    },
)
