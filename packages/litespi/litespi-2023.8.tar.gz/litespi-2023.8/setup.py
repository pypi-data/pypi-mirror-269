#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="litespi",
    description="Small footprint and configurable SPI core",
    author="LiteSPI Developers",
    version                       = "2023.08",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/litex-hub",
    download_url="https://github.com/litex-hub/litespi",
    test_suite="test",
    license="BSD",
    python_requires="~=3.6",
    packages=find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "litespi_gen=litespi.gen:main",
        ],
    },
)
