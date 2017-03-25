#!/usr/bin/env python

from setuptools import setup


# confused? check setup.cfg
setup(
    package_dir={"devns": "devns"},
    entry_points={
        "console_scripts": ["devns = devns.cli:main"]
    }
)
