# hold all defined variables for the pilot experiment

# define user path
import sys
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

# import libraries
from objects import *





def initialiseGame():

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

    # initialise out of test mode
    gameEngine.testMode = False

    return gameEngine 

if __name__ == "__main__":
    gameEngine = initialiseGame()