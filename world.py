import xml.etree.ElementTree
import yaml
import svg.path

import helper
import features
import formulas

#TODO remove all sympy references
import sympy
import sympy.abc

identity = sympy.abc.x


#TODO def etree_flat_filter( filter_callback, expand_filter, node ):
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
    "Extract the id, path and transformation and return them in a tuple"
    node_id = path_node.attrib['id'] if 'id' in path_node.attrib else '<no_id>'
    node_path = path_node.attrib['d'] if 'd' in path_node.attrib else ''
    node_transformation = path_node.attrib['transform'] if 'transform' in path_node.attrib else ''
    return node_id, node_path, node_transformation
    
def make_zone_pair( id, path, transf ):
    "Return a key-value couple, with the id as the key, and a zone as the value."
    return id,   Zone( svg.path.parse_path(path), transf )

class EntityProperty:
    "A property of the game entity, with a value and an update formula."
    def __init__( self, initialValue, initialFormula, variableIdentifiers=set() ):
        self.feature = features.featurize( initialValue )
        self.formula = formulas.formulize( initialFormula, variableIdentifiers )
    
    @property
    def value( self ):
        return self.feature.value
    
    @value.setter
    def value( self, value ):
        self.feature.value = value
    
    @property
    def formula( self ):
        return self._formula
    
    @formula.setter
    def formula( self, newFormula ):
        self._formula = newFormula

class EntityTag:
    def __init__( self, initialValue ):
        self.feature = features.featurize( initialValue )
        
    @property
    def value( self ):
        return self.feature.value
    
    @value.setter
    def value( self, value ):
        self.feature.value = value

class Zone:
    "A zone on the world map, with non-negligeable surface area."
    def __init__( self, multiPath, transformation, propertyTable = None, tagTable = None ):
        self.path = multiPath
        self.transformation = transformation
        self._properties = propertyTable if propertyTable != None else {}
        self._tags = tagTable if tagTable != None else {}
        pass
        
    def set_property( self, identifier, value = None, formula = None ):
        if identifier not in self._properties:
            value = value if value != None else 0
            #by default use the identity, that is next(x) = x, where x is the variable with identifier 'identifier'
            formula = formula if formula != None else identifier
            identifiers = set(self._properties.keys()) | { identifier }
            self._properties[identifier] = EntityProperty( value, formula, identifiers )
        else:
            if value != None:
                self._properties[identifier].value = value
            if formula != None:
                self._properties[identifier].formula.set_text( formula, set(self._properties.keys()) )
                #TODO TODO TODO change to a call of the form `self._properties[identifier].formula.reformulate( formula, set(self._properties.keys()) )`
                #So the reformulation is done without erasing the formula object, and without breaking its links
    
    def set_formula( self, identifier, formula ):
        self.set_property( identifier, None, formula )
            
    def set_properties( self, propertyTable ):
        for id,value in propertyTable.items():
            self.set_property(id,value)
            
    def set_formulas( self, formulaTable ):
        for id,formulaText in formulaTable.items():
            self.set_formula( id, formulaText )
        
    def has_property( self, propertyId ):
        return propertyId in self._properties
        
    def get_property( self, propertyId ):
        return self._properties[propertyId].value
            
    def properties( self ):
        yield from self._properties.items()
    
    def set_tag( self, id, value ):
        if id not in self._tags:
            self._tags[id] = EntityTag( value )
        else:
            self._tags[id].value = value
        
    def set_tags( self, tagTable ):
        for id,value in tagTable.items():
            self.set_tag( id, value )

    def has_tag( self, tagId ):
        return tagId in self._tags
        
    def get_tag( self, tagId ):
        return self._tags[tagId].value
        
    def tags( self ):
        yield from self._tags.items()
    
    @property
    def path( self ):
        return self._path
        
    @path.setter
    def path( self, path ):
        self._path = path
            
    @property
    def transformation( self ):
        return self._transformation
        
    @transformation.setter
    def transformation( self, transformation ):
        self._transformation = transformation


class World:
    "A game world"
    def __init__(self):
        self._zones = dict()
    
    def parse_and_add( self, yamlfilename ):
        with open(yamlfilename) as cfg_file:
            zones_cfg = yaml.safe_load( cfg_file )
            
            svgfilename = zones_cfg['map']['file']
            svgfilename = helper.path_relative_to_file_directory( origin=yamlfilename, path=svgfilename )
            svgtree = xml.etree.ElementTree.parse(svgfilename)
            path_nodes = etree_flat_filter( ( lambda node : node.tag.endswith('path') ), svgtree.getroot() )
            paths = list( map( etree_extract_path, path_nodes ) )
            self._zones.update( map( lambda triple: make_zone_pair(*triple), paths ) )
        
            
            zone_default_cfg = zones_cfg['default']
            zone_default_tags = zone_default_cfg['tags']
            zone_default_properties = zone_default_cfg['properties']
            zone_default_formulas = zone_default_cfg['formulas']
        
            zone_cfgs = zones_cfg['zones']
            
            for zone_cfg in zone_cfgs:
                zone_id = zone_cfg['id']
                
                zone_tags = zone_cfg['tags'] if 'tags' in zone_cfg else {}
                self._zones[zone_id].set_tags( zone_default_tags )
                self._zones[zone_id].set_tags( zone_tags )
                
                zone_properties = zone_cfg['properties'] if 'properties' in zone_cfg else {}
                self._zones[zone_id].set_properties( zone_default_properties )
                self._zones[zone_id].set_properties( zone_properties )
                
                zone_formulas = zone_cfg['formulas'] if 'formulas' in zone_cfg else {}
                self._zones[zone_id].set_formulas( zone_default_formulas )
                self._zones[zone_id].set_formulas( zone_formulas )
                
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
    formulas:
        civils: civils * 0.99 + ( civils + soldiers ) * 0.05
        soldiers: soldiers + civils * 0.01
    deductions:
        population: civils + soldiers
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
