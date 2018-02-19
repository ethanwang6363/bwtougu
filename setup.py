#!usr/bin/evn python3
# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from os.path import (
    dirname, 
    join
)
from setuptools import (
    setup, 
    find_packages,
    )

with open(join(dirname(__file__), 'bwtougu/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()
    
requirements = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]

setup(
    name='bwtougu',
    version=version,
    description='bwtougu for python3',
    author='luhx',
    author_email='luhx@bangth.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='http://www.bangth.com',
    packages=find_packages(exclude=[]),
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        "console_scripts":[
            "bwtougu = bwtougu.__main__:entry_point"
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
