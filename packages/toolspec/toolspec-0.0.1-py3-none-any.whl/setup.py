# -*- coding: utf-8 -*-

"""A setuptools based setup module.
See:
https://github.com/pypa/sampleproject

https://python-packaging.readthedocs.io/
https://packaging.python.org/tutorials/distributing-packages/
"""

# Always prefer setuptools over distutils
from setuptools import setup#, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the version from __init__
with open(path.join(here, 'toolspec/__init__.py'), encoding='utf-8') as f:
    __version__ = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

setup(
    name='toolspec',  # Required
    version=__version__,  # Required
    author='Xiaoqing Chen',  # Optional
    author_email='1092640727@qq.com',  # Optional
    packages=['toolspec'],  # Required
    package_dir={'toolspec':'toolspec'},
    description='Special Tools',  # Required
    long_description=long_description,  # Optional
)
