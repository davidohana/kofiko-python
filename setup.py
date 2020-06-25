from os import path

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kofiko',
    packages=['kofiko'],
    version="1.0.3",
    license='Apache',
    description="Code-First Configuration package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Ohana, IBM Research Haifa",
    author_email="david.ohana@ibm.com",
    url="https://github.com/davidohana/kofiko",
    keywords=['configuration', 'code', 'first', 'config', 'ini', 'environment', 'env', 'IBM'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
