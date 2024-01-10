from config_streaming import rigidBodyParts
import numpy as np
import pickle

print(rigidBodyParts.index('RHand'))

i = [[0,1,2],[0,1,2]]
a = np.asarray(i)
print(a.shape)

with open("GameSaves/Ashwin_09_01__17_05.pkl", 'rb') as file:
            oldGameEngine = pickle.load(file)
print(oldGameEngine.allBodyPartsDatastore.shape)