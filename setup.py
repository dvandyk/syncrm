#!/usr/bin/python
# vim: set sw=4 sts=4 et tw=120 :

from setuptools import setup, find_packages

with open('rmt/_version.py') as f:
    exec(f.read())

setup(name='rmt',
    version=__version__,
    author='Danny van Dyk',
    author_email='danny.van.dyk@gmail.com',
    url='https://github.com/dvandyk/rmt',
    description='Toolkit to synchronize with the reMarkable eInk tablet',
    license='LGPLv2',
    packages=find_packages(),
    package_data={
        'rmt': [],
    },
    install_requires=[ 'FileLock', 'py-dateutil' ],
    extras_require={
        'testing': [],
    },
    entry_points={
        'console_scripts': [ 'rmt = rmt.cli:rmt_cli' ],
    },
)
