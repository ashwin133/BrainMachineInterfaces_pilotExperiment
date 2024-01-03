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

        gameEngine.checkIfCursorHitTarget()
        # every X seconds place a target
        gameEngine.checkPlaceTarget()

        # every x seconds 
        gameEngine.checkSpawnMinion()

        # Fill the screen with blue
        #gameEngine.screen.fill(gameEngine.colours['BLUE'])
        gameEngine.draw_sea()
        #gameEngine.draw_waves()

        # Render the text representing the variable
        gameEngine.text = gameEngine.font.render(f'Score: {gameEngine.gameStatistics.score}', True, gameEngine.colours['WHITE'])  # Create a text surface
        gameEngine.text_rect = gameEngine.text.get_rect(center=(gameEngine.screen_width *0.95, 30))  # Get the rectangular area of the text

        # Blit the text onto the screen
        gameEngine.screen.blit(gameEngine.text, gameEngine.text_rect)

        # draw the maze
        gameEngine.drawMaze()

        # update energy zone
        gameEngine.updateEnergyZones()


        # draw game zones
        gameEngine.drawEnergyZones()

        # draw the right cursor
        gameEngine.cursor.handle_keys()  # Adjust cursor velocity based on keys pressed
        gameEngine.cursor.update()       # Update cursor position
        gameEngine.cursor.draw(gameEngine.screen)   # Draw cursor

        # check if any minions hit the cursor
        gameEngine.checkIfMinionHitCursor()

        # update and draw minion
        gameEngine.updateAndDrawMinion()

        # draw all targets
        gameEngine.drawTargets()
        
        # update and draw blinking skull if needed
        gameEngine.updateAndDrawBlinkingSkull()
        # Update danger bar
        gameEngine.updateDangerBar()

        # Draw danger bar
        gameEngine.drawDangerBar()
        
        # draw danger zone if necessary
        gameEngine.drawDangerZone()

        # draw piranha off and on sign if necessary
        gameEngine.piranhaOffSign.update_and_draw()
        gameEngine.piranhaOnSign.update_and_draw()
        

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

