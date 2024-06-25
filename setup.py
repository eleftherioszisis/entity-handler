#!/usr/bin/env python
import importlib.util
from pathlib import Path

from setuptools import setup, find_packages


setup(
    name="entity-handler",
    author="bbp-ou-nse",
    author_email="bbp-ou-nse@groupes.epfl.ch",
    version="0.1",
    entry_points={"console_scripts": ["entity-handler=entity_handler.cli:app"]},
    install_requires=[
        "click>=8.0",
        "libsonata",
        "numpy",
        "pandas",
        "entity_management>=1.2.41",
        "blue-cwl",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
)

