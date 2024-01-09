"""
Functionality to simulate the streaming of rigid body data from motive by feeding each frame 
"""
# import python specific libraries
import os
import sys
import numpy as np
import pandas as pd
import atexit
import time

# add base dir to system path
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

# import my libraries
import StreamingAgent.Client.NatNetClient as NatNetClient
import StreamingAgent.Client.DataDescriptions as DataDescriptions
import StreamingAgent.Client.MoCapData as MoCapData
import StreamingAgent.Client.PythonSample as PythonSample
from StreamingAgent import streamData
print("Program started")

# set what type of data to get e.g. Bone, Bone Marker
typeData = "Bone"

# initialise shared memory
shared_Block,sharedArray = streamData.defineSharedMemory(sharedMemoryName= 'Test Rigid Body', dataType= "Bone", noDataTypes= 51,bodyType='skeleton')

# this function fetches data from motive and dumps data in the shared memory
streamData.fetchLiveData(sharedArray, shared_Block, simulate=False)

print("Program ended successfully")
shared_Block.close()