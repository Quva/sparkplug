# coding=utf-8

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup,find_packages

setup( name         = 'sparkplug',
       version      = '1.3.0',
       description  = 'Sparkplug',
       author       = 'Quva Oy',
       url          = 'https://github.com/Quva/sparkplug.git',
       packages     = find_packages(),
       install_requires = [],
       scripts      = ['bin/sparkplug']
)
       
       
