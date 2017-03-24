#!/usr/bin/env python

from setuptools import setup


# confused? check setup.cfg
setup(
    entry_points={
        "console_scripts": ["devns = devns.cli:main"]
    }
)
