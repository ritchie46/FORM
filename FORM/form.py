from sympy import diff, pprint
import scipy.stats as stats
import matplotlib.pyplot as plt


class IterForm:
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

        # A predefined beta can be given to search for design values that coincide with the reliability index
        self.predef_beta = None

        # beta: mean / std dev
        self.beta = []
        # alpha_i = part_diff(x) * std dev(x) / std_dev(z)
        self.alpha_i = []
        # new mean value per iteration
        # mean i = mean - alpha_i * beta * std dev
        self.mean_i = [mean]

        # total chance
        self.chance = []

    @property
    def P(self):
        return self.beta[-1]

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
        if self.predef_beta is not None:
            beta = self.predef_beta
        else:
            beta = self.mean_z_evalf[i] / self.std_dev_z_evalf[i]
        self.beta.append(beta)
        self.chance.append(stats.norm.cdf(float(self.beta[i])))

        # determine alpha i and adapt mean values
        self.alpha_i.append([])
        self.mean_i.append([])
        for j in range(len(self.std_dev)):
            self.alpha_i[i].append(self.partial_dev__std_dev[i][j] / self.std_dev_z[i].subs(self.subs_mean[i]).evalf())
            self.mean_i[i + 1].append(self.mean_i[0][j] - self.alpha_i[i][j] * beta * self.std_dev[j])

    def output(self):
        line = 40
        print("\n\nPartial derivatives:\n%s" % ("-" * line))
        for j in range(len(self.symbols)):
            print("Partial derivative to %s:" % self.symbols[j])
            pprint(self.partial_dev[j])

        for i in range(len(self.mean_z)):
            self.output_by_index(i, verbose=True)

    def output_by_index(self, i, verbose=False):
        line = 40
        if verbose:
            print("\n\n\n\nIteration %d.\n%s\n\n"
                  "Total reliability function results:\n"
                  "\tMean z-function:\n" % ((i + 1), "-" * line))
            pprint(self.mean_z[i])

            print("\n\tStd dev z-function:\n")
            pprint(self.std_dev_z[i])
            print("\n\tstd dev z-function floating point value:", self.std_dev_z[i].subs(self.subs_mean[i]).evalf())
        print("\nResults:"
              "\n\n\tDesign point location:\n\t", self.subs_mean[i])
        print("\n\tMean z-function floating point value:", self.mean_z[i].subs(self.subs_mean[i]).evalf())
        print("\n\tSymbols order of αi:\n\t %s" % self.symbols)
        print("\n\tαi: %s" % self.alpha_i[i])
        print("\n\tThe reliability index β: %s" % self.beta[i])
        print("\n\tProbability of z >= 0:\n\t\tP(β): %s" % self.chance[i])
        print("\n\tProbability of z <= 0:\n\t\tP(1 - β): %s" % (1 - self.chance[i]))

    def plot(self):
        x = [0, 1]
        dbeta = [0, self.beta[0]]

        for i in range(1, len(self.beta)):
            dbeta.append(self.beta[i] - self.beta[i - 1])
            x.append(i + 1)
        plt.ylim([0, float(max(self.beta) + 0.5)])
        plt.plot(x, [0] + self.beta)
        plt.plot(x, dbeta)
        plt.show()



