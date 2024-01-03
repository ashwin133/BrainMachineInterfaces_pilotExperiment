"""
Handles setup for game
"""
import sys
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

# import libraries
from objects import *
from variables import initialiseGame
import pygame

def runGameSetup(gameEngine):
    pygame.init()

    gameEngine.screen = pygame.display.set_mode((gameEngine.screen_width, gameEngine.screen_height))
    # Set the title of the window
    pygame.display.set_caption('Display Variable Example')



    # Set up fonts
    gameEngine.font = pygame.font.Font(None, 36)  # You can also use a specific font.

    # Define the variable you want to display
    gameEngine.gameStatistics.score = 0  # Example variable

    gameEngine.createMaze()
    

    
    # start the clock
    gameEngine.clock = pygame.time.Clock()

    # cursor path
    cursorPaths = {'left': "Images/fish_left.png", 'right': "Images/fish2_right.png",
                   'down': "Images/fish_down.png",'up': "Images/fish_up.png"}
    if gameEngine.unstableMode:
        unstableCursor = True
        delayLength = 4
    else:
        unstableCursor = False
        delayLength = 0
    controlMethod = "Mouse"
    gameEngine.cursor = Cursor(x=gameEngine.screen_width//2, y=gameEngine.screen_height//2, width=60, height=40, color=(255, 255, 255),imagePaths=cursorPaths,delaySamples=delayLength,unstableMode=unstableCursor,controlMethod= controlMethod)
    
    

    # initialise skull zone image
    skullImagePath = "Images/skull_bright_orange.png"
    gameEngine.skullImage = pygame.image.load(skullImagePath)
    gameEngine.spawnDangerZone(25,665,50,50)

    # initialise danger bar
    gameEngine.spawnDangerBar(time = 20)

    # get piranha image
    pathToPiranhaImage = "Images/piranha.png"
    gameEngine.piranhaImage = pygame.image.load(pathToPiranhaImage)

    # spawn energy zones
    gameEngine.spawnEnergyZones()

    # initialise target image
    pathToTargetImage = "Images/gem1.png"
    gameEngine.targetImage = pygame.image.load(pathToTargetImage)

    # initialise blinking skull
    gameEngine.blinkingSkull = BlinkingSkull(765,5,60,40,gameEngine)

    # spawn sign that piranha nest destroyed
    piranhaOffFont = pygame.font.Font(None, 144)  # You can also use a specific font.
    gameEngine.piranhaOffSign = PiranhaNestDestroyedSign(gameEngine,piranhaOffFont)

    # spawn sign that piranha nest spawned
    piranhaOffFont = pygame.font.Font(None, 144)  # You can also use a specific font.
    gameEngine.piranhaOnSign = PiranhaNestSpawnedSign(gameEngine,piranhaOffFont)


    return gameEngine


if __name__ == "__main__":
    gameEngine = initialiseGame()
    gameEngine = runGameSetup(gameEngine=gameEngine)