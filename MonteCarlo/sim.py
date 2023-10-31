print("Imported module sim.")

import numpy as np
import pandas as pd



class Die:
    '''
    Die class represents a stochastic object with a specified number of faces represented by unique symbols (str or numeric,
    e.g. "H" and "T" for a coin or 1, 2, 3, 4, 5, and 6 for an actual die), each with a weight representing its probability
    of being rolled.

    The object simulates a die (or coin, etc.) by randomly selecting from the faces a specified number of times and returning
    a list of results (e.g. ["H", "H", "T", "H", "T"] for a coin flipped 5x).

    The weights of the faces can be changed to create "unfair" dice.
    '''


    def __init__(self, faces):
        '''
        Purpose:
        Initializes Die object with a specified number of sides (which can represent a coin (2 sides),
        an actual die (6 sides), etc.).

        Inputs:
        faces : numpy array with distinct values representing each face (e.g. array(["Heads", "Tails"])
                for a coin.)

        Outputs:
        Die object with given number of sides and equal weights of 1.0 (a fair coin, die, etc.).
        '''

        # raise TypeError if argument is not a numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError("Die must be initialized with a NumPy array.")
        
        # raise ValueEroor if faces are not unique
        if not len(faces) == len(np.unique(faces)):
            raise ValueError("Duplicate faces.")


        # instantiate object faces array and equal weights
        else:
            self._state = pd.DataFrame({
                "Weight" : np.ones(len(faces))},
                index = faces)
            
            self._state.index.name = "Face"

    def change_weight(self, face, new_weight):
        '''
        Purpose:
        Allows the user to change the weight of a given face to make the die "unfair".

        Inputs:
        face       : str or numeric representation of one of the faces
        new_weight : new weight for that side (e.g. new_weight = 5 would make that face 5x more likely to be rolled
                     if no other faces were changed)

        Outputs:
        None (in-place change of Die object's state attribute)
        '''

        # raise IndexError if the face given is not part of the Die
        if face not in self._state.index:
            raise IndexError("No such face.")
        
        # raise TypeError if weight cannot be interpreted as numeric
        try:
            float(new_weight)
        except:
            raise TypeError("New weight must be numeric")
        
        # change weight
        self._state.loc[face, "Weight"] = new_weight


    def roll(self, times=1):
        '''
        Purpose:
        Simulates rolling the die a given number of times, returning a list of outcomes of the rolls.

        Inputs:
        times : int number of rolls to be recorded

        Outputs:
        outcomes : list of length(times) of the results of the rolls
        '''

        # raise TypeError if times is not an integer
        try:
            int(times)
        except:
            raise TypeError("Argument must be an integer")
        
        # build list with times number of values randomlly chosen from the die, with applied weights, without saving in memory
        return list(np.random.choice(self._state.index, size=times, replace=True, p=self._state["Weight"]/self._state["Weight"].sum()))


    def get_state(self):
        return self._state
        





if __name__ == "__main__":
    a = np.array(["H", "T"])
    print(a)

    d = Die(a)
    d.change_weight("H", 30)
    print(d.roll(100))
    print(d.get_state())