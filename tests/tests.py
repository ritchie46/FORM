import math
import unittest

from sympy import symbols, pi

from FORM.form import *
from FORM.parser import Parser


class FormTest(unittest.TestCase):
    def test_beta(self):
        smbl = "f d s"

        f, d, s = symbols(smbl)

        # average values of the stochastic symbols
        average = [290, 30, 100e3]

        # standard deviation of the stochastic symbols
        sig = [25, 3, 0]

        smbl = smbl.split(sep=" ")

        # Reliability function
        z = pi * d ** 2 * f / 4 - s

        a = IterForm(z, smbl, average, sig)
        a.iterate(4)
        for i in range(len(a.beta)):
            self.assertTrue(math.isclose(a.beta[i],
                                         [2.35168452829880, 2.85290452651544, 2.87229325859207, 2.87221319115248][i]),
                            "Beta value is not correct.")

    def test_parser(self):
        a = Parser("pi * d² * f / 4 - s * cot(x)")
        self.assertEqual(str(a.f), "pi*d**2*f/4 - s*cot(x)", "_pythonify function")
        self.assertRegex(str(a.variables), r'[d]|[f]|[s]|[x]|[^a-zA-Z]', "_create_symbols function")


if __name__ == '__main__':
    unittest.main()