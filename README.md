# rn7ena_ds5100_montecarlo
Final project for DS5100 F23

Author: Becky Desrosiers
Project title: Monte Carlo Simulator

## Synopsis
The package contains three (3) classes: Die, Game and Analyzer.


### install
After cloning rn7ena_DS5100_montecarlo to your machine, navigate to the directory and run
```
python setup.py install
```

The package is now available for your use in python. Running setup.py should have added `\monte_carlo_simulator-0.1-py3.7.egg` to your sys.path. You can check if it's there by running the following python code:
```
import sys
for p in sys.path: print(p)    # python 3 - use print p for python 2
```



### import
Since there is only one module, the __init__ file of the montecarlo package will also import the montecarlo module. Methods can then be called usind dot notation.

```
import montecarlo
montecarlo.montecarlo.Die(argument)
```
In order to type less, it is recommended to instead import the module directly as `mc`:

```
from montecarlo import montecarlo as mc
mc.Die(argument)
```


Die objects are initialized with a numpy array reflecting the names of their faces (e.g. [1, 2, 3, 4, 5, 6]) for a regular die. A Die object can have as many faces as you wish, and their weights will be automatically set to 1, but the Die can be made unfair using the change_weight method.

