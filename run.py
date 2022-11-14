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
import pickle


class retrival_small():
  def __init__(self,input_frame,input_features,device,model):
    self.input_frame = input_frame
    self.input_features = input_features
    self.number_neighbors = len(input_frame) if len(input_frame)<100 else 100
    self.index = pynndescent.NNDescent(input_features)
    self.model = model
    self.device = device

  def __call__(self,input_text):
    text = clip.tokenize([input_text]).to(self.device)
    with torch.no_grad():
       text_features = self.model.encode_text(text)
    text_features = text_features[0].cpu().detach().numpy().reshape(1,-1)
    index = self.index
    neighbors = index.query(text_features,self.number_neighbors)
    output = [self.input_frame[i] for i in neighbors[0][0]]
    return output

class retrival_main():
  def __init__(self,input_frame,input_features,device,model):
    self.input_frame = input_frame
    self.input_features = input_features
    self.number_neighbors = 100
    with open("index", "rb") as fp:  # Unpickling
      self.index = pickle.load(fp)
    self.model = model
    self.device = device

  def __call__(self,input_text):
    text = clip.tokenize([input_text]).to(self.device)
    with torch.no_grad():
       text_features = self.model.encode_text(text)
    text_features = text_features[0].cpu().detach().numpy().reshape(1,-1)
    index = self.index
    neighbors = index.query(text_features,self.number_neighbors)
    output = [self.input_frame[i] for i in neighbors[0][0]]
    return output

def make_features_images(features_path,images_path):
  images_database = []
  features_dir = os.listdir(features_path)
  features_dir.sort()
  features_database = []
  for dir in features_dir:
    dir = features_path + '/'+ dir  
    feature = np.load(dir)
    shape = feature.shape[0]
    for i in range(shape):
      features_database.append(feature[i])
  images_dir = os.listdir(images_path)
  images_dir.sort()
  for i in images_dir:
      dir = images_path + '/' + i
      for j in os.listdir(dir):
         images_database.append(dir+'/'+j)
  return np.array(features_database),images_database

features_path = 'CLIPFeatures_C00_V00'
image_path = 'KeyFramesC00_V00'

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/16", device=device)


# database = make_features_images(features_path,image_path)
# with open("database", "wb") as fp:  # Pickling
#   pickle.dump(database, fp)
with open("database", "rb") as fp:  # Unpickling
  database = pickle.load(fp)
key_main = database[1]
value_main = list(database[0])
# print("run1")
# index = pynndescent.NNDescent(database[0])
# with open("index", "wb") as fp:  # Pickling
#   pickle.dump(index, fp)

retrival_main = retrival_main(database[1],database[0],device,model)
