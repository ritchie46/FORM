from sympy import symbols, sqrt
from FORM.form import *

smbl = "x b s"

x, b, s = symbols(smbl)

# average values of the stochastic symbols
average = [100, 1, 40]

# standard deviation of the stochastic symbols
sig = [5, 0.2, 5]

smbl = smbl.split(sep=" ")

# Reliability function
z = b - s + sqrt(x)

a = IterForm(z, smbl, average, sig)
a.iterate()
a.output()
a.plot_iterations()