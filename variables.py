# hold all defined variables for the pilot experiment

# define user path
import sys
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

# import libraries
from objects import *




def initialiseGame():

    import numpy as np

    mazeDims = np.array([
    [   5,    5, 1265,   25],  # Top border with gap
    [   5,    5,   25,  735],  # Left border with gap
    [   5,  715, 1265,  735],  # Bottom border with gap
    [1245,    5, 1265,  735],  # Right border with gap
    [ 105,  105,  295,  125],  # Inner horizontal walls with gaps
    [ 505,  205,  695,  225],
    [ 205,  305,  445,  325],
    [ 605,  405,  895,  425],
    [ 305,  505,  595,  525],
    [ 105,  605,  245,  625],
    [ 805,  605,  995,  625],
    [ 105,  105,  125,  235],  # Inner vertical walls with gaps
    [ 205,  365,  225,  595],
    [ 605,  415,  625,  595],
    [ 805,  105,  825,  285],
    [1005,  415, 1025,  595],
    [1155,  155, 1175,  335]
    ])



    # colours
    BLUE = (25, 25, 200)
    BLACK = (23, 23, 23)
    WHITE = (254, 254, 254)
    RED  = (255,0,0)
    GREEN = (0,255,0)
    WHITE = (255,255,255)
    colours = {'BLUE': BLUE , 'BLACK': BLACK, 'WHITE':WHITE, 'RED':RED, 'GREEN':GREEN, 'WHITE':WHITE
    }   
    # Initialise game engine
    gameEngine = GameEngine()

    # set up debugger
    gameEngine.debugger = Debugger(debugLevel=3)

    # set screen properties of game engine
    gameEngine.screen_width = 1270    
    gameEngine.screen_height = 740   

    # store colour settings
    gameEngine.colours = colours

    #store maze info
    gameEngine.mazeDims = mazeDims

    # initialise out of test mode
    gameEngine.testMode = False

    # 
    gameEngine.fps = 30

    # metadata for placing target
    gameEngine.targetPlaceFrequency = 5000
    gameEngine.targetWidth = 40
    gameEngine.targetHeight = 40

    # load in unstable mode
    gameEngine.unstableMode = False

    # metadata for placing minion
    gameEngine.minionPlaceFrequency = 10000
    gameEngine.minionWidth = 40
    gameEngine.minionHeight = 40
    gameEngine.minionSpeed = 4

    return gameEngine 

if __name__ == "__main__":
    gameEngine = initialiseGame()