"""
Contains classes to help with data analysis
"""

# import necessary libraries
import pickle
import numpy as np
import sys
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from config_streaming import renderingBodyParts
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
            controlIdx = simpleBodyParts[self.trainingBodyParts.index(self.controlBodyPartIdx)]
            print(controlIdx)
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1
        
        elif rigidBodyGroup == "C":
            lHandIdx = rigidBodyParts.index("LHand")
            controlIdx = self.trainingBodyParts.index(lHandIdx)
            print(controlIdx)
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1
        
        elif rigidBodyGroup == "D":
            rHandIdx = rigidBodyParts.index("RHand")
            controlIdx = rHandIdx
            print(controlIdx)
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1
        
        elif rigidBodyGroup == "E":
            # Decode from rotations of all body parts except right hand

            # find the index of the body part in the list of non redundant bodies
            delIdx = self.trainingBodyParts.index(self.controlBodyPartIdx)
            # delete this index from the list of non redundant bodies
            del self.trainingBodyParts[delIdx]

            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,self.trainingBodyParts,:]
            # we need to delete the control index as this will be what we are trying to find
            self.noBodyParts = len(self.trainingBodyParts)


            # Extract the rotations only
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,:,3:] 

            # Reshape matrix to N_ x DOF N_ is number of timestamps in training set and DOF is number of degrees of freedom

            self.trainingSamples = len(self.rawFeatureTrainingData[:,0])


        
        
        elif rigidBodyGroup == "F":
            # # # angles only, use all except right side

            # Extract data from all body parts
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of right hand on principal skeleton
            idxRightHand = renderingBodyParts.index('RHand') * 3

            # Find index of right shoulder on principal skeleton
            idxRightShoulder = renderingBodyParts.index('RShoulder') * 3

            # Retrieve all rigid body rotations for all timestamps
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,:,3:].reshape(-1,19*3)
            
            # Delete rigid bodies on the right side
            self.rawFeatureTrainingData = np.delete(self.rawFeatureTrainingData,slice(idxRightShoulder,idxRightHand+3,1),1)

            # Reshape into N x m x DOF
            self.rawFeatureTrainingData = self.rawFeatureTrainingData.reshape(-1,15,3)

        

        elif rigidBodyGroup == "G":
            # # # Angles only: only get the left hand

            # Extract data from all body parts
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of left hand in principal rigid bodies
            idxLeftHand = renderingBodyParts.index('LHand') 

            # Extract only the left hand rotations for training set
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,idxLeftHand,3:].reshape(-1,1,3)


        elif rigidBodyGroup == "H":
            # # # only get the right hand

            # Extract data from all body parts
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of right hand in principal rigid bodies
            idxRightHand = renderingBodyParts.index('RHand') 

            # Extract only right hand rotations 
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,idxRightHand,3:].reshape(-1,1,3)

        elif rigidBodyGroup == "I":
            # # # Only use the lower body
            # # # angles only

            # Extract rotations from all body parts
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,3:]

            # Find index of left thigh on principal skeleton as this is start of lower bodies
            idxLeftThigh = renderingBodyParts.index('LThigh') 

            # Find index of right foot on principal skeleton as this is end of lower bodies
            idxRightFoot = renderingBodyParts.index('RFoot') 
            
            # Extract data from specific rigid bodies
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,idxLeftThigh:idxRightFoot+1,:]
            

            


        
        elif rigidBodyGroup == "J":
            # # # Only use the upper body ( excludes upper left and right)
            # # # angles only

            # Find index of neck on principal skeleton as this is start of upper body
            idxNeck = renderingBodyParts.index('Neck') 

            # Find index of head on principal skeleton as this is end of upper body
            idxHead = renderingBodyParts.index('Head')
            
            # Extract rotations from all body parts
            self.rawFeatureTrainingData = self.trainingDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,3:]

            # Extract data from specific rigid bodies
            self.rawFeatureTrainingData = self.rawFeatureTrainingData[:,idxNeck:idxHead+1,:]


        # Transform the training data to the correct plane using the calibration matrix
        if self.rigidBodyGroup in {"E","F","G","H","I","J"}:
            # Use a reduced calibration matrix for rotations 
            self.rawFeatureTrainingData = np.tensordot(self.rawFeatureTrainingData,self.trainingCalibrationMatrix[0:3,0:3],axes = ([2],[0]))
            self.noBodyParts = len(self.rawFeatureTrainingData[0,:,0])
            # Reshape matrix to N_ x DOF N_ is number of timestamps in training set and DOF is number of degrees of freedom
            self.rawFeatureTrainingData = self.rawFeatureTrainingData.reshape(-1,self.noBodyParts*3)
        else:
            # Use a full calibration matrix for rotations and positions
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
            controlIdx = simpleBodyParts[self.trainingBodyParts.index(self.controlBodyPartIdx)]
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1

        elif rigidBodyGroup == "C":
            lHandIdx = rigidBodyParts.index("LHand")
            controlIdx = self.trainingBodyParts.index(lHandIdx)
            print(controlIdx)
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1
        
        elif rigidBodyGroup == "D":
            rHandIdx = rigidBodyParts.index("RHand")
            controlIdx = rHandIdx
            print(controlIdx)
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,controlIdx,:].reshape(-1,1,6)
            self.noBodyParts = 1
        
        # Decoders to decode from rotation - as this gets rid of offset bias
            
        elif rigidBodyGroup == "E":
            # Decode from rotations of all body parts except right hand

            # find the index of the body part in the list of non redundant bodies
            delIdx = self.testBodyParts.index(self.controlBodyPartIdx)
            # delete this index from the list of non redundant bodies
            del self.testBodyParts[delIdx]

            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,self.testBodyParts,:]
            # we need to delete the control index as this will be what we are trying to find
            self.noBodyParts = len(self.testBodyParts)


            # Extract the rotations only
            self.rawFeatureTestData = self.rawFeatureTestData[:,:,3:] 

            


        
        
        elif rigidBodyGroup == "F":
            # # # angles only, use all except right side

            # Extract data from all body parts
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of right hand on principal skeleton
            idxRightHand = renderingBodyParts.index('RHand') * 3

            # Find index of right shoulder on principal skeleton
            idxRightShoulder = renderingBodyParts.index('RShoulder') * 3

            # Retrieve all rigid body rotations for all timestamps
            self.rawFeatureTestData = self.rawFeatureTestData[:,:,3:].reshape(-1,19*3)
            
            # Delete rigid bodies on the right side
            self.rawFeatureTestData = np.delete(self.rawFeatureTestData,slice(idxRightShoulder,idxRightHand+3,1),1)

            # Reshape into N x m x DOF
            self.rawFeatureTestData = self.rawFeatureTestData.reshape(-1,15,3)

        

        elif rigidBodyGroup == "G":
            # # # Angles only: only get the left hand

            # Extract data from all body parts
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of left hand in principal rigid bodies
            idxLeftHand = renderingBodyParts.index('LHand') 

            # Extract only the left hand rotations for test sets
            self.rawFeatureTestData = self.rawFeatureTestData[:,idxLeftHand,3:].reshape(-1,1,3)


        elif rigidBodyGroup == "H":
            # # # only get the right hand

            # Extract data from all body parts
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,:]

            # Find index of right hand in principal rigid bodies
            idxRightHand = renderingBodyParts.index('RHand') 

            # Extract only right hand rotations 
            self.rawFeatureTestData = self.rawFeatureTestData[:,idxRightHand,3:].reshape(-1,1,3)

        elif rigidBodyGroup == "I":
            # # # Only use the lower body
            # # # angles only

            # Extract rotations from all body parts
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,3:]

            # Find index of left thigh on principal skeleton as this is start of lower bodies
            idxLeftThigh = renderingBodyParts.index('LThigh') 

            # Find index of right foot on principal skeleton as this is end of lower bodies
            idxRightFoot = renderingBodyParts.index('RFoot') 
            
            # Extract data from specific rigid bodies
            self.rawFeatureTestData = self.rawFeatureTestData[:,idxLeftThigh:idxRightFoot+1,:]
            

            


        
        elif rigidBodyGroup == "J":
            # # # Only use the upper body ( excludes upper left and right)
            # # # angles only

            # Find index of neck on principal skeleton as this is start of upper body
            idxNeck = renderingBodyParts.index('Neck') 

            # Find index of head on principal skeleton as this is end of upper body
            idxHead = renderingBodyParts.index('Head')
            
            # Extract rotations from all body parts
            self.rawFeatureTestData = self.testDataGameEngine.allBodyPartsDatastore[:,simpleBodyParts,3:]

            # Extract data from specific rigid bodies
            self.rawFeatureTestData = self.rawFeatureTestData[:,idxNeck:idxHead+1,:]

        # Transform the test data to the correct plane using the calibration matrix
        if self.rigidBodyGroup in {"E","F","G","H","I","J"}:
            # Use a reduced calibration matrix for rotations 
            self.rawFeatureTestData = np.tensordot(self.rawFeatureTestData,self.testCalibrationMatrix[0:3,0:3],axes = ([2],[0]))
        
            # Reshape matrix to N_ x DOF N_ is number of timestamps in test set and DOF is number of degrees of freedom
            self.rawFeatureTestData = self.rawFeatureTestData.reshape(-1,self.noBodyParts*3)
        else:
            # Use a full calibration matrix for rotations and positions
            self.rawFeatureTestData = np.tensordot(self.rawFeatureTestData,self.testCalibrationMatrix,axes = ([2],[0]))

            # Reshape matrix to N_ x DOF N_ is number of timestamps in test set and DOF is number of degrees of freedom
            self.rawFeatureTestData = self.rawFeatureTestData.reshape(-1,self.noBodyParts*6)
        
        self.testSamples = len(self.rawFeatureTestData[:,0])
    
    def retrieveTrainingOutputs(self):
        self.outputTrainingData = self.trainingDataGameEngine.cursorVelocityWriteDatastore[2:,:]
    
    def retrieveTestOutputs(self):
        self.outputTestData = self.testDataGameEngine.cursorVelocityWriteDatastore[2:,:]

    def extractFinalCalibrationIndexes(self):
        self.testFinalCalibrationIdx = self.testDataGameEngine.calibrationLastRecording
        self.trainingFinalCalibrationIdx = self.trainingDataGameEngine.calibrationLastRecording
        
    def normaliseDatasets(self,byVariance = False,delCalibrationData = True,normaliseByOffsetOnly = True,normaliseByRangeOnly = False, skipNormalisation = False,applyNormalisationToOutputs = False):
        
        # Delete the calibration data from the start of the features
        if delCalibrationData:
            self.deleteCalibrationInformation()

        # Normalise features training and test data
        self.featureTrainingData,self.featureTrainingDataDOFMeans = self.normaliseData(self.rawFeatureTrainingData,byVariance,normaliseByOffsetOnly = normaliseByOffsetOnly,normaliseByRangeOnly = normaliseByRangeOnly,skipNormalisation=skipNormalisation)
        self.featureTestData, self.featureTestDataDOFMeans = self.normaliseData(self.rawFeatureTestData,byVariance,useTrainedDOFMeans = True,normaliseByOffsetOnly = normaliseByOffsetOnly,normaliseByRangeOnly = normaliseByRangeOnly,skipNormalisation=skipNormalisation)
        
        if applyNormalisationToOutputs:
            self.outputTrainingData, self.outputTrainingDataDOFMeans = self.normaliseData(self.outputTrainingData,byVariance,useTrainedDOFMeans = True,normaliseByOffsetOnly = normaliseByOffsetOnly,normaliseByRangeOnly = normaliseByRangeOnly,skipNormalisation=skipNormalisation)
            self.outputTestData, self.outputTestDataDOFMeans = self.normaliseData(self.outputTestData,byVariance,useTrainedDOFMeans = True,normaliseByOffsetOnly = normaliseByOffsetOnly,normaliseByRangeOnly = normaliseByRangeOnly,skipNormalisation=skipNormalisation)
    
    def normaliseData(self,data,byVariance = True,useTrainedDOFMeans = False,normaliseByOffsetOnly = False,normaliseByRangeOnly = False,skipNormalisation = False):
        """
        Normalises data by mean and optionally by variance 

        Args:
            @bool byVariance: normalise data by variance if True (default False)
            TODO: code functionality for normalising by variance as well
        """
        if skipNormalisation:
            self.normalisationMethod = None
            return data, -1
        
        if normaliseByRangeOnly:
            # This simply normalises the range of each column to be between 0 and 1 , storing
            # the min and max values for use in the closed loop decoder
            self.normalisationMethod = "Range"
            normaliserRanges = []
            normalisedData = data.copy()

            # Loop through each column and normalise
            for DOF in range(data.shape[1]):

                # Fetch the min and max values and store
                maxDOF = max(data[:,DOF])
                minDOF = min(data[:,DOF])
                normaliserRanges.append([minDOF,maxDOF])

                # Renormalise data to be between 0 and 1
                normalisedData[:,DOF] = (normalisedData[:,DOF] - minDOF) / (maxDOF - minDOF)

            # Return the normalised data and store each range in dof means 
            return normalisedData, normaliserRanges
                
        
        if normaliseByOffsetOnly:
            # Subtract all position based offsets
            normalisedData = data.copy()
            startingPositions = []
            for DOF in range(data.shape[1]):
                startingDOFPos = normalisedData[0,DOF]
                startingPositions.append(startingDOFPos)
                normalisedData[:,DOF] -= startingDOFPos
            
            self.normalisationMethod = "Offset"
            return normalisedData, startingPositions

        if byVariance == False:
            normalisedData = data.copy()

            # Find the mean for each DOF across all times
            DOFmeans = np.average(data,axis = 0)

            if useTrainedDOFMeans:
                print("Using training DOF means for normalisation of test set")
                DOFmeans = self.featureTrainingDataDOFMeans
                # Use the training means

            # Subtract the mean for each DOF across all times
            for dof,mean in enumerate(DOFmeans):
                normalisedData[:,dof] = normalisedData[:,dof] - mean
            
            # Check means of data are now 0
            if not useTrainedDOFMeans:
                assert all(abs(np.average(normalisedData,axis = 0)) < 0.0001)
            else:
                print(abs(np.average(normalisedData,axis = 0)))

        else:
            scaler = StandardScaler()
            normalisedData = scaler.fit_transform(data)
        
        return normalisedData, DOFmeans
    
    def deleteCalibrationInformation(self):
        self.rawFeatureTrainingData = self.rawFeatureTrainingData[self.trainingFinalCalibrationIdx+1:,:]
        self.rawFeatureTestData = self.rawFeatureTestData[self.testFinalCalibrationIdx+1:,:]

    def performLinearRegression(self,type = "linear",alpha = None):
        """
        Fits a model to the data 
        Args:
            @param: type: defines the model used: "linear", "ridge"
            @param: alpha: defines the weight of the penaliser term in ridge regression, set to none if not using ridge 
        """

        # Fit linear model to data
        if type == "linear":
            self.reg  = linear_model.LinearRegression().fit(self.featureTrainingData, self.outputTrainingData)
        
        # Fit ridge model to data
        elif type == "ridge":
            
            # Initialise the model
            self.reg = linear_model.Ridge(alpha = alpha)
            # Fit the model
            self.reg.fit(self.featureTrainingData, self.outputTrainingData)

    def gatherPredictions(self):
        self.testVelPredict = self.reg.predict(self.featureTestData)
    
    def exportPredictions(self,fileName):
        np.savez(fileName,predVelocities=self.outputTestData)
    
    def createNormaliserForClosedLoop(self):
        """
        Creates the function that decides how to normalise closed loop raw data and also picks correct set of rigid bodies
        """
        # First save the rigid body group to the reg object for export
        self.reg.normalisationMethod = self.normalisationMethod
        self.reg.rigidBodyGroup = self.rigidBodyGroup
        self.reg.normalise = normalise
        self.reg.decoderType = self.rigidBodyGroup
        self.reg.decoderMeans = self.featureTrainingDataDOFMeans
        
    

def normalise(reg,tmpRigBodyArray):
    """
    Function that will be exported for use in closed loop to normalise and pick correct set of rigid bodies
    """
    # First pick the correct set of rigid bodies

    # Convert to a 1D array of DOFs
    tmpRigBodyArray = tmpRigBodyArray.reshape(-1)


    if reg.decoderType == "A":
        # Decoder A : pos + rot; all rigid bodies bar hand

        # Index of right hand in principal set of rigid bodies
        idxRightHand = 12 * 6

        # Extract all rigid body data bar right hand 
        tmpArray = np.zeros(108)
        tmpArray[0:idxRightHand] = tmpRigBodyArray[0:idxRightHand,0]
        tmpArray[idxRightHand:] = tmpRigBodyArray[idxRightHand+6:,0]

    elif reg.decoderType == "B":
        # Decoder B : pos + rot; all rigid bodies bar right side

        # Index of first right rigid body
        startIndex = 9 * 6

        # Index of last right rigid body
        endIndex = 12 * 6 + 6

        # Delete all right rigid bodies from data
        tmpArray = tmpRigBodyArray.copy()
        tmpArray = np.delete(tmpArray,slice(startIndex,endIndex,1),0)
    
    elif reg.decoderType == "C":
        # Decoder C : pos + rot; left hand only

        # Index of left hand
        idxLeftHand = 8 * 6

        # Extract left hand data 
        tmpArray = tmpRigBodyArray[idxLeftHand:idxLeftHand+6]

    elif reg.decoderType == "D":
        # Decoder D : pos + rot; right hand only

        # Right hand index
        idxRightHand = 12 * 6

        # Extract right hand only
        tmpArray = tmpRigBodyArray[idxRightHand:idxRightHand+6]
    
    elif reg.decoderType == "E":
        # Decoder E : rot only ; all rigid bodies bar hand

        # Right hand index
        idxRightHand = 12 * 3

        # Extract all data bar right hand
        tmpArray = np.zeros(18*3)
        tmpArray[0:idxRightHand] = tmpRigBodyArray[0:idxRightHand]
        tmpArray[idxRightHand:] = tmpRigBodyArray[idxRightHand+3:]


    elif reg.decoderType == "F":
        # Decoder F : rot only; all rigid bodies bar right side

        # Index of first right rigid body
        startIndex = 9 * 3

        # Index of last right rigid body
        endIndex = 12 * 3 + 3

        # Delete all right side data 
        tmpArray = tmpRigBodyArray.copy()
        tmpArray = np.delete(tmpArray,slice(startIndex,endIndex,1),0)

    
    elif reg.decoderType == "G":
        # Decoder G : rot only; left hand only

        # Find index of left hand and only decode from those rotations
        idxLeftHand = 8 * 3
        tmpArray = tmpRigBodyArray[idxLeftHand:idxLeftHand+3]
        

    elif reg.decoderType == "H":
        # Decoder H : rot only; right hand only 

        idxRightHand = 12 * 3
        tmpArray = tmpRigBodyArray[idxRightHand:idxRightHand+3]

    
    elif reg.decoderType == "I":
        # Decoder I : rot only; lower rigid bodies

        # Lower rigid body start index
        startIndex = 13 * 3

        # Lower rigid body end index
        endIndex = 18 * 3 + 3



        tmpArray = tmpRigBodyArray.copy()
        tmpArray = tmpArray[startIndex:endIndex]
    
    elif reg.decoderType == "J":
        # Decoder A : rot only; head and neck only
        # Find index of Neck and Head and only decode from those rotations

        # Neck Idx
        startIndex = 3 * 3

        # Head Idx
        endIndex = 4 * 3 + 3

        tmpArray = tmpRigBodyArray.copy()
        tmpArray = tmpArray[startIndex:endIndex]

    
    # NEXT STAGE: Normalisation
    if reg.normalisationMethod == None:
        return tmpArray
    elif reg.normalisationMethod == "Range":
        
        # transform array to be in range, 0 to 1 based on training data
        for DOF in range(0, len(tmpArray)):
            tmpArray[DOF] = (tmpArray[DOF] - reg.decoderMeans[DOF][0] ) / (reg.decoderMeans[DOF][1] - reg.decoderMeans[DOF][0])

        # transform to be between -1 and 1 for use in real time game
        
        return tmpArray
    elif reg.normalisationMethod == "Offset":

        tmpArray = tmpArray - reg.decoderMeans

        return tmpArray

