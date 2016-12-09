import unittest
import math

from form import *

smbl = "f d s"

f, d, s = symbols(smbl)

# average values of the stochastic symbols
average = [290, 30, 0]

# standard deviation of the stochastic symbols
sig = [25, 3, 0]

smbl = smbl.split(sep=" ")

# Reliability function
z = pi * d**2 * f / 4 - s

a = IterForm(z, smbl, average, sig)
a.iterate(4)


class FormTest(unittest.TestCase):
    def test_beta(self):
        for i in range(len(a.beta)):
            self.assertTrue(math.isclose(a.beta[i],
                                         [4.59162043183260, 7.33192836812711, 8.73410698874749, 9.38389491801219][i]),
                            "Beta value is not correct.")

if __name__ == '__main__':
    unittest.main()