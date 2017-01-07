# FORM
Compute the probability that a non linear reliability function with stochastic variables will get result <= 0.

Installation:
```$ python3 setup.py install```

Run
```python
>>> from FORM.cli import CLI
>>> CLI()
```

## Example
Consider the following construction.
![](https://github.com/ritchie46/FORM/blob/master/res/Selection_001.png?raw=true)

The failure function can be described with:
![](https://raw.githubusercontent.com/ritchie46/FORM/master/res/Selection_002.png)

Assume that te stochastic variables have the following values:

| variable   | mean     | standard deviation |
| ---------- | -------- |------------------- |
| d          | 30       | 3                  |
| f          | 290      | 35                 |
| s          | 100,000  | 7,500              |

Below is the probability contour plot shown. We are computing the probability of the meshed area.

P(Z < 0)

![](https://github.com/ritchie46/FORM/blob/master/res/Selection_004.png?raw=true)


```python
Welcome to the FORM command line interface.
You will walk through some steps to setup your reliability function in the form of z = 'any function'.
The probability of z <= 0 will be computed by First Order Reliability Methods.

Gotcha's:
	αi: Influence of a stochastic value on the probability of total failure.
	β: mean / standard deviation, Can be used to determine the probability of a Gaussian distribution.

Set your reliability function:
pi * d² * f / 4 - s

Your function:

 The failure function z =

   2
π⋅d ⋅f
────── - s
  4

Set the mean value for d:
30

Set the mean value for f:
290

Set the mean value for s:
100e3

Set the standard deviation for d:
3

Set the standard deviation for f:
35

Set the standard deviation for s:
7500

Choose your option:
[0] Show result summary of latest iteration.
[1] Show output off all iterations.
[2] Show αi.
[3] Change mean values.
[4] Change standard deviation values.
[5] Change the reliability function.
[6] Plot convergence.
[7] Preset reliability index β
[8] Quit.
0

Computing solution ...




Results:

	Design point location:
	 {'s': 104687.089069978, 'f': 246.681165512765, 'd': 23.2452181058089}

	αi:
	{'s': -0.236340529999135, 'f': 0.468060635918737, 'd': 0.851505957103692}

	The reliability index β: 2.64425530490390

	Probability of z >= 0:
		P(β): 0.99590645609

	Probability of z <= 0:
		P(1 - β): 0.00409354390967
```

Besides the information of the failure probability is the influences of the variables known. As can be seen in the
example above the αi values are a measure for the influence of the variables.

The diameter d has an αi of 0.85. Showing that reducing the standard deviation of the diameter would result in highest
safety increase.