import torch
import clip
from PIL import Image
import os
import pynndescent
import numpy as np
import h5py
from urllib.request import urlretrieve
import matplotlib.pyplot as plt
import time
import pandas as pd

def make_database(features_path,image_path):
  features_dir = os.listdir(features_path)
  features_dir.sort()
  index_database = []
  features_database = []
  for dir in features_dir:
    dir = features_path + '/'+ dir  
    feature = np.load(dir)
    shape = feature.shape[0]
    index_database.append(shape)
    for i in range(shape):
      features_database.append(feature[i])
  image_database = os.listdir(image_path)
  image_database.sort()
  
  index_database = [np.sum(index_database[0:i]) for i in range(1,len(index_database)+1)]
  features_database = np.array(features_database)

  return index_database,features_database,image_database

class retrival():
  def __init__(self,model,database,number_neighbors,device,image_path):
    self.database = database
    self.number_neighbors = number_neighbors
    self.device = device
    self.model = model
    self.index = pynndescent.NNDescent(database[1])
    self.image_path = image_path
    self.output_dir = []
    self.output = []
  def __call__(self,input_text):
    text = clip.tokenize([input_text]).to(self.device)
    with torch.no_grad():
       text_features = self.model.encode_text(text)
    text_features = text_features[0].cpu().detach().numpy().reshape(1,-1)
    index = self.index
    start = time.time()
    neighbors = index.query(text_features,self.number_neighbors)
    end = time.time()
    print('Retrival time with',len(neighbors[0][0]),'neighbors is',end-start,' sec')
    output = []
    output_dir = []
    for neighbor in neighbors[0][0]:
      i = 0
      while self.database[0][i] < neighbor:
        i = i+1
      list_keyframes_inside = os.listdir(self.image_path+'/'+self.database[2][i])
      list_keyframes_inside.sort()
      output_dir.append(self.image_path +'/'+self.database[2][i]+'/'+list_keyframes_inside[neighbor-self.database[0][i]])

      output.append({'video':self.database[2][i]+'.mp4','key_frame':list_keyframes_inside[neighbor-self.database[0][i]].split('.')[0]})
    self.output_dir = output_dir
    self.output = output
    return output_dir
  def plot_results(self):
    plt.figure(figsize=(30,30))
    
    #for i in range(1,len(self.output_dir)+1):
    for i,image_path in enumerate(self.output_dir):
       plt.subplot(int(np.sqrt(len(self.output_dir)))+1,int(np.sqrt(len(self.output_dir))),i+1)
       image = Image.open(image_path).convert("RGB")
       plt.imshow(image)
       plt.title("Rank: "+str(i+1))

  def write_submit_file(self):
    data = [[i['video'],i['key_frame']] for i in self.output]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)


features_path = 'CLIPFeatures_C00_V00'
image_path = 'KeyFramesC00_V00'

database = make_database(features_path,image_path)
   
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)
number_neighbors = 100
retrival = retrival(model=model,database=database,number_neighbors=number_neighbors,device=device,image_path=image_path) 