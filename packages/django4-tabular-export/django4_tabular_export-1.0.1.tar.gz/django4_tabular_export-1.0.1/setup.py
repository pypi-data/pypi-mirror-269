#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

from setuptools import setup

setup(
    name='django4-tabular-export',
    version='1.0.1',
    description="""Simple spreadsheet exports for Django 4+""",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Franco Borrelli',
    author_email='francoborrelli96@gmail.com',
    url='https://github.com/francoborrelli/django4-tabular-export',
    packages=[
        'tabular_export',
    ],
    include_package_data=True,
    install_requires=[
        'django',
        'xlsxwriter',
    ],
    test_suite='tests.run_tests.run_tests',
    license='CC0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
)
