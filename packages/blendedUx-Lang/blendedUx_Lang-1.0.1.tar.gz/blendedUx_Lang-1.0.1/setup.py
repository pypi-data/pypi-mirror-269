from distutils.core import setup
#!/usr/bin/env python
import os
from setuptools import setup, find_packages

DESCRIPTION = 'Blendedux_lang'
VERSION = '1.0.1'

setup(
url='http://blended.dbmonline.net/',
description = DESCRIPTION,
name='blendedUx_Lang',
version= VERSION,
license='license.txt',
author='Cognam Technologies',
author_email='hbhadu@cognam.com',
packages=find_packages(),
include_package_data=True,
install_requires=[],
zip_safe = False,
)