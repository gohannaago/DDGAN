"""
Code for rescaling velocity values
"""
#%%
#import dependencies
import numpy as np
import copy

#import dataset
set_1 = np.load("training_dataset/training_set_1.npy")
set_2 = np.load("training_dataset/training_set_2.npy")
set_3 = np.load("training_dataset/training_set_3.npy")
set_4 = np.load("training_dataset/training_set_4.npy")
set_5 = np.load("training_dataset/training_set_5.npy")
set_6 = np.load("training_dataset/training_set_6.npy")
set_7 = np.load("training_dataset/training_set_7.npy")
set_8 = np.load("training_dataset/training_set_8.npy")
set_9 = np.load("training_dataset/training_set_9.npy")
set_10 = np.load("training_dataset/training_set_10.npy")

#import minmax values
min_1 = -7.336326599121094
max_1 = 7.152307033538818
min_2 = -7.713073253631592
max_2 = 7.705145835876465
min_3 = -7.337389945983887
max_3 = 7.2488532066345215
min_4 = -7.687894821166992
max_4 = 7.010688781738281
min_5 = -7.267822265625
max_5 = 6.831949710845947
min_6 = -7.610045433044434
max_6 = 7.6747822761535645
min_7 = -6.930552005767822
max_7 = 7.635422229766846
min_8 = -7.500446319580078
max_8 = 7.646414756774902
min_9 = -7.403921604156494
max_9 = 7.485347747802734
min_10 = -7.368843078613281
max_10 = 7.52786111831665

print("Start Descale")
#descale sets
de_set_1 = set_1.copy()
de_set_1[:,:,:,:2] = (de_set_1[:,:,:,:2]*(max_1-min_1) + min_1)
de_set_2= set_2.copy()
de_set_2[:,:,:,:2] = (de_set_2[:,:,:,:2]*(max_2-min_2) + min_2)
de_set_3= set_3.copy()
de_set_3[:,:,:,:2] = (de_set_3[:,:,:,:2]*(max_3-min_3) + min_3)
de_set_4= set_4.copy()
de_set_4[:,:,:,:2] = (de_set_4[:,:,:,:2]*(max_4-min_4) + min_4)
de_set_5= set_5.copy()
de_set_5[:,:,:,:2] = (de_set_5[:,:,:,:2]*(max_5-min_5) + min_5)
de_set_6= set_6.copy()
de_set_6[:,:,:,:2] = (de_set_6[:,:,:,:2]*(max_6-min_6) + min_6)
de_set_7 = set_7.copy()
de_set_7[:,:,:,:2] = (de_set_7[:,:,:,:2]*(max_7-min_7) + min_7)
de_set_8 = set_8.copy()
de_set_8[:,:,:,:2] = (de_set_8[:,:,:,:2]*(max_8-min_8) + min_8)
de_set_9 = set_9.copy()
de_set_9[:,:,:,:2] = (de_set_9[:,:,:,:2]*(max_9-min_9) + min_9)
de_set_10 = set_10.copy()
de_set_10[:,:,:,:2] = (de_set_10[:,:,:,:2]*(max_10-min_10) + min_10)

print("make into one set")
# sum all sets into one
full_set = np.concatenate((de_set_1, de_set_2, de_set_3, de_set_4, de_set_5, de_set_6, de_set_7, de_set_8, de_set_9, de_set_10))
print(full_set.shape)

# Scale velocity values in full_set
print("rescaling full set")
max_vel = np.amax(full_set[:,:,:,:2])
min_vel = np.amin(full_set[:,:,:,:2])

scale = 1/(max_vel- min_vel)
print("full_set.npy : min_vel = ", min_vel, " , max_vel = ", max_vel, " , vel_scaling = ", scale)

full_set[:,:,:,:2] = scale*(full_set[:,:,:,:2]-min_vel)

np.save("full_set.npy", full_set)