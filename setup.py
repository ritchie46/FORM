import sys
from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python 2.x is not supported')

setup(
    name='FORM-cal',
    version="0.2.1",
    description='Taylor series approximation of the performance function of different stochastic variables.',
    author='Ritchie Vink',
    author_email='ritchie46@gmail.com',
    url='http://ritchievink.com',
    license='MIT License',
    packages=['FORM'],
    install_requires=[
        "sympy",
        "matplotlib",
        "scipy",
        "numpy"
    ]
)
