import random
from sympy import symbols, sqrt


class MonteCarlo:
    def __init__(self, z, _symbols, mean, std_dev):
        """
         :param z: (code) Failure function in python/sympy code. Example:
                     pi * d**2 * f / 4 - s
         :param _symbols: (list) Sympy symbols. Example:
                     ['x', 'b', 's']
         :param mean: (list) Mean values variables, corresponding with the symbols.
         :param std_dev: (list) Standard deviation values variables, corresponding with the symbols.
                         If the symbol variables is deterministic, the value is 0.
         """
        # Failure function
        self.z = z

        # Values for the total z-function after iteration (Taylor linearization). Each index is an iteration level.
        self.mean_z = []
        self.std_dev_z = []

    def compute(self, draw):
        for i in range(draw):
            print(random.normalvariate(3, 1))


smbl = "Yw d Yg h R p Ys"
Yw, d, Yg, h, R, p, Ys = symbols(smbl)
# average values of the stochastic symbols
average = [10, 10, 17, 30, 5, 240, 12]

# standard deviation of the stochastic symbols
sig = [0, 0, 5, 3, 0, 10, 0]

smbl = smbl.split(sep=" ")

a = MonteCarlo(
    z=Yw * d + Yg * (h - d - R) - (p - Ys * R),
    _symbols=smbl,
    mean=average,
    std_dev=sig
)
a.compute(200)