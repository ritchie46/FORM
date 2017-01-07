from sympy import symbols
from sympy.core import pi

from FORM.form import *

smbl = "f d s"

f, d, s = symbols(smbl)

# average values of the stochastic symbols
average = [290, 30, 100e3]

# standard deviation of the stochastic symbols
sig = [25, 3, 0]

smbl = smbl.split(sep=" ")

# Reliability function
z = pi * d**2 * f / 4 - s

a = IterForm(z, smbl, average, sig)
a.plot_failure_function_2D(
    index_x=1,
    index_y=0,
    range_x=range(12, 48),
)
a.iterate()
a.output()
#
# a.plot_iterations()