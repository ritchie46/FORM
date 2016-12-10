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
        # symbols
        self.s = []
        self._pythonify()
        self._create_symbols()
        # expression
        self.f = parse_expr(self.f)

    def _create_symbols(self):
        sml = re.findall(r'\b[a-z]\b', self.f)

        for s in sml:
            if s not in self.variables.keys():
                # Assign the symbols to the global namespace
                exec("%s = sm.symbols('%s')" % (s, s), globals())
                self.variables[s] = sm.symbols(s)
                self.s.append(s)

    def _pythonify(self):
        # replace all superscript with numbers
        old = [u"\u00B9", u"\u00B2", u"\u00B3", u"\u2074", u"\u2075", u"\u2076", u"\u2077", u"\u2078", u"\u2079", u"\u2070"]
        new = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        for i in range(9):
            self.f = self.f.replace(old[i], new[i])

        # The power sign need to be inserted between the letters and the numbers and insert **
        s1 = re.split(r"[a-zA-Z0-9]\d", self.f)
        s2 = re.findall(r'[a-zA-Z0-9]\d', self.f)

        expr = ""
        count = 0
        for st in s1:
            expr += st

            if count < len(s2):
                expr += s2[count][0] + "**" + s2[count][1]
            count += 1
        self.f = expr
        self.f = self.f.replace('^', '**')


