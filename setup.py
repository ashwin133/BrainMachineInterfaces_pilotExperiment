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
    return gameEngine

if __name__ == "__main__":
    gameEngine = initialiseGame()
    gameEngine = runGameSetup(gameEngine=gameEngine)