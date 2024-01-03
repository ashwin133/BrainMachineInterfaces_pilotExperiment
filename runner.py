"""
script used to run game
"""

from variables import initialiseGame
from setup import runGameSetup
from gameDynamics import startupGame

# initialise the game engine to pass configuration of game
gameEngine = initialiseGame()

# next run game setup to load game configurationss 
gameEngine = runGameSetup(gameEngine=gameEngine)

# now start the game
startupGame(gameEngine=gameEngine)

