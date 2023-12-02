# rn7ena_ds5100_montecarlo
Final project for DS5100 F23

Author: Becky Desrosiers
Project title: Monte Carlo Simulator

## Synopsis

### install
It is recommended to clone this repo into a directory in sys.path. To checkc which directories are in sys.path, run the following python code:
```
import sys
for p in sys.path: print(p)    # or print p for python 2
```

After cloning this repo to your machine, navigate into rn7ena_DS5100_montecarlo and run
```
python setup.py install
```

The package is now available for your use in python.


### import
Since there is only one module, the __init__ file of the montecarlo package will also import the montecarlo module. Methods can then be called using dot notation.

```
import montecarlo
# montecarlo.montecarlo.Die(argument) will work
```

To save time typing, you can also import the module directly witih a nickname, e.g. `mc`:
```
from montecarlo import montecarlo as mc
# mc.Die(argument) will work
```

### Using the module

#### Die
Die objects are initialized with a numpy array reflecting the names of their faces (e.g. [1, 2, 3, 4, 5, 6]) for a regular die. A Die object can have as many faces as you wish, and their weights will be automatically set to 1. Faces and weights can be retrieved with the `get_state` method.
```
array = np.array(["H", "T"])  # represents a coin
coin = mc.Die(array)
print(coin.get_state())

## Output
##       Weight
## Face
## H        1.0
## T        1.0
```

The Die can be made unfair by setting new weights. In this example, I set the face "H" to weight 2, so it will be twice as likely to roll as "T".
```
coin.change_weight("H", 2)
print(coin.get_state())

## Output
##       Weight
## Face
## H        2.0
## T        1.0
```

Simulate rolling the Die (or flipping the coin, etc.) with the `rol`l method by specifying the number of times you want to roll. The results will be displayed in a list but not stored in the Die object.

```
print(coin.roll(10))

## Output
## ['T', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
```


#### Game
A Game object is initialized with a list of Die objects which all must have the same faces, though the weights can be different. The Game simulates rolling the set of "dice" a specified number of times with the `play` method. The `play` method returns the data frame and also stores it as an attribute, which can be accessed with `get_last_play()`

```
game1 = mc.Game([coin, coin, coin])    # Game with 3 coins
game1.play(5)                          # 5 flips
print(game1.get_last_play())

## Output
## Die #   1  2  3
## Roll #
## 1       H  T  H
## 2       H  T  H
## 3       H  H  H
## 4       H  H  H
## 5       H  H  H
```

Notice how there are many more heads than tails because we weighted the "H" face!




