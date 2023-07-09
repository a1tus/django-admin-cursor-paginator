#!/usr/bin/env python3

import os

from setuptools import setup


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):  # __version__ = '0.1.2'
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError('Unable to find version string.')


setup(
    version=get_version('admin_cursor_paginator/version.py'),
)
