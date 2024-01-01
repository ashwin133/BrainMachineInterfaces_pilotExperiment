import pygame

import sys
import os
from multiprocessing import shared_memory
import numpy as np
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')


# import variables and objects used and run setup
from setup import runGameSetup
from variables import initialiseGame



# Game loop


def startupGame(gameEngine):
    gameEngine.running = True
    while gameEngine.running:

        
        

        gameEngine.gatherKeyPresses()

        gameEngine.checkIfCursorHitWall()

        # Fill the screen with blue
        gameEngine.screen.fill(gameEngine.colours['BLUE'])

        # Render the text representing the variable
        gameEngine.text = gameEngine.font.render(f'Score: {gameEngine.gameStatistics.score}', True, gameEngine.colours['WHITE'])  # Create a text surface
        gameEngine.text_rect = gameEngine.text.get_rect(center=(gameEngine.screen_width *0.9, gameEngine.screen_height * 0.1))  # Get the rectangular area of the text

        # Blit the text onto the screen
        gameEngine.screen.blit(gameEngine.text, gameEngine.text_rect)

        # draw the maze
        gameEngine.drawMaze()

        # draw the right cursor
        gameEngine.cursor.handle_keys()  # Adjust cursor velocity based on keys pressed
        gameEngine.cursor.update()       # Update cursor position
        gameEngine.cursor.draw(gameEngine.screen)   # Draw cursor

        # Update the display
        pygame.display.flip()
        
        

        
        gameEngine.clock.tick(gameEngine.fps)
        gameEngine.checkRunningStatus()
    # End Pygame
    pygame.quit()
    return gameEngine


# if __name__ == "__main__":
#     gameEngine = initialiseGame()
#     gameEngine = runGameSetup(gameEngine=gameEngine)
#     startupGame(gameEngine=gameEngine)

