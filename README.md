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
## 1       T  T  T
## 2       T  T  H
## 3       H  H  T
## 4       H  H  H
## 5       H  H  T

```

Notice how there are many more heads than tails because we weighted the "H" face!

If you find a need, you can also access the Die objects with the `get_dice` method, which will return a list of the Die objects that the Game was instantiated with.
```
for d in game1.get_dice():
  print(d.get_state())

## Output
##       Weight
## Face
## H        2.0
## T        1.0
##       Weight
## Face
## H        2.0
## T        1.0
##       Weight
## Face
## H        2.0
## T        1.0
```


#### Analyzer
The Analyzer class has a few methods which will display some facts about a Game. An Analyzer object is initialized with a Game object as an argument, which can be accessed with the `get_game` method.
```
a = mc.Analyzer(game1)
print(a.get_game().get_last_play())

## Output
## Die #   1  2  3
## Roll #
## 1       T  T  T
## 2       T  T  H
## 3       H  H  T
## 4       H  H  H
## 5       H  H  T

```

The Analyzer will tell you how many times you hit the jackpot (rolled all of the same faces in a single roll), how many times each face was rolled in each roll, and how many distinct combinations and permutations were rolled along with their counts.
```
print("Jackpots:", a.jackpot(), sep ="")
print("\nFace counts: \n", a.face_counts(), sep ="")
print("\nCombos: \n", a.combo_counts(), sep ="")
print("\nPermutations: \n", a.perm_counts(), sep ="")

## Output
## Jackpots: 2
##
## Face counts:
##    T  H
## 1  3  0
## 2  2  1
## 3  1  2
## 4  0  3
## 5  1  2
##
## Combos:
##        Counts
## T T T       1
## H T T       1
##   H T       2
##     H       1
##
## Permutations:
##        Counts
## T T T       1
##     H       1
## H H T       2
##     H       1
```

## API description
NAME
    montecarlo.montecarlo

CLASSES
    builtins.object
        Analyzer
        Die
        Game

### Analyzer

`class Analyzer(builtins.object)`

An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.

METHODS

`__init__(self, game)`

__Purpose:__

Initializes Analyzer object with a given game.

__Inputs:__

game : Game object to be analyzed.

__Outputs:__

Analyzer object with the given Game.

`combo_counts(self)`

__Purpose:__

Computes distinct combinations (regardless of order) of faces rolled and reports them along with their counts in a pandas data frame. Distinct combinations are described in a Multiindex with a single column of counts.

__Inputs:__

None.

__Outputs:__

combos : pandas data frame of all distinct combinations and their counts.

`face_counts(self)`

__Purpose:__

Computes how many times each face is rolled for each roll in a game, returning a data frame describing the faces rolled in the Game.

__Inputs:__

None.

__Outputs:__

face_counts : pandas DataFrame describing the faces rolled in the Game, with index Roll # and face values as columns.

`get_game(self)`

__Purpose:__

Safely retrieve a copy of the Game object that the Analyzer was initialized with.

__Inputs:__

None.

__Outputs:__

Game object the Analyzer was initialized with.

`jackpot(self)`

__Purpose:__

Computes the number of times all Die objects 'rolled' the same face in a single roll, returning an integer value.

__Inputs:__

None.

__Outputs:__

jackpots : int representing number of times all dice rolled the same face.

`perm_counts(self)`

__Purpose:__

Computes the distinct (ordered) permutations of faces rolled and reports them along with their counts in a pandas data frame. Distinct combinations are described in a multiindex with a single column of counts.
     
__Inputs:__

None.

__Outputs:__

perms : pandas data frame of all distinct permutations and their counts.


### Die

`class Die(builtins.object)`

A Die object represents a stochastic object with a specified number of faces represented by unique symbols (str or numeric, e.g. "H" and "T" for a coin or 1, 2, 3, 4, 5, and 6 for an actual die), each with a weight representing its probability of being rolled. The object simulates a die (or coin, etc.) by randomly selecting from the faces a specified number of times and returning a list of results (e.g. ["H", "H", "T", "H", "T"] for a coin flipped 5x). The weights of the faces can be changed to create "unfair" dice.

METHODS
`__init__(self, faces)`

__Purpose:__

Initializes Die object with a specified number of sides (which can represent a coin (2 sides), an actual die (6 sides), etc.).

__Inputs:__

faces : numpy array with distinct values representing each face (e.g. array(["Heads", "Tails"]) for a coin.)

__Outputs:__

Die object with given number of sides and equal weights of 1.0 (a fair coin, die, etc.).

`change_weight(self, face, new_weight)`

__Purpose:__

Allows the user to change the weight of a given face to make the die "unfair".

__Inputs:__

face       : str or numeric representation of one of the faces
new_weight : new weight for that side (e.g. new_weight = 5 would make that face 5x more likely to be rolled if no other faces were changed)

__Outputs:__

None (in-place change of Die object's state attribute)

`get_state(self)`

__Purpose:__

Safely access the state object of the Die, which holds the names and weights of each face in a pandas data frame.

__Inputs:__

None.

__Outputs:__

state: pandas data frame with names and weights of each face of the Die object.

`roll(self, times=1)`

__Purpose:__

Simulates rolling the die a given number of times, returning a list of outcomes of the rolls.

__Inputs:__

times : int number of rolls to be recorded

__Outputs:__

outcomes : list of length(times) of the results of the rolls

### Game

`class Game(builtins.object)`

Game object takes one or more dice (of the Die class) with the same number and names of faces and simulates rolling them.

METHODS
`__init__(self, dice)`

__Purpose:__

Initializes a Game object with a given list of dice.

__Inputs:__

dice : list of Die objects with the same number and labels of faces.

__Outputs:__

Game object with the given dice.

`get_dice(self)`
     
__Purpose:__

Safely retrieve list of Die objects stored in the Game.

__Inputs:__

None.

__Outputs:__

dice : list of Die objects that the Gmae was instantiated with

`get_last_play(self, format='wide')`

__Purpose:__

Safely retrieve information on the last game played.
     
__Inputs:__

format : string "wide" or "narrow" to desribe the shape of the dataframe returned. "wide" or "w" will return the dataframe with row indexes representing Roll # and columns representing Die #. "narrow" or "n" will return the dataframe multi-indexed with level 1 representing Roll # and level 2 representing Die #.
     
__Outputs:__

last_play : pandas dataframe with results from the last game, in wide or narrow format as specified. Defaults to wide.

`play(self, times=1)`

__Purpose:__

Simulate gameplay by getting results of a given number of rolls of the dice in the Game. Results are returned and stored in the Game object, retrievable with the get_last_play() method. Only the most recent play is recorded; play history is lost.

__Inputs:__

times : int number of rolls in the game. Defaults to 1.

__Outputs:__

results : pandas dataframe of the results of times rolls of the game's dice.
