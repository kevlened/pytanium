#!/usr/bin/env python

from distutils.core import setup

setup(name='pytanium',
      version='0.1',
      description='Selenium wrapper to add additional features',
      author='Len Boyette',
      author_email='boyettel+pytanium@gmail.com',
      url='https://github.com/kevlened/pytanium',
      packages=['pytanium'],
      requires=['selenium', 'unittest'],
     )