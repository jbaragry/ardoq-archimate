# ardoq-archimate - a Python tool for importing archimate exchange files to Ardoq

## Description

ardoq-archimate is a tool for importing archimate models (in .xml format) to [Ardoq](https://ardoq.com). Sign up for a trial at https://ardoq.com.

Note: this is an open source project to import archimate exchange format to Ardoq. 
It is not an officially supported part of Ardoq.
Contact the author through github if you find bugs or need updates


## Limitations / Known Issues
- Location not implemented. Waiting for Ardoq to include it in the template
- Workspaces are not added to folder. API call to move a workspace is not working
- Properties are ignored

## Dependencies

- python3
- [ardoqpy](https://github.com/jbaragry/ardoq-python-client) - for integration with ardoq
- [xmltodict](https://github.com/martinblech/xmltodict) - for reading and writing xml

## Quick Start
    
Steps:

    git clone https://github.com/jbaragry/ardoq-archimate.git
    cd ardoq-archimate
    pip3 install --user ardoqpy xmltodict
    cd ardoq_archimate
    python3 ardoq_archimate.py --host https://myorg.ardoq.com/ -t <insert_token_here> -x <insert_path_to_xml_file_here>
    
Using config file:

    clone the repo or just download ardoq_archimate.py
    install ardoqpy and xmltodict using pip
    edit the config file to use your API token from Account Settings in Ardoq and host (https://yourhostname.ardoq.com)
    edit the config file to point to the archimate exchange file
    when in dir ardoq_archimate, run program
    

## Version

- 2023/02 - parent-child for composition
- 2022/12 - Added flag to use the sync client to update components rather than replace
- 2022/02 - Added Strategy workspace and ValueStream component types
- 2022/01 - Fix to support changes to usage of model templates in Ardoq
- 2016/11 - Refactored version to import archimate 2.1 to the official ardoq archimate 3 template/model
- 2016/04 - Initial version from archimate 2.1 to my own archimate 2.1 model

## Changelog
- 20230216
  - ability to convert composition to parent-child relationships for named component types. p-c must be of the same type

- 20220121
  - updated to deal with new ways of using templates and models in Ardoq
  - deprecated org as a separate param. Now part of hostname
  - general cleanup for 6y.o code
  - ignore properties until they can be successfully imported as Fields

- 20210717
  - previous updates


## TODO
- make the tool easier for non-programmers to use
    - perhaps solution in AWS lamda to provide archimate import as a service to Ardoq
- Import Properties as Fields

## License
ardoq_archimate is licensed under the MIT License

See LICENSE.md
