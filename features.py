from gi.repository import GObject as gobject
import re

class Feature( gobject.Object ):
    def __init__( self, value ):
        gobject.Object.__init__( self )
        self._set_value( value )
        
    def _set_value( self, value ):
        self._value = self._build_value( value )
    
    def _build_value( self, value ):
        return value
    
    @property
    def value( self ):
        return self._value
    
    @value.setter
    def value( self, value ):
        if self._value == value:
            return False
        self._set_value( value )
        self.emit( 'mutated', self._value )
        return True
    
    def __str__( self ):
        return str( self.value )
    
    def __repr__( self ):
        return "<Feature %s>" % str(self)
    
    #def do_mutated( self, arg ):
    #    print( 'emit mutated', arg )

class IntegerFeature( Feature ):
    __gsignals__ = {
        'mutated' : ( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (int,))
    }
        
    def __init__( self, value ):
        Feature.__init__( self, value )
        
    def _build_value( self, value ):
        return int(value)
        
        
#class RatioFeature( Feature ):
#    __gsignals__ = {
#        'mutated' : ( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (float,))
#    }
#        
#    def __init__( self, value ):
#        Feature.__init__( self, value )
#        
#    def __str__( self ):
#        return "%s%%" % str( 100*self.value )
#        
#    def _build_value( self, value ):
#        if type(value) == str:
#            return float(value[:-1])/100.0 #could be smarter by shifting the \. in the string
#        else:
#            return float(value)
        
    
class RealFeature( Feature ):
    __gsignals__ = {
        'mutated' : ( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (float,))
    }
        
    def __init__( self, value ):
        Feature.__init__( self, value )
        
    def _build_value( self, value ):
        return float(value)
        

class StringFeature( Feature ):
    __gsignals__ = {
        'mutated' : ( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str,))
    }
        
    def __init__( self, value ):
        Feature.__init__( self, value )
        
    def _build_value( self, value ):
        return str(value)
        
    def __repr__( self ):
        return "<Feature %s>" % repr(self.value)
        

#INTEGER_REGEX = re.compile("^[+-]?[0-9]+$")
#RATIO_REGEX = re.compile("^\+?(100(\.0*)?|([0-9]{1,2})(\.[0-9]*)?|\.[0-9]+)\%$")
#REAL_REGEX = re.compile("^[+-]?([0-9]+\.|\.[0-9]|[0-9])[0-9]*(e[+-]?[0-9]+)?$")
#STRING_REGEX = re.compile("^.*$")
#PARSING_STR_DATA = [
#    #( INTEGER_REGEX , IntegerFeature ),
#    ( RATIO_REGEX , RatioFeature ),
#    #( REAL_REGEX , RealFeature ),
#    ( STRING_REGEX , StringFeature )
#]
PARSING_TYPE_DATA = {
    int : IntegerFeature,
    float : RealFeature,
    str : StringFeature
}
def featurize( yamlValue ):
    #if type( yamlValue ) == str:
    #    for regex, constructor in PARSING_STR_DATA:
    #        if regex.match( yamlValue ):
    #            return constructor( yamlValue )
    #else:
    #    return PARSING_TYPE_DATA[ type(yamlValue) ]( yamlValue)
    #
    #return None
    
    return PARSING_TYPE_DATA[ type(yamlValue) ]( yamlValue)
        

if __name__ == '__main__':
    def on_new_value( emitter, event ):
        print( "--Signal received-- : ", repr(emitter), ";", repr(event) )
    
    i = IntegerFeature( 0 )
    i.connect('mutated', on_new_value)
    i.value = 0
    
    r = RatioFeature( "50%" )
    r.connect('mutated', on_new_value )
    r.value = 0.1
    r.value = "100%"

    s = StringFeature( "lol" )
    s.connect('mutated', on_new_value )
    s.value = "string"


    for s in "1", "hello", "50%", "200%", "6", "3.1415", "Gnosia", "-42":
        print( repr(s), repr(featurize(s) ) )
