import pandas as pd
import numpy as np
from sim import Die, Game
import unittest


# Some convenience initializer functions
die = lambda : Die(np.array([1, 2, 3, 4, 5, 6]))
coin = lambda : Die(np.array(["H", "T"]))

######################################################################################################################
###### Die Tests #####################################################################################################
######################################################################################################################



class DieTester(unittest.TestCase):
    '''
    Class with methods to test the Die class from sim.
    '''
    ############################
    #### Tests for __init__ ####
    ############################
    
    def test_init_type_error(self):
        '''Ensure __init__ raises TypeError when the argument is not a numpy array'''
        # Try to instantiate a Die object with bad input (not a numpy array)
        try:
            Die([1, 2, 3, 4, 5, 6])
            # If the above works, this test should fail
            assert 1 == 0, "__init_ worked with bad input (not a numpy array)"

        # When the above fails, it should raise a TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "__init__ raised the wrong error when passed bad input (not a numpy array)"

    
    def test_init_value_error(self):
        '''Ensure __init__ raises ValueError when the array contains dupicate values'''
        # Try to instantiate a die with bad input (duplicate faces)
        try:
            Die(np.array(["H", "T", "H"]))
            # If the above works, this test should fail
            assert 1 == 0, "__init__ worked with bad input (duplicate faces)"

        # when the above fails, it should raise a ValueError
        except Exception as v:
            assert isinstance(v, ValueError), "__init__ raised the wrong error when passed bad input (duplicate values)"

    
    def test_init(self):
        '''Ensure initialized object has correct state DataFrame'''
        # Instantiate a Die object
        d = die()

        # d.state should be a pandas DataFrame
        assert isinstance(d.get_state(), pd.DataFrame), "d.state is not a pd.DataFrame"

        # all weights should be 1 (True)
        assert d.get_state()["Weight"].all(), "Weights not all 1"

        # 6 faces
        assert d.get_state().shape == (6, 1), "Incorrect shape"


    #########################
    ## Tests for get_state ##
    #########################

    def test_get_state(self):
        '''Ensure get_state returns a dataframe of proper shape'''

        # Instantiate a Die object
        d = coin()

        # Return value should be a pd.DataFrame
        assert isinstance(d.get_state(), pd.DataFrame), "get_state returned something other than a pd.DataFrame"

        # DataFrame should be of shape (2, 1)
        assert d.get_state().shape == (2, 1), "get_state returned a DataFrame of the wrong shape"

    ## Another good test is the fact that all of my other tests work with get_state()
    

    #############################
    ## Tests for change_weight ##
    #############################

    def test_change_weight_index_error(self):
        '''Ensure change_weight raises IndexError if the given face is not in the Die'''
        # Instantiate a Die object
        d = die()

        # Try to change the weight of a nonexistant face
        try:
            d.change_weight(7, 2)
            # If the above works, this test should fail
            assert 1 == 0, "change_weight ran with a nonexistent face"

        # When the above fails, it should raise IndexError
        except Exception as i:
            assert isinstance(i, IndexError), "change_weight raised the wrong error when passed a nonexistant face"

    
    def test_change_weight_type_error(self):
        '''Ensure change_weight raises TypeError if weight cannot be interpreted as numeric'''
        # Instantiate a Die object
        d = die()

        # Try to change weight to invalid weight
        try:
            d.change_weight(3, "always")

            # If the above works, this test should fail
            assert 1 == 0, "change_weight() ran with invalid weight passed"

        # When the above fails, it should raise TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "change_weight raised the wrong error when invalid weight passed"

    
    def test_change_weight(self):
        '''Ensure change_weight actually changes the weight'''

        # Instantiate a Die object
        d = die()

        # Change weight
        d.change_weight(2, 3)

        assert d.get_state().loc[2, "Weight"] == 3, "change_weight failed to change weight correctly"


    ####################
    ## Tests for roll ##
    ####################

    def test_roll_type_error(self):
        '''Ensure roll raises TypeError if passed non-integer argument'''

        # Instantiate a Die object
        d = die()

        # Roll die
        try:
            d.roll("ten times")
            # If the above works, this test should fail
            assert 1 == 0, "roll ran with invalid input"

        # When the above fails, it should raise TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "roll raised the wrong error when passed invalid input"

    
    def test_roll(self):
        '''Ensure roll returns a list of length(times)'''

        # Instantiate a Die object
        d = die()

        # Roll die
        r = d.roll(10)

        # Return value should be a list
        assert isinstance(r, list), "roll failed to return a list"

        # Returned list should be of length(times)
        assert len(r) == 10, "roll returned a list of the wrong length"

        # Returned list should be full of values that equal the sides of the Die
        for element in r:
            assert element in d.get_state().index, "roll returned values that were not valid faces"
            d.get_state()






######################################################################################################################
###### Game Tests ####################################################################################################
######################################################################################################################

# Some convenience initializer functions
game1 = lambda : Game([die(), die(), die()])
game2 = lambda : Game([coin(), coin(), coin(), coin(), coin()])



class GameTester(unittest.TestCase):

    ########################
    ## Tests for __init__ ##
    ########################


    def test_init_type_error1(self):
        '''Ensure a Game object raises TypeError when passed not a list'''

        # Try to instantiate a Game object with a string
        try:
            Game("not a list")
            # If the above works, this test should fail
            assert 1 == 0, "Game instantiated with a string"

        # When the above fails, it should raise a TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "Game raised other than TypeError when instantiated with string"

    
    def test_init_type_error2(self):
        '''Ensure a Game object raises TypeError when passed a list not full of Die objects'''

        # Try to instantiate a Game object with a list of ints
        try:
            Game([1, 2, 3])
            # If the above works, this test should fail
            assert 1 == 0, "Game instantiated with a list of ints"

        # When the above fails, it should raise a TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "Game raised other than TypeError when instantiated with a list of ints"

    
    def test_init_value_error(self):
        '''Ensure a Game object raises ValueError when passed a list of dissimilar Die objects'''

        # Try to instantiate a Game object with dissimilar Die objects
        try:
            Game([die(), coin()])
            # If the above works, this test should fail
            assert 1 == 0, "Game instantiated with a list of dissimilar Die objects"

        # When the above fails, it should raise a ValueError
        except Exception as v:
            assert isinstance(v, ValueError), "Game raised other than ValueError when instantiated with dissimilar dice"


    def test_init1(self):
        '''Ensure init instantiates a Game object'''

        # Initialize a Gmae object
        g = game1()

        # Ensure g is a Game object
        assert isinstance(g, Game), "init failed to create a Game object"

    
    def test_init2(self):
        '''Ensure Game instantiates with last_play = None'''

        # Initialize a Game object
        g = game1()

        # Ensure last_play instantiates to None
        assert g.get_last_play() == None, "Game failed to initiate with last_play = None"


    def test_get_dice1(self):
        '''
        Ensure the get_dice method returns a list of the correct length.

        This test also serves to ensure that init initializes a Game object with proper list of Die objects
        '''

        # Instantiate a Game
        g = game1()                 # game with 3 dice

        # Ensure get_dice returns a list of 3 dice
        assert len(g.get_dice()) == 3, "get_dice failed to return a list of appropriate length"


    def test_get_dice2(self):
        '''Ensure that get_dice returns a list of the correct objects'''

        # Instantiate a Game object and a die object to work with
        g = game1()                  # Game with 3 dice

        # Ensure the list contains the correct dice
        for d in g.get_dice():                                              # Iterate through the dice in the Game list
            for i in range(0, 6):                                           # Iterate through the faces in the dice

                # Face names should be 1-6
                assert d.get_state().index[i] == i + 1, "get_dice returned the wrong list of objects"
                # Weights should all be 1.0
                assert d.get_state()["Weight"].iloc[i] == 1.0, "get_dice returned the wrong list of objects"


    def test_get_last_play(self):
        '''Ensure get_last_play returns a pandas data frame of correct shape'''

        # Instantiate Game object
        g = game2()                     # 5 coins

        # Play game
        g.play(15)                      # 15 rolls

        # Ensure the returned object is a data frame
        assert isinstance(g.get_last_play(), pd.DataFrame), "get_last_play failed to return a pandas data frame"

        # Ensure data frame is correct shape
        assert g.get_last_play().shape == (15, 5)


    def test_play_type_error(self):
        '''Ensure play raises TypeError when passed noninteger'''

        # Instantiate Game object
        g = game1()

        # Try to play game with bad input
        try:
            g.play("ten times")
            # If the above works, this test should fail
            assert 1 == 0, "play worked with noninteger input"

        # When the abolve fails, it should raise a TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "play failed to raise TypeError when passed noninteger input"
    

    def test_play_value_error0(self):
        '''Ensure play raises ValueError when passed times = 0'''

        # Instantiate Game object
        g = game1()

        # Try to play game with bad input
        try:
            g.play(0)
            # If the above works, this test should fail
            assert 1 == 0, "play worked with zero input"

        # When the above fails, it should raise a ValueErrer
        except Exception as v:
            assert isinstance(v, ValueError), "play failed to raise ValueError when passed zero input"


    def test_play_value_error1(self):
        '''Ensure play raises ValueError when passed times < 0'''

        # Instantiate Game object
        g = game1()

        # Try to play game with bad input
        try:
            g.play(-1)
            # If the above works, this test should fail
            assert 1 == 0, "play worked with negative input"

        # When the above fails, it should raise a ValueErrer
        except Exception as v:
            assert isinstance(v, ValueError), "play failed to raise ValueError when passed negative input" 


    def test_play_df(self):
        '''Ensure play returns a pandas data frame'''

        # Instantiate Game object
        g = game1()

        # Ensure play returns a pandas data frame
        assert isinstance(g.play(), pd.DataFrame), "play failed to return a pandas data frame"


    def test_play_results1(self):
        '''Ensure play returns appropriate results'''

        # Instantiate a Game object
        g = game1()                     # 3 dice

        # get play results
        results = g.play(15)

        # Ensure the resulting data frame has appropriate shape and values
        assert results.shape == (15, 3), "play returned a data frame of the wrong size"
        
        for list in results.values:
            for v in list:
                assert v in [1, 2, 3, 4, 5, 6], "play returned a dataframe with nonexistant faces"


    def test_play_results2(self):
        '''Ensure play returns appropriate results again'''

        # Instantiate a Game object
        g = game2()                     # 5 coins

        # get play results
        results = g.play(10)

        # Ensure the resulting data frame has appropriate shape and values
        assert results.shape == (10, 5), "play returned a data frame of the wrong size"
        
        for list in results.values:
            for v in list:
                assert v in "HT", "play returned a dataframe with nonexistant faces"









if __name__ == "__main__":
    unittest.main(verbosity = 3)
