# setup.py

import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='LR1STPKG',
    version='0.1',
    description='A simple Python package named LR1STPKG',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author='Your Name',
    author_email='your@email.com',
    packages=['LR1STPKG'],
)