from config_streaming import rigidBodyParts
import numpy as np
import pickle
import matplotlib.pyplot as plt

print(rigidBodyParts.index('RHand'))

i = [[0,1,2],[0,1,2]]
a = np.asarray(i)
print(a.shape)

with open("GameSaves/Ashwin_24_01__12_36_2min.pkl", 'rb') as file:
            oldGameEngine = pickle.load(file)
cursorVels = oldGameEngine.cursorVelocityWriteDatastore
dists = np.zeros(cursorVels.shape)
x = 1270//2
y = 740//2
for i in range(0,cursorVels.shape[0]):
        x = x + cursorVels[i,0] * 0.03
        y = y + cursorVels[i,1] * 0.03
        dists[i,:] = [x,y]
        
plt.plot(dists[:,0],dists[:,1])
plt.show()