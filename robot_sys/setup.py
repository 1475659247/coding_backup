# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='robot_sys',
    version='0.1.0',
    description='crawler for uugongye',
    long_description=readme,
    author='kuku',
    author_email='kuku.whu@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

