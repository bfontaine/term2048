# -*- coding: UTF-8 -*-

from os.path import dirname
import sys

from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='src/term2048/__init__.py'
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
    package_dir={'':'src'},
    packages=['term2048'],
    url='https://github.com/bfontaine/term2048',
    license='LICENSE',
    description='2048 in your terminal',
    long_description=open('README', 'r').read(),
    install_requires=[
        'colorama >= 0.2.7',
    ],
    scripts=['bin/term2048'],
)
