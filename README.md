# ardoq-archimate - a Python tool for importing archimate exchange files to Ardoq

## Description

ardoq_archimate is a tool for importing archimate models to [Ardoq](https://ardoq.com).

Note: this is an open source project to import archimate exchange format to Ardoq. 
It is not an officially supported part of Ardoq.
Contact the author through github if you find bugs or need updates

## Documentation
(see the test client for examples)

## Limitations / Issues
- Location not implemented. Waiting for Ardoq to include it in the template
- Workspaces are not added to folder. API call to move a workspace is not working
- Properties are ignored

## Dependencies

- python3
- [ardoqpy](https://github.com/jbaragry/ardoq-python-client) - for integration with ardoq
- [xmltodict](https://github.com/martinblech/xmltodict) - for reading and writing xml

## Quick Start
To get started from an IDE

    clone the repo or just download ardoq_archimate.py
    install ardoqpy using pip
    edit the config file to use your API key and host
    edit the config file to point to the archimate exchange file
    when in dir ardoq_archimate, run program

## Version

- 2022/02 - Added Strategy workspace and ValueStream components
- 2022/01 - Updated for new ways of using model templates in Ardoq
- 2016/11 - Refactored version to import archimate 2.1 to the official ardoq archimate 3 template/model
- 2016/04 - Initial version from archimate 2.1 to my own archimate 2.1 model

## Changelog
- 20220121
  - updated to deal with new ways of using templates and models in Ardoq
  - deprecated org as a separate param. Now part of hostname
  - general cleanup for 6y.o code
  - ignore properties until they can be successfully imported as Fields

- 20210717
  - previous updates


## TODO
- Make config file available as a cmd line param
- make the tool easier for non-programmers to use
    - perhaps solution in AWS lamda to provide archimate import as a service to Ardoq
- Import Properties as Fields

## License
ardoq_archimate is licensed under the MIT License

See LICENSE.md
