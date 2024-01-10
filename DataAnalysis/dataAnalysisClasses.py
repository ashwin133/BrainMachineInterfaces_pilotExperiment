"""
Contains classes to help with data analysis
"""

# import necessary libraries
import pickle
import numpy as np
import sys
sys.path.insert(0,'/Users/ashwin/Documents/Y4 project Brain Human Interfaces/General 4th year Github repo/PilotExperiment/BrainMachineInterfaces_pilotExperiment')

from config_streaming import rigidBodyParts, simpleBodyParts

class ProcessData():
    """
    A class to handle processing of raw data from a game for the purposes of decoding
    """
    def __init__(self,trainingDataPath,testDataPath):
        """
        Retrieves training and test data
        Args:
            @str trainingDataPath: path to game save of training data
            @str testDataPath: path to game save of test data
        """
        self.trainingDataPath = trainingDataPath
        self.testDataPath = testDataPath
        self.trainingDataGameEngine = self.retrieveGameEngineFromFile(self.trainingDataPath)
        self.testDataGameEngine = self.retrieveGameEngineFromFile(self.testDataPath)
        
    
    def retrieveGameEngineFromFile(self,filePath):
        with open(filePath,'rb') as file:
            return pickle.load(file)
    
    def retrieveTrainingFeatureData(self):
        # the training data will be of size T x 51 x 6 where T is the number of timestamps
        self.trainingBodyParts = simpleBodyParts.copy()
        # find the index of the body part in the all rigid bodies
        self.controlBodyPartIdx = self.trainingDataGameEngine.controlBodyPartIdx
        # find the index of the body part in the list of non redundant bodies
        delIdx = self.trainingBodyParts.index(self.controlBodyPartIdx)
        # delete this index from the list of non redundant bodies
        del self.trainingBodyParts[delIdx]

        self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,self.trainingBodyParts,:]
        # we need to delete the control index as this will be what we are trying to find
        
        self.rawFeatureTrainingData = self.rawFeatureTrainingData.reshape(-1,len(self.trainingBodyParts)*6)
        self.trainingSamples = len(self.rawFeatureTrainingData[:,0])

    def retrieveTestFeatureData(self):
        # the test data will be of size T x 51 x 6 where T is the number of timestamps
        self.testBodyParts = simpleBodyParts.copy()
        # find the index of the body part in the all rigid bodies
        self.controlBodyPartIdx = self.testDataGameEngine.controlBodyPartIdx
        # find the index of the body part in the list of non redundant bodies
        delIdx = self.testBodyParts.index(self.controlBodyPartIdx)
        # delete this index from the list of non redundant bodies
        del self.testBodyParts[delIdx]

        self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,self.testBodyParts,:]
        # we need to delete the control index as this will be what we are trying to find
        
        self.rawFeatureTestData = self.rawFeatureTestData.reshape(-1,len(self.testBodyParts)*6)
        self.testSamples = len(self.rawFeatureTestData[:,0])
    
    def retrieveTrainingOutputs(self):
        self.

    def normaliseDatasets(self,byVariance = False):
        self.featureTrainingData = self.normaliseData(self.rawFeatureTrainingData)
        self.featureTestData = self.normaliseData(self.rawFeatureTestData)
        
    def normaliseData(self,data,byVariance = False):
        """
        Normalises data by mean and optionally by variance 

        Args:
            @bool byVariance: normalise data by variance if True (default False)
            TODO: code functionality for normalising by variance as well
        """
        normalisedData = data.copy()

        # Find the mean for each DOF across all times
        DOFmeans = np.average(data,axis = 0)

        # Subtract the mean for each DOF across all times
        for dof,mean in enumerate(DOFmeans):
            normalisedData[:,dof] = normalisedData[:,dof] - mean
        
        # Check means of data are now 0
        assert all(abs(np.average(normalisedData,axis = 0)) < 0.0001)
        
        return normalisedData

