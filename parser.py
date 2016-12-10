import sympy as sm
from sympy.parsing.sympy_parser import parse_expr
from sympy.functions import *
import re


class Parser:
    def __init__(self, formula):
        """
        :param formula: (str)
        """
        self.f = formula
        self.variables = {}
        self._create_symbols()
        self._pythonify()
        self.f = parse_expr(self.f)

    def _create_symbols(self):
        sml = re.findall(r'\b[a-z]\b', self.f)

        for s in sml:
            # Assign the symbols to the global namespace
            exec("%s = sm.symbols('%s')" % (s, s), globals())
            self.variables[s] = sm.symbols(s)

    def _pythonify(self):
        self.f = self.f.replace('^', '**')

