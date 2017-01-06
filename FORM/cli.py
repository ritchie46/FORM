from sympy import pprint

from FORM.form import IterForm
from FORM.parser import Parser


class CLI:
    def __init__(self):
        self.p = None
        self.mean = None
        self.std_dev = None
        self.sol = None
        self.n = 4
        self.result = False
        self.predef_beta = None
        self.options()

    def options(self):
        if self.p is None:
            print("\nWelcome to the FORM command line interface. \nYou will walk through some steps to setup your "
                  "reliability function in the form of z = 'any function'.\n"
                  "The probability of z <= 0 will be computed by First Order Reliability Methods.\n\n"
                  "Gotcha's:\n"
                  "\tαi: Influence of a stochastic value on the probability of total failure.\n"
                  "\tβ: mean / standard deviation, Can be used to determine the probability of a Gaussian distribution."
                  )
            self.z_new()
        print("\nChoose your option:\n"
              "[0] Show result summary of latest iteration.\n"
              "[1] Show output off all iterations.\n"
              "[2] Show αi.\n"
              "[3] Change mean values.\n"
              "[4] Change standard deviation values.\n"
              "[5] Change the reliability function.\n"
              "[6] Plot convergence.\n"
              "[7] Preset reliability index β\n"
              "[8] Quit.")
        opt = int(input())
        if opt == 0:
            print("\nComputing solution ...\n\n")
            self.assign()
            self._compute()
            self.sol.output_by_index(-1, False)
            self.result = True
            self.options()

        elif opt == 1:
            print("\nComputing solution ...\n\n")
            self.assign()
            self._compute()
            self.sol.output()
            self.result = True
            self.options()
        elif opt == 2:
            print("The αi factor shows the influence of a variable on the failure probability.\n"
                  "The shown αi factor is the result after 1 iteration")
            print("\nComputing solution ...\n\n")
            self.assign()
            self._compute(1)
            for i in range(len(self.sol.symbols)):
                print("%s: %s" % (self.sol.symbols[i], self.sol.alpha_i[0][i]))
            self.options()
        elif opt == 3:
            self.mean_new()
            self.options()
        elif opt == 4:
            self.std_dev_new()
            self.options()
        elif opt == 5:
            self.z_new()
            self.options()
        elif opt == 6:
            if self.result:
                self.sol.plot_iterations()
            else:
                print("There is no solution to plot.")
            self.options()
        elif opt == 7:
            self.assign()
            self.predef_beta = float(input("Set β:\n"))
            self.options()
        elif opt == 8:
            quit()
        else:
            print("\nYour chosen option is not valid, please choose an option between 0-7")
            self.options()

    def z_new(self):
        self.p = Parser(input("\nSet your reliability function:\n"))
        print("\nYour function:\n\n The failure function z = \n")
        pprint(self.p.f)
        self.mean_new()
        self.std_dev_new()

    def std_dev_new(self):
        self.std_dev = []
        for symbol in self.p.s:
            self.std_dev.append(float(input("\nSet the standard deviation for %s:\n" % symbol)))

    def mean_new(self):
        self.mean = []
        for symbol in self.p.s:
            self.mean.append(float(input("\nSet the mean value for %s:\n" % symbol)))

    def assign(self):
        self.sol = IterForm(self.p.f, self.p.s, self.mean, self.std_dev)

    def _compute(self, n=20):
        self.sol.predef_beta = self.predef_beta
        try:
            self.sol.iterate(20)
        except TypeError as e:
            print("The following TypeError occured:\n%s\n"
                  "Cannot parse the given formula or your formula led to complex numbers. "
                  "Please check your input." % e)


if __name__ == "__main__":
    CLI()
