"""
To make dist folder
$ python setup.py sdist
"""

from setuptools import setup, find_packages

setup(
    name = "logtools"
    , version = "0.0.3"
    , packages = find_packages()
)