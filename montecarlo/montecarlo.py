print("Imported module sim.")

import numpy as np
import pandas as pd


######################################################################################################################
###### Die ###########################################################################################################
######################################################################################################################

class Die:
    '''
    A Die object represents a stochastic object with a specified number of faces represented by unique symbols (str or numeric,
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
    Game object takes one or more dice (of the Die class) with the same number and names of faces and simulates rolling them.  
    '''


    def __init__(self, dice):
        '''
        Purpose:
        Initializes a Game object with a given list of dice.

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
        None.

        Outputs:
        dice : list of Die objects that the Gmae was instantiated with
        '''

        return self._dice
    

    def get_last_play(self, format = "wide"):
        '''
        Purpose:
        Safely retrieve information on the last game played.

        Inputs:
        format : string "wide" or "narrow" to desribe the shape of the dataframe returned.
                 "wide" or "w" will return the dataframe with row indexes representing Roll # and columns representing Die #.
                 "narrow" or "n" will return the dataframe multi-indexed with level 1 representing Roll # and level 2 representing Die #.

        Outputs:
        last_play : pandas dataframe with results from the last game, in wide or narrow format as specified. Defaults to wide.    
        '''

        if not isinstance(format, str):
            raise TypeError("Argument must be a string")

        inputs = ["narrow", "n", "wide", "w"]

        if format not in inputs:
            raise ValueError("Argument must be string 'narrow' or 'wide'")

        df = self._last_play

        if format == "narrow" or format == "n":
            df = pd.DataFrame(df.stack())
            df.columns = ["Result"]

        return df


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
###### Analyzer ######################################################################################################
######################################################################################################################

class Analyzer():
    '''
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.
    '''

    def __init__(self, game):
        '''
        Purpose:
        Initializes Analyzer object with a given game.

        Inputs:
        game : Game object to be analyzed.

        Outputs:
        Analyzer object with the given Game.        
        '''

        # Raise ValueError if argument is not a Game object
        if not isinstance(game, Game):
            raise ValueError("Anlyzer must be initialized with a Game object")
        
        # Save state data
        self._game = game
        self._jackpots = None
        self._face_counts = None
        self._combos = None
        self._perms = None


    def get_game(self):
        '''
        Purpose:
        Safely retrieve a copy of the Game object that the Analyzer was initialized with.

        Inputs:
        None.

        Outputs:
        Game object the Analyzer was initialized with.        
        '''

        return self._game
    

    def jackpot(self):
        '''
        Purpose:
        Computes the number of times all Die objects 'rolled' the same face in a single roll, returning an integer value.

        Inputs:
        None.

        Outputs:
        jackpots : int representing number of times all dice rolled the same face.
        '''
        # Only do the calculation the first time
        if self._jackpots == None:

            # Instantiate a counter
            jackpots = 0

            # Iterate over rows of the last_play data frame to see how many unique values
            for value in self._game.get_last_play().nunique(axis = 1):
                # When nunique = 1, that's a jackpot!
                if value == 1: jackpots += 1
            
            # Store state data
            self._jackpots = jackpots

        return jackpots
    

    def face_counts(self):
        '''
        Purpose:
        Computes how many times each face is rolled for each roll in a game, returning a data frame describing the faces rolled
        in the Game.
        
        Inputs:
        None.
        
        Outputs:
        face_counts : pandas DataFrame describing the faces rolled in the Game, with index Roll # and face values as columns.
        '''
        # Return the result if it has already been constructed
        if isinstance(self._face_counts, pd.DataFrame): return self._face_counts

        # Get the results from the Game to work with
        g = self._game.get_last_play()

        # Construct data frame from value counts for each row (Roll #)
        counts = pd.DataFrame([g.loc[i].value_counts() for i in range(1, len(g.index) + 1)])

        # Clean up NaN's and convert to int
        counts = counts.fillna(value = 0).astype(np.int8)

        # Store the result
        self._face_counts = counts
                          
        return self._face_counts
    

    def combo_counts(self):
        '''
        Purpose:
        Computes distinct combinations (regardless of order) of faces rolled and reports them along with their counts in a pandas data frame.
        Distinct combinations are described in a Multiindex with a single column of counts.
        
        Inputs:
        None.
        
        Outputs:
        combos : pandas data frame of all distinct combinations and their counts.
        '''

        # Retreive results if it has already ben calculated
        if isinstance(self._combos, pd.DataFrame): return self._combos
        
        # Get the results from the game to work with sorted so that order doesn't matter
        g = np.sort(self._game.get_last_play().to_numpy(), axis = 1)

        # Standardize order of results (sort along axis 1) and store in hashable tuples      
        results = [tuple(result) for result in g]

        # Construct dictionary of result : count pairs
        d = {}

        for result in results:
            
            # If not in d, add with count 1
            if result not in d:
                d[result] = 1

            # Else increment the count
            else:
                d[result] += 1

        # Store the dictionary as a multiindexed data frame
        self._combos = pd.DataFrame(d.values(), index = d.keys(), columns = ["Counts"])

        return self._combos


        # Multiindex includes faces and counts


    def perm_counts(self):
        '''
        Purpose: Computes the distinct (ordered) permutations of faces rolled and reports them along with their counts in a
        pandas data frame. Distinct combinations are described in a multiindex with a single column of counts.

        Inputs:
        None.

        Outputs:
        perms : pandas data frame of all distinct permutations and their counts.
        '''

        # Retrieve result if it has already been calculated
        if isinstance(self._perms, pd.DataFrame): return self._perms

        # Get results as a list of hashable tuples
        g = self._game.get_last_play().to_numpy()
        results = [tuple(result) for result in g]

        # Construct dictionary of result : count pairs
        d = {}

        for result in results:
            
            # If not in d, add with count 1
            if result not in d:
                d[result] = 1

            # Else increment the count
            else:
                d[result] += 1

        # Store the dictionary as a multiindexed data frame
        self._perms = pd.DataFrame(d.values(), index = d.keys(), columns = ["Counts"])

        return self._perms





