#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='wegotpop-test',
    version='0.0.1',
    author='Marco Alabruzzo',
    author_email='marco.alabruzzo@gmail.com',
    packages=[
        'artist',
    ],
    include_package_data=True,
    zip_safe=False,
    scripts=['app.py', 'tests.py'],
)
