from config_streaming import rigidBodyParts
import numpy as np
import pickle
import matplotlib.pyplot as plt

print(rigidBodyParts.index('RHand'))
print(2 in {1,2,3})
i = np.array([0,1,2,5])
j = np.array([0,2,4,5])

a =  np.concatenate([i,j],axis = 0)
print(a.shape)

with open("GameSaves/Ashwin_06_02__11_21_decoder_trial.pkl", 'rb') as file:
            oldGameEngine = pickle.load(file)

# Plot hand rotations variation
handPos1 = oldGameEngine.handPos1
handPos2 = oldGameEngine.handPos2
handPos3 = oldGameEngine.handPos3
cursorVelocity = oldGameEngine.cursorVelocityWriteDatastore

print(cursorVelocity.shape)
# # Plot the hand rotations
plt.plot(handPos1,label =  "0th rotation") 
plt.plot(handPos2,label =  "1st rotation - left/right") 
plt.plot(handPos3,label =  "2nd rotation - up/down") 
plt.legend()
plt.show()


plt.plot(cursorVelocity[200:300,0],cursorVelocity[200:300,1])
plt.show()