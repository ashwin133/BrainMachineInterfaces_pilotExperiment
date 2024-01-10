"""
Contains classes to help with data analysis
"""

# import necessary libraries
import pickle
import numpy as np
import sys
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
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

        # Find full calibration matrixes
        self.trainingCalibrationMatrix = self.retrieveCalibrationMatrix(self.trainingDataGameEngine)
        self.testCalibrationMatrix = self.retrieveCalibrationMatrix(self.testDataGameEngine)
       
        # Extract final calibration indexes
        self.extractFinalCalibrationIndexes()

    def retrieveCalibrationMatrix(self,gameEngine):
        """
        Retrieves the full calibration matrix
        """
        # Find calibration matrix
        calibrationMatrix = gameEngine.calibrationMatrix

        # Use the calibration matrix to create a full calibration matrix
        fullCalibrationMatrix = np.zeros((6,6))
        fullCalibrationMatrix[0:3,0:3] = calibrationMatrix
        fullCalibrationMatrix[3:,3:] = calibrationMatrix

        return fullCalibrationMatrix

    def retrieveGameEngineFromFile(self,filePath):
        with open(filePath,'rb') as file:
            return pickle.load(file)
    
    def retrieveTrainingFeatureData(self,rigidBodyGroup):
        # the training data will be of size T x 51 x 6 where T is the number of timestamps
        self.trainingBodyParts = simpleBodyParts.copy()
        # find the index of the body part in the all rigid bodies
        self.controlBodyPartIdx = self.trainingDataGameEngine.controlBodyPartIdx
        self.rigidBodyGroup = rigidBodyGroup
        if rigidBodyGroup == "A":
            # find the index of the body part in the list of non redundant bodies
            delIdx = self.trainingBodyParts.index(self.controlBodyPartIdx)
            # delete this index from the list of non redundant bodies
            del self.trainingBodyParts[delIdx]

            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,self.trainingBodyParts,:]
            # we need to delete the control index as this will be what we are trying to find
            self.noBodyParts = len(self.trainingBodyParts)
        
        elif rigidBodyGroup == "B":
            controlIdx = self.trainingBodyParts.index(self.controlBodyPartIdx)
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,self.controlBodyPartIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1

        # Transform the training data to the correct plane using the calibration matrix
        self.rawFeatureTrainingData = np.tensordot(self.rawFeatureTrainingData,self.trainingCalibrationMatrix,axes = ([2],[0]))

        # Reshape matrix to N_ x DOF N_ is number of timestamps in training set and DOF is number of degrees of freedom
        self.rawFeatureTrainingData = self.rawFeatureTrainingData.reshape(-1,self.noBodyParts*6)
        self.trainingSamples = len(self.rawFeatureTrainingData[:,0])

    def retrieveTestFeatureData(self,rigidBodyGroup = 'A'):
        """
        Args:
            rigidBodyGroup - A: only delete control body, B: only use control body
        """
        # the test data will be of size T x 51 x 6 where T is the number of timestamps
        self.testBodyParts = simpleBodyParts.copy()
        # find the index of the body part in the all rigid bodies
        self.controlBodyPartIdx = self.testDataGameEngine.controlBodyPartIdx
        self.rigidBodyGroup = rigidBodyGroup
        if rigidBodyGroup == "A":
            # find the index of the body part in the list of non redundant bodies
            delIdx = self.testBodyParts.index(self.controlBodyPartIdx)
            # delete this index from the list of non redundant bodies
            del self.testBodyParts[delIdx]

            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,self.testBodyParts,:]
            # we need to delete the control index as this will be what we are trying to find
            self.noBodyParts = len(self.testBodyParts)
        
        elif rigidBodyGroup == "B":
            controlIdx = self.testBodyParts.index(self.controlBodyPartIdx)
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,self.controlBodyPartIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1

        # Transform the test data to the correct plane using the calibration matrix
        self.rawFeatureTestData = np.tensordot(self.rawFeatureTestData,self.testCalibrationMatrix,axes = ([2],[0]))

        # Reshape matrix to N_ x DOF N_ is number of timestamps in test set and DOF is number of degrees of freedom
        self.rawFeatureTestData = self.rawFeatureTestData.reshape(-1,self.noBodyParts*6)
        self.testSamples = len(self.rawFeatureTestData[:,0])
    
    def retrieveTrainingOutputs(self):
        self.outputTrainingData = self.trainingDataGameEngine.cursorVelocityWriteDatastore[2:,:]
    
    def retrieveTestOutputs(self):
        self.outputTestData = self.testDataGameEngine.cursorVelocityWriteDatastore[1:,:]

    def extractFinalCalibrationIndexes(self):
        self.testFinalCalibrationIdx = self.testDataGameEngine.calibrationLastRecording
        self.trainingFinalCalibrationIdx = self.trainingDataGameEngine.calibrationLastRecording
        
    def normaliseDatasets(self,byVariance = False,delCalibrationData = True):
        self.featureTrainingData = self.normaliseData(self.rawFeatureTrainingData,byVariance)
        self.featureTestData = self.normaliseData(self.rawFeatureTestData,byVariance)
        if delCalibrationData:
            self.deleteCalibrationInformation()
        #self.outputTrainingData = self.normaliseData(self.outputTrainingData,byVariance)
        #self.outputTestData = self.normaliseData(self.outputTestData,byVariance)
    
    def normaliseData(self,data,byVariance = True):
        """
        Normalises data by mean and optionally by variance 

        Args:
            @bool byVariance: normalise data by variance if True (default False)
            TODO: code functionality for normalising by variance as well
        """
        if byVariance == False:
            normalisedData = data.copy()

            # Find the mean for each DOF across all times
            DOFmeans = np.average(data,axis = 0)

            # Subtract the mean for each DOF across all times
            for dof,mean in enumerate(DOFmeans):
                normalisedData[:,dof] = normalisedData[:,dof] - mean
            
            # Check means of data are now 0
            assert all(abs(np.average(normalisedData,axis = 0)) < 0.0001)
        
        else:
            scaler = StandardScaler()
            normalisedData = scaler.fit_transform(data)
        
        return normalisedData
    
    def deleteCalibrationInformation(self):
        self.featureTrainingData = self.featureTrainingData[self.trainingFinalCalibrationIdx+1:,:]
        self.featureTestData = self.featureTestData[self.testFinalCalibrationIdx+1:,:]

    def performLinearRegression(self):
        self.reg  = linear_model.LinearRegression().fit(self.featureTrainingData, self.outputTrainingData)

    def gatherPredictions(self):
        self.testVelPredict = self.reg.predict(self.featureTestData)
    
    def exportPredictions(self,fileName):
        np.savez(fileName,predVelocities=self.outputTestData)