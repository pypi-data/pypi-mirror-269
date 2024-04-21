#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by Ohm89 <moniza.dev@gmail.com>


import os
import sys
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

readme = open(os.path.join(here, 'README.md')).read()
if sys.version.startswith('3.'):
    install_requires = ['psutil', 'netifaces', 'configparser', 'future', 'distro', 'certifi']
elif sys.version.startswith('2.7'):
    install_requires = ['psutil==5.6.7', 'netifaces', 'configparser==3.5.0', 'future', 'certifi']
else:
    install_requires = ['psutil', 'netifaces', 'configparser', 'future', 'certifi']


setuptools.setup(
    name='moniza',
    version='0.0.1',
    description='moniza server monitoring',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/ohm89/pip-moniza',
    author='ohm89',
    author_email='moniza.dev@gmail.com',
    maintainer='ohm89',
    maintainer_email='moniza.dev@gmail.com',
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring',
    ],
    keywords='moniza system monitoring agent',
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'moniza=moniza.moniza:main',
        ],
    },
    data_files=[('share/doc/moniza', [
        'moniza-example.ini',
        'LICENSE',
        'README.md',
    ])],
)