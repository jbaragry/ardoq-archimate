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

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ardoqarchimate',
    version='0.0.6',
    description='ArchiMate Open Exchange Format (R) importer for Ardoq (R)',
    long_description=long_description,
    url='https://github.com/jbaragry/ardoq-archimate',
    author='Jason Baragry',
    license='MIT',
    packages=find_packages(exclude=['resources']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
    # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='architecture ardoq archimate import development tool',
    install_requires=['ardoqpy', 'xmltodict', 'configparser'],
)
