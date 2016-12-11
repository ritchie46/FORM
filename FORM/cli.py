from sympy import pprint

from FORM.form import IterForm
from FORM.parser import Parser


def cli_start():
    p = Parser(input("\nSet your reliability function:\n"))

    print("\nYour function:\n\n The failure function z = \n")
    pprint(p.fs)

    mean = []
    std_dev = []

    for symbol in p.s:
        mean.append(float(input("\nSet the mean value for %s:\n" % symbol)))
        std_dev.append(float(input("\nSet the standard deviation for %s:\n" % symbol)))

    a = IterForm(p.f, p.s, mean, std_dev)
    a.iterate(int(input("\nHow many iteration should be done? (4 is recommended)\n")))
    a.output()

if __name__ == "__main__":
    cli_start()
