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
    [ 105,  105,  295,  115],  # Inner horizontal walls with gaps
    [ 505,  205,  695,  215],
    [ 205,  305,  445,  315],
    [ 605,  405,  895,  415],
    [ 305,  505,  595,  515],
    [ 105,  605,  245,  615],
    [ 805,  605,  995,  615],
    [ 105,  105,  115,  235],  # Inner vertical walls with gaps
    [ 205,  365,  215,  595],
    [ 405,  205,  415,  485],
    [ 605,  415,  615,  595],
    [ 805,  105,  815,  285],
    [1005,  415, 1015,  595],
    [1155,  155, 1165,  335]
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

    return gameEngine 

if __name__ == "__main__":
    gameEngine = initialiseGame()