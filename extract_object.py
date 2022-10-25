import json
# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from database import filter
#import tensorflow as tf

import matplotlib.pyplot as plt

def get_json_data(path):
    file = open(path)
    data = json.load(file)
    return data
def get_json_objs(json_data):
    boxes = np.array([[float(num) for num in box] for box in json_data["detection_boxes"]])
    class_names = json_data["detection_class_names"]
    scores = np.array([np.float32(i) for i in json_data["detection_scores"]])
    class_entities = json_data["detection_class_entities"]
    return boxes, class_names, scores, class_entities

def label_function(img_list, max_boxes=10, min_score=0.5):
    unique_objs = []
    json_list = frame2json(img_list)
    for json_file in json_list:
        data = get_json_data(json_file)
        boxes, _, scores, class_entities = get_json_objs(json_data=data)
        
        for i in range(min(boxes.shape[0], max_boxes)):
            if scores[i] >= min_score:
                if class_entities[i] not in unique_objs:
                    unique_objs.append(class_entities[i])
    unique_objs_np = np.asarray(unique_objs)                
    return unique_objs_np

def frame2json(frame_list):
    new_list = frame_list.copy()
    for i in range(len(new_list)):
        new_list[i] = 'ObjectsC00_V00' + '/'+ new_list[i].split('/')[1] + '/' + new_list[i].split('/')[2].split('.')[0] + '.json'
    return new_list

def filter_function(text_input, label_data, output_update):
    list_image_proper = []
    if text_input in label_data:
      for i in output_update:
        if text_input in get_json_objs(get_json_data(frame2json([i])[0]))[3]:
            list_image_proper.append(i)
    return list_image_proper




