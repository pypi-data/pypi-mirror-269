from setuptools import setup, find_packages
# Dynamically fetch version and requirements as before
import os

# Dynamically read the version from your package/module
from wikiparser import __version__ as version

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='simple-wikiparser',
    version=version,
    packages=find_packages(),
    description='A simple Wikipedia parser',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Biswajit Satapathy',
    author_email='biswajit2902@gmail.com',
    url='https://github.com/biswajit2903/SimpleWikiParser',
    license='Apache License 2.0',
    install_requires=required,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    include_package_data=True
)
