import numpy, sympy
import sympy.parsing.sympy_parser as sympy_parser
from gi.repository import GObject as gobject

FORMULA_TRANSFORMATIONS = (
        sympy_parser.factorial_notation,
        sympy_parser.auto_number,
        sympy_parser.convert_xor,
        sympy_parser.function_exponentiation,
        #sympy_parser.implicit_multiplication,
        #sympy_parser.implicit_application,
)
        

class Formula( gobject.Object ):
    __gsignals__ = {
        'mutated' : ( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str,))
    }
        
    def __init__( self, stringRepresentation, variableNameTable ):
        gobject.Object.__init__( self )
        self._text = None
        self.set_text( stringRepresentation, variableNameTable )
    
    def evaluate( self, **closure ):
        variables={}
        for name in self._used_symbols_names:
            variables[name] = closure[name]
        return self._function( **variables )
        
    @property
    def formula( self ):
        return self._formula
    
    @property
    def text( self ):
        return self._text
        
    def set_text( self, stringRepresentation, variableNameTable ):
        oldStringRepresentation = self._text
        if oldStringRepresentation == stringRepresentation :
            return False
            
        self._text = stringRepresentation
        symbols = dict( map( lambda n: (n,sympy.Symbol(n)), variableNameTable ) )
        
        # TODO a try-catch
        self._formula = sympy_parser.parse_expr( stringRepresentation, local_dict=symbols, transformations = FORMULA_TRANSFORMATIONS )
        
        used_symbols = self._formula.atoms(sympy.Symbol)
        self._used_symbols_names = set( map( lambda x : x.name, used_symbols ) )
        self._function = sympy.lambdify( used_symbols, self._formula, 'numpy' )
        
        self.emit( 'mutated', self._text )
        return True
        
    
    @property
    def function( self ):
        return self._function
    
    def __str__( self ):
        return self.formula
       
def formulize( yamlValue, identifiers ):
    #TODO how to pass the variable table name ?
    return Formula( str(yamlValue), identifiers )
