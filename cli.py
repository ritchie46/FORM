from sympy import init_printing, pprint
from parser import Parser
from form import IterForm
init_printing(latex_mode=True)

p = Parser(input("\nSet your reliability function:\n"))

print("\nYour function:\nz =")
pprint(p.f)

mean = []
std_dev = []

for symbol in p.s:
    mean.append(float(input("\nSet the mean value for %s:\n" % symbol)))
    std_dev.append(float(input("\nSet the standard deviation for %s:\n" % symbol)))


a = IterForm(p.f, p.s, mean, std_dev)
a.iterate(int(input("\nHow many iteration should be done? (4 is recommended)\n")))
a.output()
