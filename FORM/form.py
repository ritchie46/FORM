from sympy import diff, pprint, solve
import scipy.stats as stats
import matplotlib.pyplot as plt
import math


class IterForm:
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

    def iterate(self, n=20):
        """
        Determine the partial derivatives per iteration. The iterations stop when beta is getting constant.
        :param n: (int) Amount of iterations.
        """
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

            if i > 1 and math.isclose(self.beta[i], self.beta[i - 1]):
                break

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
        print("Partial derivatives:\n%s" % ("-" * line))
        for j in range(len(self.symbols)):
            print("Partial derivative to %s:" % self.symbols[j])
            pprint(self.partial_dev[j])

        print("\n\nInput:\n%s\nMean values:\n" % ("-" * line),
              dict(zip(self.symbols, self.mean)),
              "\nStandard deviation values:\n",
              dict(zip(self.symbols, self.std_dev)))

        for i in range(len(self.mean_z)):
            self.output_by_index(i, verbose=True)

    def output_by_index(self, i, verbose=False):
        line = 40
        if verbose:
            print("\n\n\n\nIteration %d.\n%s\n\n"
                  "Total reliability function results:\n"
                  "\tMean z-function:\n" % ((i + 1), "-" * line))
            pprint(self.mean_z[i])
            print("\n\tMean z-function floating point value:", self.mean_z[i].subs(self.subs_mean[i]).evalf())

            print("\n\tStd dev z-function:\n")
            pprint(self.std_dev_z[i])
            print("\n\tstd dev z-function floating point value:", self.std_dev_z[i].subs(self.subs_mean[i]).evalf())

        print("\n\nResults:"
              "\n\n\tDesign point location:\n\t", self.subs_mean[i])

        print("\n\tαi:\n\t%s" % dict(zip(self.symbols, self.alpha_i[i])))
        print("\n\tThe reliability index β: %s" % self.beta[i])
        print("\n\tProbability of z >= 0:\n\t\tP(β): %s" % self.chance[i])
        print("\n\tProbability of z <= 0:\n\t\tP(1 - β): %s" % (1 - self.chance[i]))

    def plot_iterations(self):
        x = [0, 1]
        dbeta = [0, self.beta[0]]

        for i in range(1, len(self.beta)):
            dbeta.append(self.beta[i] - self.beta[i - 1])
            x.append(i + 1)
        plt.ylim([0, float(max(self.beta) + 0.5)])
        plt.plot(x, [0] + self.beta)
        plt.plot(x, dbeta)
        plt.show()

    def plot_failure_function_2D(self, index_x, index_y, range_x, offset_scale=1):
        """
        Plot is only possible with two stochastic variables.
        :param index_x: (list) Index of of the stochastic variable in the mean and std. deviation list.
        :param index_y: (list) Index of of the stochastic variable in the mean and std. deviation list.
        :param range_x: (range) Range to plot.
        :param offset_scale: (float) Set the scale of the offset to create distinction with failure and non failure side.
        """

        smbl_x = self.symbols[index_x]
        smbl_y = self.symbols[index_y]
        print("x = ", smbl_x, "\ny = ", smbl_y)

        # Determine the y value that belongs to z = 0 and x = variable.
        # substitute the mean values and create a substitution dict.
        mean = list(self.mean)
        symbols = list(self.symbols)
        # The value of y should not be included as it needs te be solved.
        del mean[index_y]
        del symbols[index_y]
        sub = dict(zip(symbols, mean))

        # Determine the y values
        y = []
        y_fail = []
        y_no_fail = []
        for x in range_x:
            if x == 0:
                x += 0.01
            # Update x
            sub[smbl_x] = x
            y.append(solve(self.z.subs(sub), smbl_y)[0])

        offset = max(y) * offset_scale
        z_fail = self.z + offset
        z_no_fail = self.z - offset

        for x in range_x:
            if x == 0:
                x += 0.01
            # Update x
            sub[smbl_x] = x
            y_fail.append(solve(z_fail.subs(sub), smbl_y)[0])
            y_no_fail.append(solve(z_no_fail.subs(sub), smbl_y)[0])

        plt.xlabel("variable: " + smbl_x)
        plt.ylabel("variable: " + smbl_y)
        plt.plot(range_x, y, label="z = 0", color="blue")
        plt.plot(range_x, y_fail, label="fail_side", color="red")
        plt.plot(range_x, y_no_fail, label="no_fail_side", color="green")
        plt.legend()
        plt.show()





