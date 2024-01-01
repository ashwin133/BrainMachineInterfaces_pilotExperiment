# hold basic tests for the pilot experiment

# add Root Directory to system path to import created packages
import sys
import pytest
import warnings
import pynput
import time
import multiprocessing

import os

# Get the directory of the current file (test_basics.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# relative path
variables_dir = os.path.join(current_dir, '../')

# Add this directory to sys.path
sys.path.insert(0, variables_dir)

def testGameRuns():
    
    from variables import initialiseGame
    from setup import runGameSetup
    from gameDynamics import startupGame
    gameEngine = initialiseGame()
    gameEngine.testMode = True
    gameEngine.testTime = 3000
    # next run game setup to load game configurations 
    gameEngine = runGameSetup(gameEngine=gameEngine)
    startupGame(gameEngine=gameEngine)

def testGameStartsAndExitsWithNoError():
    sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')


    with pytest.warns(UserWarning):
        warnings.warn("DeprecationWarning", UserWarning) 
        proc1 = multiprocessing.Process(target=runGame, args=())
        proc2 = multiprocessing.Process(target=endGameByQ, args=())
        proc1.start()
        proc2.start()
        proc1.join()
        proc2.join()
        


def runGame():
    from variables import initialiseGame
    from setup import runGameSetup
    from gameDynamics import startupGame
    gameEngine = initialiseGame()
    # next run game setup to load game configurations 
    gameEngine = runGameSetup(gameEngine=gameEngine)
    startupGame(gameEngine=gameEngine)

def endGameByQ():
    time.sleep(7)
    from pynput.keyboard import Key, Controller
    keyboard = Controller()
    keyboard.press('q')
    keyboard.release('q')

