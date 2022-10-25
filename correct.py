import pandas as pd
import numpy as np
import os

change = {}

for k in os.listdir('Keyframe_P_C0_V00/keyframe_p'):
  csv = pd.read_csv('Keyframe_P_C0_V00/keyframe_p/'+k)
  for i in np.array(csv):
    change[k.split('.')[0]+'/'+i[0]] = i[1]

keys = list(change.keys())
values = list(change.values())
