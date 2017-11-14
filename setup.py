#!/usr/bin/env python

from setuptools import setup


# confused? check setup.cfg
setup(
    name="devns",
    version="0.4.7",
    author="Dave Hayes",
    author_email="dwhayes@gmail.com",
    description="Pure Python DNS server for developers",
    keywords="dns",
    license="MIT License",
    url="https://github.com/daveisadork/PyDevNS",
    package_dir={"devns": "devns"},
    entry_points={
        "console_scripts": ["devns = devns.cli:main"]
    },
    zip_safe=True,
    packages=["devns"],
    install_requires=["future", "six"],
    setup_requires=["future", "six"],
    tests_require=[
        "future",
        "mock>=2.0",
        "pytest>=2.9,<3",
        "pytest-cov>=2.4",
        "pytest-runner",
        "six",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Software Development",
        "Topic :: System",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
)
