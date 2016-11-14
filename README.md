# ardoq-archimate - a Python tool for importing archimate exchange files to Ardoq

## Description

ardoq_archimate is a tool for importing archimate models to [Ardoq](https://ardoq.com).


## Documentation
(see the test client for examples)

Implemented:

## Limitations / Issues
- Location not implemented. Waiting for Ardoq to include it in the template

## Installation

no `easy_install` or `pip` support
just clone it and use it as you need to

## Dependencies

- python3
- [ardoqpy](https://github.com/jbaragry/ardoq-python-client) - for integration with ardoq
- [xmltodict](https://github.com/martinblech/xmltodict) - for reading and writing xml


## Quick Start
To get started from an IDE

    clone the repo
    clone the ardoqpy project
    adjust your python path to include ardoqpy
    edit the config file to use your API key
    edit the config file to point to the archimate exchange file

or from the command-line

    download the zipfile for the ardoqpy
    download the zipfile for ardoq_archimate
    edit ardoqpy or python PATH to point to ardoqpy module
    edit the config file to use your API key
    edit the config file to point to the archimate exchange file


## Version

- 2016/04 - Initial version from archimate 2.1 to my own archimate 2.1 model
- 2016/11 - Refactored version to import archimate 2.1 to the official ardoq archimate 3 template/model

## TODO
- import archimate 3 exchange file once the spec if updated
- make the tool easier for non-programmers to use
    - perhaps solution in AWS lamda to provide archimate import as a service to Ardoq

## License
ardoq_archimate is licensed under the MIT License

See LICENSE.md
