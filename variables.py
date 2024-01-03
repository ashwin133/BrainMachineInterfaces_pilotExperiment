# hold all defined variables for the pilot experiment

# define user path
import sys
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

# import libraries
from objects import *




def initialiseGame():

    import numpy as np

    mazeDims = np.array([
    [   5,    50, 1265,   75],  # Top border with gap
    [   5,    50,   25,  735],  # Left border with gap
    [   5,  715, 1265,  735],  # Bottom border with gap
    [1245,    50, 1265,  735],  # Right border with gap 

    # top left
    [ 200,  200,  345,  220],  # top left horizontal

    # top right
    [ 805,  255,  1075,  275], # top right horizontal
    [ 1055,  175,  1075,  320], # top right vertical

    # bottom left
    [ 205,  360,  445,  380], # bottom left horizontal
    [ 205,  365,  225,  595], # bottom left vertical

    # bottom right
    [ 805,  455,  1095,  475], # bottom right horizontal left part
    [ 555,  555,  815,  575], # bottom right horizontal right part
    [ 805,  465,  825,  600], # bottom right vertical

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
    gameEngine.targetPlaceFrequency = 3000
    gameEngine.targetWidth = 40
    gameEngine.targetHeight = 40

    # load in unstable mode
    gameEngine.unstableMode = False

    # metadata for placing minion
    gameEngine.minionPlaceFrequency = 10000
    gameEngine.minionWidth = 60
    gameEngine.minionHeight = 40
    gameEngine.minionSpeed = 4

    # max targets
    gameEngine.maxTargets = 5


    return gameEngine 

if __name__ == "__main__":
    gameEngine = initialiseGame()