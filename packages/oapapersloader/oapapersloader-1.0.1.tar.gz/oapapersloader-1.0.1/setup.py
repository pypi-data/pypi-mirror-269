# -*- coding: UTF-8 -*-
""""
Created on 05.11.21

:author:     Martin Dočekal
"""
from setuptools import setup, find_packages


def is_requirement(line):
    return not (line.strip() == "" or line.strip().startswith("#"))


with open('README.md') as readme_file:
    README = readme_file.read()

with open("requirements.txt") as f:
    REQUIREMENTS = [line.strip() for line in f if is_requirement(line)]

setup_args = dict(
    name='oapapersloader',
    version='1.0.1',
    description='Package for working with OAPapers dataset.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='The Unlicense',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author='Martin Dočekal',
    keywords=['dataset', 'OAPapers loader', 'OAPapers dataset'],
    url='https://github.com/KNOT-FIT-BUT/OAPapersLoader',
    python_requires='>=3.9',
    install_requires=REQUIREMENTS
)

if __name__ == '__main__':
    setup(**setup_args)
