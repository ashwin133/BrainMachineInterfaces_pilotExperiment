# hold basic tests for the pilot experiment

# add Root Directory to system path to import created packages
import sys
import pytest
import warnings
import pynput
import time
import multiprocessing

sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

def testGameRuns():
    sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')
    from variables import initialiseGame
    from setup import runGameSetup
    from gameDynamics import startupGame
    gameEngine = initialiseGame()
    gameEngine.testMode = True
    gameEngine.testTime = 3000
    # next run game setup to load game configurations 
    gameEngine = runGameSetup(gameEngine=gameEngine)
    startupGame(gameEngine=gameEngine)

