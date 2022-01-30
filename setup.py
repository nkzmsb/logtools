"""
To make dist folder
$ python setup.py sdist
"""

from setuptools import setup, find_packages

setup(
    name = "logtools"
    , version = "0.1.0"
    , packages = find_packages()
    , zip_safe=False
    
    , author = "nkzmsb"
    , url = "https://github.com/nkzmsb/logtools"
    , description = "This is a wrapper for logging"
    , long_descriptoin=open("README.md", encoding='utf-8').read()
    , long_description_content_type = "text/markdown"
    
    , python_requires = ">=3.7"
    
)