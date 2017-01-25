import configparser
import sys, os
import xmltodict
import logging
import ardoqpy
sys.path.append('../resources')

from ardoqpy.ardoqpy import ArdoqClient
from ardoqpy.ardoqpy import ArdoqClientException

configfile='ardoq_archimate.cfg'
#configfile = "testardoq_archimate.cfg"
# configfile = "./ardoq_archimate/ardoq_archimate.cfg"
config = configparser.ConfigParser()

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
#log file hardcoded in same dir for now
logger = logging.getLogger(__name__)
ardoq = None
business_layer_template = '57c447c972fa6d6e74679763'
application_layer_template = '57c447c972fa6d6e74679765'
technology_layer_template = '57c447c972fa6d6e74679762'
motivation_layer_template = '57c447c972fa6d6e74679767'
strategy_layer_template = '57c447c972fa6d6e74679766'
implementation_layer_template = '57c447c972fa6d6e74679764'
physical_layer_template = '57c447c972fa6d6e74679768'

field_property_map =  {}

def get_config():
    try:
        logger.debug('path: %s', os.getcwd())
        if len(config.read(configfile)) != 1:
            raise RuntimeError("Could not read config file ", configfile)
    except:
        raise RuntimeError("could not get config file")


def get_tag_name(name_data, lang):
    if type(name_data) is list:
        for x in name_data:
            if x['@xml:lang'] == lang:
                if '#text' in x:
                    return x['#text']
                else:
                    return None;
    else: # xmltodict drops the list if its only one element
        if '#text' in name_data:
            return name_data['#text']
        else:
            return None;


def get_archimate_elements(doc, types):
    '''
    parse archimate interchange file and extract all components that match the types in a particular layer
    :param doc: xml doc
    :param types: list of archimate component types to extract
    :return: dict of components
    '''
    elems = {}
    for e in doc:
        logger.debug('e: %s', e)
        if e['@xsi:type'].lower() in types:
            elem = {}
            elem['id'] = e['@identifier']
            elem['type'] = e['@xsi:type']
            if 'label' not in e.keys():
                break
            elem['name'] = get_tag_name(e['label'], config['Archimate']['lang'])
            if 'documentation' in e:
                elem['description'] = get_tag_name(e['documentation'], config['Archimate']['lang'])
            else:
                elem['description'] = elem['id'] + ' : ' + elem['name']
            elems[e['@identifier']] = elem
            if 'properties' in e:
                elem['fields'] = {}
                for p in e['properties']['property']:
                    if type(p) is not unicode:
                        elem['fields'][field_property_map[p['@identifierref']]] = get_tag_name(p['value'], config['Archimate']['lang'])
        else:
            logger.error('found unknown archimate element type: [%s]', e['@xsi:type'])
    return elems


def get_archimate_relationships(doc, types):
    rels = {}
    for e in doc:
        if e['@xsi:type'].lower() in types:
            logger.debug('e: %s', e)
            elem = {}
            elem['id'] = e['@identifier']
            elem['type'] = e['@xsi:type']
            elem['source'] = e['@source']
            elem['target'] = e['@target']
            if 'label' in e:
                elem['name'] = get_tag_name(e['label'], config['Archimate']['lang'])
            else:
                elem['name'] = elem['type']
            if 'documentation' in e:
                elem['description'] = get_tag_name(e['documentation'], config['Archimate']['lang'])
            else:
                elem['description'] = elem['id'] + ' : ' + elem['type']
            rels[e['@identifier']] = elem
        else:
            logger.error('found unknown archimate relationship type: %s', e['@xsi:type'])
    return rels


def create_ardoq_components(layer, elems, config_items):
    '''
    Need to rewrite this whole function. Some 2.1 components need to move to other spaces
    takes on dict of ardoq definitions
    :param layer: dict of one ardoq workspace
    :param elems: list of elements for that layer from interchange file
    :param config_items: relevant section from config file
    :return:
    '''
    # get the model for the workspace so that I can get the ID
    ws_id = layer['ws_id']
    id_map = {}
    try:
        model = ardoq.get_model(ws_id=ws_id)
    except ArdoqClientException as e:
        logger.debug('could not get model: %s', e)
    layer['ardoq_component_types'] = model['root']
    layer['ardoq_reference_types'] = model['referenceTypes']
    logger.debug('attempting to add %d elements', len(elems))
    for e, ev in elems.items():
        if ev['type'].lower() in config_items.keys():
            elem_type = config_items[ev['type'].lower()]
            if elem_type == 'NONE':
                continue
            if ':' in elem_type:
                continue
            ardoq_type = next((item for item in layer['ardoq_component_types'].values() if item['name'] == elem_type),
                              False)
            if not ardoq_type:
                continue
            try:
                component = {'description': ev['description'], 'parent': None, 'rootWorkspace': ws_id,
                             'typeId': ardoq_type['id'], 'name': ev['name'], 'archimateID': ev['id']}
                if 'fields' in ev:
                    for f, fv in ev['fields'].items():
                        component[f] = fv
                comp = ardoq.create_component(comp=component)
                id_map[ev['id']] = comp['_id']
            except ArdoqClientException as e:
                logger.debug('error adding component: %s - %s', ev['name'], e)
        else:
            logger.error('could not find element type in config file: %s', ev['type'])
    layer['id_map'] = id_map


def create_ardoq_references(layers, rels, config_items):
    for rk, rv in rels.items():
        source_id = source_ws = None
        target_id = target_ws = None
        ref_id = None
        for lk, lv in layers.items():
            if rv['source'] in lv['id_map'].keys():
                source_id = lv['id_map'][rv['source']]
                source_ws = lv['ws_id']
                for ref_k, ref_v in lv['ardoq_reference_types'].items():
                    if config_items[rv['type'].lower()] == ref_v['name']:
                        ref_id = ref_k
                        break
            if rv['target'] in lv['id_map'].keys():
                target_id = lv['id_map'][rv['target']]
                target_ws = lv['ws_id']
            # find the rel_type number in the source workspace
        logger.debug('creating new ref with %s - %s', rk, ref_id)
        if (ref_id == None):
            continue
        try:
            ref = {'order': 0, 'returnValue': '', 'targetWorkspace': target_ws, 'target': target_id,
                   'source': source_id, 'rootWorkspace': source_ws, 'type': int(ref_id),
                   'description': rv['name'] + '\n' + rv['description']}
            ardoq_ref = ardoq.create_reference(ref=ref)
        except ArdoqClientException as e:
            logger.debug('error adding reference: %s - %s', rv['name'], e)


def create_model_space(model_name, model_descript = None):
    # TODO: check that the modeltype is available....
    '''
    create an ardoq folder for the project and then workspaces for each archimate layer
    :param model_name: name from interchange file
    :param model_descript: text description from interchange file
    :return: dict of layers in ardoq. names and model ids
    '''
    if model_descript is None:
        model_descript = 'folder for the imported archimate model'
    folder = {'name': model_name, 'description': model_descript}
    logger.debug('creating folder for model: %s', folder)
    try:
        f = ardoq.create_folder(folder)
    except ArdoqClientException as e:
        print (e)
    logger.debug('created folder: %s', f)
    #TODO: get this information instead of hardocding
    # TODO: maybe seperate layer for Data?
    global wspaces
    wspaces = {'Business': {'name': 'Business Layer', 'model_id': business_layer_template,
                            'config_name': 'Business'},
               'Application': {'name': 'Application Layer', 'model_id': application_layer_template,
                               'config_name': 'Application'},
               'Technology': {'name': 'Technology Layer', 'model_id': technology_layer_template,
                              'config_name': 'Technologu'},
               'Motivation': {'name': 'Business Motivation', 'model_id': motivation_layer_template,
                              'config_name': 'Motivation'},
               'Implementation': {'name': 'Implementation and Migration', 'model_id': implementation_layer_template,
                                  'config_name': 'Implementation'}}
    views = ["componenttree", "processflow", "reader", "relationships"]
    ws_list = []
    # TODO: include the process and component views in the ws creation
    # TODO: create fields to hold archimate import IDs
    for k, w in wspaces.items():
        logger.debug('create a workspace for %s', w['name'])
        new_workspace = {'description': 'workspace for archimate ' + w['name'], 'componentTemplate': w['model_id'],
                         'name': w['name'], 'folder': f['_id'], 'views': views}
        try:
            workspace = ardoq.create_workspace(new_workspace)
            logger.debug('workspace created: %s', workspace)
            # ws_list.append(workspace['_id'])
            w['ws_id'] = workspace['_id']

            for field, field_value in field_property_map.items():
                if field_value and len(field_value) > 1:
                    logger.debug('Creating field: %s', field_value)
                    # Creating fields for each componentModel.
                    newField = {'model':workspace['componentModel'], 'name': field_value, 'label': field_value, 'type': 'Text', 'global': True,
                    'description': '', 'globalref': False, 'defaultValue': ''}
                    ardoq.create_field(newField)

        except ArdoqClientException as e:
            print (e)
    return wspaces

def property_field_map(doc):
    global field_property_map
    #propertydefs>
    #<propertydef identifier="propid-11" name="" type="string" />
    #<propertydef identifier="propid-12" name="BusinessValue" type="string" />
    if 'propertydefs' in doc:
        if type(doc['propertydefs']['propertydef']) is list:
            for p in doc['propertydefs']['propertydef']:
                print 'Adding property: ' + p['@name']
                field_property_map[p['@identifier']] = p['@name']
        else:
            p = doc['propertydefs']['propertydef']
            print 'Adding property: ' + p['@name']
            field_property_map[p['@identifier']] = p['@name']

def main():
    get_config()
    global ardoq
    ardoq = ArdoqClient(hosturl=config['Ardoq']['host'], token=config['Ardoq']['token'], org=config['Ardoq']['org'])
    with open(config['Archimate']['exchange_file']) as fd:
        doc = xmltodict.parse(fd.read(),  force_list=set('propertydef'))
    model_name = get_tag_name(doc['model']['name'], config['Archimate']['lang'])
    logger.debug('model name: %s', model_name)
    folder_descript = 'archimate import model description'
    if 'metadata' in doc['model'] and 'dc:desciption' in doc['model']['metadata']:
        folder_descript = doc['model']['metadata']['dc:desciption']
    folder = {'name': model_name, 'description': folder_descript}

    property_field_map(doc['model'])
    layers = create_model_space(model_name=model_name, model_descript=folder_descript)



    # TODO: this bit is very inefficient. looping through all elements 3 times.
    # can do it better if the elementtypes were in a dict
    elements = get_archimate_elements(doc['model']['elements']['element'], config.options('Business'))
    logger.debug('got %s business elems', len(elements))
    create_ardoq_components(layers['Business'], elements, config['Business'])
    elements = get_archimate_elements(doc['model']['elements']['element'], config.options('Application'))
    logger.debug('got %s application elems', len(elements))
    create_ardoq_components(layers['Application'], elements, config['Application'])
    elements = get_archimate_elements(doc['model']['elements']['element'], config.options('Technology'))
    logger.debug('got %s technology elems', len(elements))
    create_ardoq_components(layers['Technology'], elements, config['Technology'])
    elements = get_archimate_elements(doc['model']['elements']['element'], config.options('Motivation'))
    logger.debug('got %s motivation elems', len(elements))
    create_ardoq_components(layers['Motivation'], elements, config['Motivation'])
    elements = get_archimate_elements(doc['model']['elements']['element'], config.options('Implementation'))
    logger.debug('got %s implementation elems', len(elements))
    create_ardoq_components(layers['Implementation'], elements, config['Implementation'])
    logger.info('finished creating components')
    relationships = get_archimate_relationships(doc['model']['relationships']['relationship'], config.options('Relationships'))
    create_ardoq_references(layers, relationships, config['Relationships'])
    # TODO create views
    # need to determine the filters needed for particular views
    logger.info('Finished importing archimate model to ardoq')


if __name__ == '__main__':
    main()
