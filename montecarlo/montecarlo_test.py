import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer
import unittest


# Some convenience initializer functions
die = lambda : Die(np.array([1, 2, 3, 4, 5, 6]))
coin = lambda : Die(np.array(["H", "T"]))

# Some convenience initializer functions
game1 = lambda : Game([die(), die(), die()])
game2 = lambda : Game([coin(), coin(), coin(), coin(), coin()])



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
        g = game1()                     # 3 dice

        # Ensure last_play instantiates to None
        assert g.get_last_play() == None, "Game failed to initiate with last_play = None"


    ########################
    ## Tests for get_dice ##
    ########################

    def test_get_dice1(self):
        '''
        Ensure the get_dice method returns a list of the correct length.

        This test also serves to ensure that init initializes a Game object with proper list of Die objects
        '''

        # Instantiate a Game
        g = game1()                 # 3 dice

        # Ensure get_dice returns a list of 3 dice
        assert len(g.get_dice()) == 3, "get_dice failed to return a list of appropriate length"


    def test_get_dice2(self):
        '''Ensure that get_dice returns a list of the correct objects'''

        # Instantiate a Game object and a die object to work with
        g = game1()                  # 3 dice

        # Ensure the list contains the correct dice
        for d in g.get_dice():                                              # Iterate through the dice in the Game list
            for i in range(0, 6):                                           # Iterate through the faces in the dice

                # Face names should be 1-6
                assert d.get_state().index[i] == i + 1, "get_dice returned the wrong list of objects"
                # Weights should all be 1.0
                assert d.get_state()["Weight"].iloc[i] == 1.0, "get_dice returned the wrong list of objects"



    #############################
    ## Tests for get_last_play ##
    #############################

    def test_get_last_play_type_error(self):
        '''Ensure get_last_play raises TypeError when passed nonstring input'''

        # Instantiate Game and last_play data frame
        g = game1()
        g.play(10)

        # Try to get last play with bad input
        try:
            g.get_last_play(12)
            # If the above works, this test should fail
            assert 1 == 0, "get_last_play ran with integer input"

        # Whe the above fails, it should raise TypeError
        except Exception as t:
            assert isinstance(t, TypeError), "get_last_play raised other than TypeError with integer input"

    
    def test_get_last_play_value_error(self):
        '''Ensure get_last_play raises ValueError when passed invalid input'''

        # Instantiate game and last_play data frame
        g = game1()                             # 3 dice
        g.play(10)

        # Try to get last play with bad input
        try:
            g.get_last_play("column")
            # If the above works, this test should fail
            assert 1 == 0, "get_last_play worked with invalid string input"

        # When the avobe fails, it should raise ValueError
        except Exception as v:
            assert isinstance(v, ValueError), "get_last_play raised other than ValueError when passed invalid string input"


    def test_get_last_play(self):
        '''Ensure get_last_play returns a pandas data frame of correct shape'''

        # Instantiate Game object
        g = game2()                     # 5 coins

        # Play game
        g.play(15)                      # 15 rolls

        # Ensure the returned object is a data frame
        assert isinstance(g.get_last_play(), pd.DataFrame), "get_last_play failed to return a pandas data frame"

        # Ensure data frame is correct shape
        assert g.get_last_play().shape == (15, 5), "get_last_play returned a data frame of the wrong shape"

    
    def test_get_last_play_narrow1(self):
        '''Ensure get_last_play returns a pandas data frame of correct shape with argument "narrow"'''

        # Instantiate Game object
        g = game2()                       # 5 coins

        # Play game
        g.play(10)                        # 10 rolls

        # Get last play
        n = g.get_last_play(format = "narrow")

        # Ensure the returned object is a data frame
        assert isinstance(n, pd.DataFrame), "get_last_play failed to return pandas data frame with argument 'narrow'"

        # Ensure index is correct shape
        assert len(n.index) == 50, "get_last_play('narrow') failed to multiindex"

        # Ensure data frame is correct shape
        assert n.shape == (50, 1), "get_last_play('narrow') returned a data frame of the wrong shape"

    
    def test_get_last_play_narrow2(self):
        '''Ensure get_last_play returns a pandas data frame of correct shape with argument "n"'''

        # Instantiate Game object
        g = game2()                       # 5 coins

        # Play game
        g.play(10)                        # 10 rolls

        # Get last play
        n = g.get_last_play(format = "n")

        # Ensure the returned object is a data frame
        assert isinstance(n, pd.DataFrame), "get_last_play failed to return pandas data frame with argument 'n'"

        # Ensure index is correct shape
        assert len(n.index) == 50, "get_last_play('n') failed to multiindex"

        # Ensure data frame is correct shape
        assert n.shape == (50, 1), "get_last_play('n') returned a data frame of the wrong shape"



    ####################
    ## Tests for play ##
    ####################

    def test_play_type_error(self):
        '''Ensure play raises TypeError when passed noninteger'''

        # Instantiate Game object
        g = game1()                     # 3 dice

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
        g = game1()                         # 3 dice

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
        g = game1()                         # 3 dice

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
        g = game1()                         # 3 dice

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



######################################################################################################################
###### Analyzer Tests ################################################################################################
######################################################################################################################

class AnalyzerTest(unittest.TestCase):

    ########################
    ## Tests for __init__ ##
    ########################

    def test_init_value_error1(self):
        '''Ensure __init__ raises ValueError when passed other than a Game object'''

        # Try to initialize with bad input
        try:
            a = Analyzer("puppies")
            # If the above works, this test should fail
            assert 1 == 0, "__init__ ran with string input"

        # When the above fails, it should raise ValueError
        except Exception as v:
            assert isinstance(v, ValueError), "__init__ raised other than ValueError when passed string input"


    def test_init_value_error2(self):
        '''Ensure __init__ raises ValueError when passed other than a Game object'''

        # Try to initialize with bad input
        try:
            a = Analyzer(100)
            # If the above works, this test should fail
            assert 1 == 0, "__init__ ran with integer input"

        # When the above fails, it should raise ValueError
        except Exception as v:
            assert isinstance(v, ValueError), "__init__ raised other than ValueError when passed integer input"


    def test_init(self):
        '''Ensure __init__ instantiates an Analyzer object with the correct Game object'''

        # Initialize Analyzer object
        a = Analyzer(game1())                        # 3 dice
        g = a.get_game()

        # Ensure the Analyzer has a Game object attribute
        assert isinstance(g, Game), "Analyzer initiated without Game object"

        # Ensure the Game has a list of three Die objects
        dice = g.get_dice()

        assert len(dice) == 3, "Analyzer initiated with the wrong list of dice"

        for d in dice:
            assert isinstance(d, Die), "Analyser initiated with other than Die objects in Game"


    #######################
    ## Tests for jackpot ##
    #######################

    def test_jackpot0(self):
        '''Ensure jackpot returns an integer equal to the number of jackpots'''

        # We will have to construct a fake last play here
        g = game1()                     # 3 dice
        g._last_play = pd.DataFrame([[2, 3, 4, 1, 4],        # 0 jackpots
                                     [3, 2, 4, 5, 3],
                                     [3, 3, 3, 4, 5]
                                     ])
        
        # Make sure jackpot == 2
        assert Analyzer(g).jackpot() == 0, "jackpot failed to return zero when there were no jackpots"


    def test_jackpot1(self):
        '''Ensure jackpot returns an integer equal to the number of jackpots'''

        # We will have to construct a fake last play here
        g = game1()                     # 3 dice
        g._last_play = pd.DataFrame([[1, 2, 3],
                                     [4, 5, 6],
                                     [3, 3, 3],
                                     [6, 4, 2],
                                     [4, 4, 4]])        # 2 jackpots
        
        # Make sure jackpot == 2
        assert Analyzer(g).jackpot() == 2, "jackpot failed to return the correct number"


    ###########################
    ## Tests for face_counts ##
    ###########################

    def test_face_counts    (self):
        '''Ensure that face_counts returns a data frame with proper shape and values'''

        # Initialize Analyzer object to work with
        g = game1()                     # 3 dice
        g.play(10)                      # 10 rolls
        a = Analyzer(g)

        # face_counts should return a data frame of shape (10, 6): 10 rolls, 6 faces
        assert a.face_counts().shape == (10, 6), "face_counts returned a data frame of the wrong shape"
        
        # Each row should add up to 3 (3 dice rolled therefore 3 faces to count)
        for sum in a.face_counts().sum(axis = 1):
            assert sum == 3, "face_counts returned inappropriate values"


    ############################
    ## Tests for combo_counts ##
    ############################

    def tests_combo_counts(self):
        '''Ensure combo_counts returns a data frame with appropriate results'''
        g = game1()                 # 3 dice
        g.play(100)                 # 100 rolls

        a = Analyzer(g)

        assert isinstance(a.combo_counts(), pd.DataFrame), "combo_counts failed to return a pandas data frame"

        counts_local = a.combo_counts()["Counts"]

        # Counts should add up to 100
        assert sum(counts_local) == 100, "combo_counts failed to report the correct number of results"

        # Length should be <=32 because there are only 56 combinations of 3 numbers 1-6
        assert len(counts_local) <= 56, "combo_counts failed to consolidate unique permutations"
      



    ###########################
    ## Tests for perm_counts ##
    ###########################

    def text_perm_counts(self):
        '''Ensure perm_counts returns a data frame with appropriate results'''
        g = game2()                 # 5 coins
        g.play(40)                  # 40 rolls

        a = Analyzer(g)

        assert isinstance(a.perm_counts(), pd.DataFrame), "perm_counts failed to return a pandas data frame"

        counts_local = a.perm_counts()["Counts"]

        # Counts should add up to 40
        assert sum(counts_local) == 40, "perm_counts failed to report the correct number of results"

        # Length should be <=32 because there are only 32 permutations of 5 "H" and "T"
        assert len(counts_local) <= 32, "perm_counts failed to consolidate unique permutations"

    def test_compare_combos_perms(self):
        '''Ensure combo_counts returns <= the amount of rows as perm_counts'''

        g = game1()                 # 3 dice
        g.play(50)                  # 50 rolls

        a = Analyzer(g)

        # There should never be more combinations than permutations
        assert len(a.combo_counts()) <= len(a.perm_counts()), "more combos than perms"




if __name__ == "__main__":
    unittest.main(verbosity = 3)
