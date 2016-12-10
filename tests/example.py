from form import *
from sympy import symbols
from sympy.core import pi

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
a.output()

print(a.beta)