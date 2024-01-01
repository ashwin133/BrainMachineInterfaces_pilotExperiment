# hold basic tests for the pilot experiment

# add Root Directory to system path to import created packages
import sys
import pytest
import warnings
import pynput
import time
import multiprocessing

sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')



def testGameStartsWithNoError():
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

