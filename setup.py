#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


# Get long description (used on PyPI project page)
def get_long_description():
    try:
        # Use pandoc to create reStructuredText README if possible
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except:
        return None


setup(
    name='cidr-brewer',
    version='1.0.0',
    description='A CLI utility for working with classless IP addresses',
    long_description=get_long_description(),
    url='https://github.com/caleb531/cidr-brewer',
    author='Caleb Evans',
    author_email='caleb@calebevans.me',
    license='MIT',
    keywords='networking ip addresses cidr',
    py_modules=['cidrbrewer'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'cidr-brewer=cidrbrewer:main'
        ]
    }
)
