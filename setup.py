__author__ = 'user'

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
# Determine if Windows or Mac
import platform

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

print(platform.system())
print find_packages()
if platform.system() == 'Windows':
    data_files=[('./sbol', ['sbol/bin/Win_32/_libsbol.pyd', 'sbol/bin/Win_32/libsbol.py'])]
elif platform.system() == 'Darwin':
    data_files=[('./sbol', ['sbol/bin/Mac_OSX/_libsbol.so', 'sbol/bin/Mac_OSX/libsbol.py'])]
	
setup(
    name='sbolqc',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0b1',

    description='A Python module for visualizing, constructing, reading, writing, and publishing genetic designs according to the standardized specifications of the Synthetic Biology Open Language (SBOL).',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/SynBioDex/SBOL-QC',

    # Author details
    author='Bryan Bartley',
    author_email='bartleyba@sbolstandard.org',

    # Choose your license
    license='Apache 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: Apache 2.0',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='synthetic biology',

    packages=find_packages(),  # Should find packages dnaplotlib, sbol, and qc

    data_files = data_files,

    zip_safe = False  # Prevents .egg from installing as a .zip.  It must be unpacked to import the _libsbol binaries properly
)
