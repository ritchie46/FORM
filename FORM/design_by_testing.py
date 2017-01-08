from scipy.stats import t
import numpy as np

"""
R = m + u * s

R = resistance
m = mean
u = variable in the normal distribution, commonly used is β or x.
s = standard deviation

R in student t distribution:
R = m - s * tn-1 * √(1 + 1/n)

tn-1 = correction if s is unknown
√(1 + 1/n) = correction if m is unknown

"""

"""
mean and standard deviation can be computed from n measurements. In these cases the values are not deterministic and
should be set to False. If they are given they should be set to the give value.
"""
mean_set = False
std_dev_set = 15

# chance
p = 0.05

# measurements
values = [88, 95, 117]
n = len(values)


mean = mean_set if mean_set else np.mean(values)
std_dev = std_dev_set if std_dev_set else np.std(values)

print("Mean: ", mean, "\nStandard deviation: ", std_dev)

if not std_dev_set:
    # tn-1 (student t distribution)
    #c1 = t.ppf(1 - p, n)
    c1 = t.ppf(0.05, n)
    print("\nCorrection due to uncertainty of the standard deviation:\ntn-1 = %f" % c1)
else:
    c1 = -1

if not mean_set:
    # √(1 + 1/n)
    c2 = (1 + 1 / n) ** 0.5
    print("\nCorrection due to uncertainty of the mean:\n√(1 + 1/n) = %f" % c2)
else:
    c2 = 1

R = mean + std_dev * c1 * c2
print("\nR = %f" % R)