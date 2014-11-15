import xml.etree.ElementTree
import yaml
import svg.path
import re

import numpy
import sympy
import sympy.parsing.sympy_parser
import sympy.abc

identity = sympy.abc.x


def etree_flat_filter(filter_callback, node):
    "Filter nodes of the XML ElementTree with function <filter_callback> and returns an iterator over the positive Node results."
    unexplored = [node]
    
    while unexplored:
        e = unexplored.pop(0)
        if filter_callback(e):
            yield e
        else:
            unexplored.extend( iter(e) )

def etree_extract_path( path_node ):
    "Extract the id, path and transformation id and return them in a tuple"
    node_id = path_node.attrib['id'] if 'id' in path_node.attrib else '<no_id>'
    node_path = path_node.attrib['d'] if 'd' in path_node.attrib else ''
    node_transformation = path_node.attrib['transform'] if 'transform' in path_node.attrib else ''
    return node_id, node_path, node_transformation
    
def make_zone_pair( id, path, transf ):
    "Return a key-value couple, with the id as the key, and a zone as the value."
    return id,   Zone( svg.path.parse_path(path), transf )

class Formula: #Todo, use formulaes than retain their string representation and the variable to be evaluated
    def __init( self, string_represention ):
        pass

class EntityProperty:
    "A property of the game entity, with a value and an update formula."
    def __init__(self, initialValue, updateFormula, propertyType=None):
        propertyType = propertyType or type( initialValue )
        self.set_value( propertyType(initialValue) )
        self.set_update_formula( updateFormula )
    
    def set_value( self, value ):
        self.value = value
    
    def set_update_formula( self, formula ):
        self.update_formula = formula
        self.update_function = sympy.lambdify( sympy.abc.x, formula, 'numpy' )

class Zone:
    "A zone on the world map, with non-negligeable surface area."
    def __init__( self, multiPath, transformation, propertyTable = None, tagTable = None ):
        self.path = multiPath
        self.transformation = transformation
        self.properties = propertyTable if propertyTable != None else {}
        self.tags = tagTable if tagTable != None else {}
        pass
        
    def set_property( self, id, value = None, updateFormula = None ):
        if id not in self.properties:
            value = value if value != None else 0
            updateFormula = updateFormula if updateFormula != None else identity
            self.properties[id] = EntityProperty( value, updateFormula )
        else:
            if value != None:
                self.properties[id].set_value( value )
            if updateFormula != None:
                self.properties[id].set_formula( updateFormula )
            
    def set_properties( self, propertyTable ):
        for id,value in propertyTable.items():
            self.set_property(id,value)
    
    def set_tag( self, id, value ):
        self.tags[id] = value
        
    def set_tags( self, tagTable ):
        for id,value in tagTable.items():
            self.set_tag( id, value )

class World:
    "A game world"
    def __init__(self):
        self._zones = dict()
    
    def parse_and_add( self, svgfilename, yamlfilename ):
        svgtree = xml.etree.ElementTree.parse(svgfilename)
        path_nodes = etree_flat_filter(
                ( lambda node : node.tag.endswith('path') ),
                svgtree.getroot() )
        paths = list( map( etree_extract_path, path_nodes ) )
        _zones = map( lambda triple: make_zone_pair(*triple), paths )
        self._zones.update( _zones )
        with open(yamlfilename) as cfg_file:
            zone_cfgs = yaml.safe_load( cfg_file )
            for zone_cfg in zone_cfgs:
                zone_id = zone_cfg['id']
                zone_tags = zone_cfg['tags']
                zone_properties = zone_cfg['properties']
                self._zones[zone_id].set_properties( zone_properties )
                self._zones[zone_id].set_tags( zone_tags )
                
        return self._zones
    
    def zone_ids(self):
        yield from self._zones.keys()
        
    def zones(self):
        yield from self._zones.items()
    
    DUMMY_ZONE_STRING ="""\
-   id: %s
    tags:
        name: %s
    properties:
        civils: 20000
        soldiers: 1000
"""
    def write_dummy_zone_cfg(self,outputfilename):
        with open( outputfilename, 'w' ) as outfile:
            for id in self.zone_ids():
                print( World.DUMMY_ZONE_STRING % (id,id), file=outfile )

class YamlWriter():
    "Class to write configuration to a configuration file"
    indent_width = 4
    
    def __init__():
        self.indent = 0
