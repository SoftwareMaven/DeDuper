#!/usr/bin/env python

from setuptools import setup, find_packages

dependencies = ['mutagen','smhasher',]
packages = find_packages()
scripts = ['scripts/deduper',]
setup(name='DeDuper',
      version='0.1',
      description='File De-Duplicator',
      author='Travis Jensen',
      author_email='travis.jense@gmail.com',
      url='https://github.com/SoftwareMaven/DeDuper',
      packages=packages,
      scripts=scripts,
      requires=dependencies,
     )
