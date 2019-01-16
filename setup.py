#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyatmo',
    version='0.0.0',
    author='Astatine',
    author_email='astatine085@gmail.com',
    url='https://github.com/085astatine/pyatmo',
    packages=[
        'pyatmo',
        'pyatmo.weather'],
    install_requires=[
        'pytz',
        'pyyaml>=4.2b1',
        'requests>=2.20',
        'sqlalchemy'])
