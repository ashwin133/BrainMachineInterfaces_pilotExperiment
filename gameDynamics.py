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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return gameEngine
            

            # or get movement from key presses
            if event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.KEYUP:
                if event.key == ord('q'):
                    running = False
                    pygame.quit()
                    return gameEngine
            

        # Fill the screen with blue
        gameEngine.screen.fill(gameEngine.blue)

        # Render the text representing the variable
        gameEngine.text = gameEngine.font.render(f'Score: {gameEngine.gameStatistics.score}', True, gameEngine.white)  # Create a text surface
        gameEngine.text_rect = gameEngine.text.get_rect(center=(gameEngine.screen_width/2, gameEngine.screen_height/2))  # Get the rectangular area of the text

        # Blit the text onto the screen
        gameEngine.screen.blit(gameEngine.text, gameEngine.text_rect)

        # Update the display
        pygame.display.flip()

    # End Pygame
    pygame.quit()


if __name__ == "__main__":
    gameEngine = initialiseGame()
    gameEngine = runGameSetup(gameEngine=gameEngine)
    startupGame(gameEngine=gameEngine)

