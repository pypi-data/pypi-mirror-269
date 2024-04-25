# -*- coding: utf-8 -*-
"""
setup.py

python-can-mcpcan
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="python-can-mcpcan",
    version="0.2.1",
    author="SoftMagic",
    author_email="softmajik@gmail.com",
    description="Python-can MCPcan",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hardbyte/python-can",
    package_dir={"": "mcpcan"},
    # py_modules=["mcpcan.mcpcan", "mcpcan.utils", "mcpcan.__init__"],
    python_requires=">=3.11",
    install_requires=["python-can"],
    entry_points={"can.interface": ["mcpcan = mcpcan:MCPcanBus"]},
)
