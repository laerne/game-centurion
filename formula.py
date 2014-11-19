import numpy, sympy
import sympy.parsing.sympy_parser as sympy_parser

formula_transformations = (
        sympy_parser.factorial_notation,
        sympy_parser.auto_number,
        sympy_parser.convert_xor,
        sympy_parser.function_exponentiation,
        sympy_parser.implicit_multiplication,
        sympy_parser.implicit_application
)
        

class Formula:
    def __init__( self, string_represention ):
        self._text = string_represention
        self._update_formula = updateFormula
        self._update_function = sympy.lambdify( sympy.abc.x, self._update_formula, 'numpy' )

