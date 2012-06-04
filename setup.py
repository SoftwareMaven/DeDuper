#!/usr/bin/env python

from distutils.core import setup

dependencies = ['mutagen',]
packages = ['deduper',]
scripts = ['scripts/deduper',]
setup(name='DeDuper',
      version='0.1',
      description='File De-Duplicator',
      author='Travis Jensen',
      author_email='travis.jense@gmail.com',
      url='https://github.com/SoftwareMaven/DeDuper',
      packages=packates,
      scripts=scripts,
      requires=dependencies,
     )
