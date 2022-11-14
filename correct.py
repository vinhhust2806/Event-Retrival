import pandas as pd
import numpy as np
import os
import glob
import pickle
change = {}
#
# for k in os.listdir('Keyframe_P_C0_V00/keyframe_p'):
#   csv = pd.read_csv('Keyframe_P_C0_V00/keyframe_p/'+k,header=None)
#   for i in np.array(csv):
#     print(i)
#     change[k.split('.')[0]+'/'+i[0]] = i[1]
# with open("correct", "wb") as fp:  # Pickling
#   pickle.dump(change, fp)
with open("correct", "rb") as fp:  # Unpickling
  change = pickle.load(fp)
keys = list(change.keys())
values = list(change.values())




