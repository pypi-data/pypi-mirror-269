from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'fitching Deftable and timeseries table'
LONG_DESCRIPTION = 'contain an api wrapper that helps to fetch gas cconsumption data.'

# Setting up
setup(
    name="gasconsumption",
    version=VERSION,
    author="Ahmad Riad",
    author_email="meuralengine@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas',],
    keywords=['python', 'Deftable', 'timeseries table'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)