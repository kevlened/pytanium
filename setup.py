#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pytanium',
    version='0.1',
    description='Selenium wrapper to add additional features',
    long_description=open('README.rst').read(),
    author='Len Boyette',
    author_email='boyettel+pytanium@gmail.com',
    url='https://github.com/kevlened/pytanium',
    packages=['pytanium'],
    keywords=['testing'],
    requires=['selenium'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta'
    ]
     )

# To update pypi: 'python setup.py register sdist bdist_wininst upload'