import re

import setuptools
from setuptools import find_packages

with open("./flatfilediff/__init__.py", "r") as f:
    content = f.read()
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flatfilediff",
    version=version,
    author="capjamesg",
    author_email="jamesg@jamesg.blog",
    description="Monitor for changes in a file that stores a list of items.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/capjamesg/flatfilediff",
    install_requires=["requests"],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)