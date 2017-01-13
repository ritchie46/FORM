import random
from sympy import lambdify


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
        self.symbols = _symbols
        self.mean = mean
        self.std_dev = std_dev

    def compute(self, draw, solution_print=True):
        """
        :param draw: (int) Number of draws.
        :param solution_print: (bool) If True, print result
        :return: p: (float) chance of z < 0
        """
        fail = []
        z = lambdify(self.symbols, self.z)

        for _ in range(draw):

            args = []
            for i in range(len(self.mean)):
                args.append(random.normalvariate(self.mean[i], self.std_dev[i]))

            sol = z(*args)
            if sol < 0:
                fail.append(sol)

        p = len(fail) / draw
        if solution_print:
            print("%d/%d" % (len(fail), draw),  p)
        return p


