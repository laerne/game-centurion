import numpy, sympy
import sympy.parsing.sympy_parser as sympy_parser

FORMULA_TRANSFORMATIONS = (
        sympy_parser.factorial_notation,
        sympy_parser.auto_number,
        sympy_parser.convert_xor,
        sympy_parser.function_exponentiation,
        #sympy_parser.implicit_multiplication,
        #sympy_parser.implicit_application,
)
        

class Formula:
    def __init__( self, string_represention, variableNameTable ):
        self._text = string_represention
        symbols = dict( map( lambda n: (n,sympy.Symbol(n)), variableNameTable ) )
        self._formula = sympy_parser.parse_expr( string_represention, local_dict=symbols, transformations = FORMULA_TRANSFORMATIONS )
        used_symbols = self._formula.atoms(sympy.Symbol)
        self._used_symbols_names = set( map( lambda x : x.name, used_symbols ) )
        self._function = sympy.lambdify( used_symbols, self._formula, 'numpy' )
    
    def evaluate( self, **closure ):
        variables={}
        for name in self._used_symbols_names:
            variables[name] = closure[name]
        return self._function( **variables )
       

