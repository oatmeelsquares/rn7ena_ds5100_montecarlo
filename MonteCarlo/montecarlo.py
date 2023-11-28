print("Imported module sim.")

import numpy as np
import pandas as pd


######################################################################################################################
###### Die ###########################################################################################################
######################################################################################################################

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
            raise TypeError("Argument must be an integer.")
        
        # return a list with times number of values randomlly chosen from the die, with applied weights, without saving in memory
        return list(np.random.choice(self._state.index, size=times, replace=True, p=self._state["Weight"]/self._state["Weight"].sum()))


    def get_state(self):
        '''
        Purpose:
        Safely access the state object of the Die, which holds the names and weights of each face in a pandas data frame.

        Inputs:
        None.

        Outputs:
        state: pandas data frame with names and weights of each face of the Die object.
        '''
        return self._state
        





######################################################################################################################
###### Game ##########################################################################################################
######################################################################################################################

class Game():
    '''
    Game class represents rolling one or more dice (of the Die class) with the same number and names of faces.  
    '''


    def __init__(self, dice):
        '''
        Purpose:
        Instantiates a Game object with a given list of dice.

        Inputs:
        dice : list of Die objects with the same number and labels of faces.

        Outputs:
        Game object with the given dice.        
        '''

        # raise TypeError if the object passed to the initializer is not a list
        if not isinstance(dice, list):
            raise TypeError("Game object must be instantiated with a list.")
        

        for die in dice:
            # raise TypeError if any element of the list is not a Die object
            if not isinstance(die, Die): raise TypeError("Game object must be instantiated with a list of Die objects.")

            # verify the list components are similar dice
            faces = dice[0].get_state().index               # this Index object should hold the same values for every Die in the list
                                                            # This variable will be assigned for each iteration but I think it's worth
                                                            # it for code clarity and it saves me from having to iterate through the
                                                            # list of dice two times
            for i in range(0, len(faces)):
                # raise ValueError if any Die in the list has a different index values
                if die.get_state().index[i] != faces[i]: raise ValueError("Dice must be similar (same number and names of faces).")

        self._dice = dice
        self._last_play = None


    def get_dice(self):
        '''
        Purpose:
        Safely retrieve list of Die objects stored in the Game.

        Inputs:
        format : string "wide" or "narrow" to desribe the shape of the dataframe returned.
                 "wide" will return the dataframe with row indexes representing # of the roll and columns representing # of the Die.
                 "narrow" will return the dataframe multi-indexed with level 1

        Outputs:
        dice : list of Die objects that the Gmae was instantiated with
        '''

        return self._dice
    

    def get_last_play(self, format = "wide"):
        '''
        Purpose:
        Safely retrieve information on the last game played.

        Inputs:
        None.

        Outputs:
        last_play : pandas dataframe with results from the last game.        
        '''

        return self._last_play


    def play(self, times=1):
        '''
        Purpose:
        Simulate gameplay by getting results of a given number of rolls of the dice in the Game. Results are returned and stored in
        the Game object, retrievable with the get_last_play() method. Only the most recent play is recorded; play history is lost.

        Inputs:
        times : int number of rolls in the game. Defaults to 1.

        Outputs:
        results : pandas dataframe of the results of times rolls of the game's dice.        
        '''

        # Raise TypeError if passed a noninteger argument
        if not isinstance(times, int): raise TypeError("Argument must be an integer.")

        # Raise ValueError if passed times < 1
        if times < 1: raise ValueError("Argument must be a positive integer.")

        results = pd.DataFrame([d.roll(times) for d in self._dice])

        # Format the data frame the way we want it
        results = results.transpose(copy = False)
        
        # Set indexes to start at 1
        r, c = results.shape
        results.index = [i + 1 for i in range(0, r)]
        results.columns = [i + 1 for i in range(0, c)]

        # Name indexes appropriately
        results.index.name = "Roll #"
        results.columns.name = "Die #"

        # Update last_play and return results
        self._last_play = results
        return results



    












######################################################################################################################


if __name__ == "__main__":
    a = np.array(["H", "T"])
    print(a)

    c = Die(a)

    g = Game([c])

    print("State:", g.get_dice()[0].get_state())
    print("Play:")
    print(g.play(5))
    
    df = g.play(100000)
    df.to_csv("~/School/MSDS/DS5100/h-t.csv")






