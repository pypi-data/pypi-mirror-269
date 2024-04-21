# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 09:51:01 2024

@author: Ailin
"""


import os
from setuptools import setup, find_packages

setup(
    name='weight_calculation',  
    version='1.0.0',  
    packages=find_packages(),  
    description='Package for calculating the total weight of items based on individual weight and quantity',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',  
    author='Ailin',  
    author_email='ailin.yar@yahoo.com',  
    keywords='weight calculation, packaging',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',  
    entry_points={
        'console_scripts': [
            'weight_calculation=weight_calculation:main',  
        ],
    },
)
    