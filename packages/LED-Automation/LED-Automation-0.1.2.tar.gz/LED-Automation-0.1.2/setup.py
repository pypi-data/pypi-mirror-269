# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README.md file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="LED-Automation",
    version="0.1.2",
    description="LED Automation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://about.readthedocs.com/?ref=readthedocs.org",
    author="Joshua Parker",
    author_email="Joshua.Parker@johnsonfit.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    packages=["LEDAutomation"],
    include_package_data=True,
    install_requires=["numpy"]
)