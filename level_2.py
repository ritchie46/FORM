from sympy import symbols, pi, diff, pprint
import math

smbl = "f d s"

f, d, s = symbols(smbl)

# average values of the stochastic symbols
average = [290, 30, 100e3]

# standard deviation of the stochastic symbols
sig = [25, 3, 0]

smbl = smbl.split(sep=" ")

z = pi * d**2 * f / 4 - s


class Level2Prob:
    def __init__(self, z, _symbols, mean, std_dev):
        # Failure function
        self.z = z

        # Values for the total z-function after iteration (Taylor linearization). Each index is an iteration level.
        self.mean_z = []
        self.std_dev_z = []
        # evaluated floating point values
        self.mean_z_evalf = []
        self.std_dev_z_evalf = []

        self.symbols = _symbols
        self.partial_dev = []
        self.mean = mean
        self.std_dev = std_dev

        # Values for the stochastic variables after iteration (Taylor linearization). Each index is an iteration level.
        # [[f, d, x], [f*, d*, x*]]
        #   iter 1        iter 2
        self.mean_var = []
        self.std_dev_var = []

        self.prev_design_average = mean
        self.prev_design_std_dev = std_dev

        # subs dict for sympy
        self.subs_mean = []

        # part_diff * std dev
        self.partial_dev__std_dev = []

        # beta: mean / std dev
        self.beta = []
        # alpha_i = part_diff(x) * std dev(x) / std_dev(z)
        self.alpha_i = []
        # new mean value per iteration
        # mean i = mean - alpha_i * beta * std dev
        self.mean_i = [mean]

    def det_partial_dev(self):
        for variable in self.symbols:
            self.partial_dev.append(diff(self.z, variable))

    def iterate(self, n):
        self.det_partial_dev()
        for i in range(n):
            # append substitution dict.
            self.subs_mean.append({})

            # First iteration the substituted values are the original values
            for j in range(len(self.symbols)):
                self.subs_mean[i][self.symbols[j]] = self.mean_i[i][j]

            # Apply the mean linearization
            # mean of the total z-function
            self.mean_z.append(self.z)
            # (mean0 - mean_previous_iteration) * partial derivative mean variable
            for j in range(len(self.mean)):
                self.mean_z[i] += (self.mean[j] - self.mean_i[i][j]) * self.partial_dev[j]

            # Apply the standard deviation linearization (only if there is no covariance)
            # std dev of the total z-function
            self.std_dev_z.append(0)
            self.std_dev_var.append([])
            self.partial_dev__std_dev.append([])
            # (partial derivative std_dev_variable)² * std_dev_variable²
            for j in range(len(self.std_dev)):
                self.std_dev_var[i].append(
                        # function                 # number (constant)
                    self.partial_dev[j]**2 * self.std_dev[j]**2
                )
                self.std_dev_z[i] += self.std_dev_var[i][j]

                self.partial_dev__std_dev[i].append(
                    (self.partial_dev[j] * self.std_dev[j]).subs(self.subs_mean[i]).evalf()
                )

            self.std_dev_z[i] **= 0.5

            # floating point values
            self.mean_z_evalf.append(self.mean_z[i].subs(self.subs_mean[i]).evalf())
            self.std_dev_z_evalf.append(self.std_dev_z[i].subs(self.subs_mean[i]).evalf())
            self._update_mean(i)

    def _update_mean(self, i):
        """
        The results of every iterations are determined to adapt the input for the next iteration.
        """
        self.beta.append(self.mean_z_evalf[i] / self.std_dev_z_evalf[i])

        # determine alpha i and adapt mean values
        self.alpha_i.append([])
        self.mean_i.append([])
        for j in range(len(self.std_dev)):
            self.alpha_i[i].append(self.partial_dev__std_dev[i][j] / self.std_dev_z[i].subs(self.subs_mean[i]).evalf())
            self.mean_i[i + 1].append(self.mean_i[0][j] - self.alpha_i[i][j] * self.beta[i] * self.std_dev[j])

    def output(self):
        line = 40
        line_small = 20
        print("\n\nPartial derivatives:\n%s" % ("-" * line))
        for j in range(len(self.symbols)):
            print("variable %s" % self.symbols[j])
            pprint(self.partial_dev[j])

        for i in range(len(self.mean_z)):
            print("\n\nIteration %d.\n%s\n\nmean z-function:\n" % ((i + 1), "-" * line_small))
            pprint(self.mean_z[i])

            print("\nMean variables\n%s\n" % ("-" * line), self.subs_mean[i])
            print("\nmean z-function value:", self.mean_z[i].subs(self.subs_mean[i]).evalf())

            print("\nstd dev z-function:\n")
            pprint(self.std_dev_z[i])
            print("\nstd dev z-function value:", self.std_dev_z[i].subs(self.subs_mean[i]).evalf())

            print("\n\nBeta: %s" % self.beta[i])
            print("\nalpha i: %s" % self.alpha_i[i])


a = Level2Prob(z, smbl, average, sig)
a.iterate(5)
a.output()

