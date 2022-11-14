import os

path = 'KeyFramesC00_V00'
a = os.listdir(path)
a.sort()
a = [path+'/'+i for i in a]
for j in a:
    k = os.listdir(j)
    k.sort()
    k = [j+'/'+h for h in k]
filter = {'police':k[0:100],'man':k[90:150]}

print(list(set(filter['man'])&set(filter['police'])))

import glob
import json
import numpy as np

def findImagesByObjects(arr):
    paths = glob.glob("ObjectNPArray/*/*.npy")
    obj_id = json.load(open("obj_id.json"))
    val_list = list(obj_id.values())
    key_list = list(obj_id.keys())
    id = key_list[val_list.index(arr[0])]
    print(arr[0], id)
    for path in paths:
        print(path)
        data = np.load(path)
        if arr[1] == len(np.where(data==id)[0]):
            print("True: ", path)


# findImagesByObjects(["Car",2])

def mappingClassName2Label():
    mapping = {}
    paths = glob.glob("ObjectsC00_V00/*/*.json")
    for path in paths:
        print(path)
        f = open(path)
        data = json.load(f)
        for class_Name, id in zip(data["detection_class_entities"],data["detection_class_labels"]):
            try:
                mapping[id] = class_Name
            except Exception as e:
                print("Exception: ",e)
    print(mapping)

# mappingClassName2Label()
def convertObject2Numpy():
    paths = glob.glob("ObjectsC00_V00/*/*.json")
    for path in paths:
        video_name = path.split("\\")[1]
        frame = path.split("\\")[2].split(".")[0]
        print(path)
        f = open(path)
        data = json.load(f)
        arr = np.array(data["detection_class_labels"])
        # Mkdir:
        if not os.path.exists("ObjectNPArray/"+video_name):
            os.mkdir("ObjectNPArray/"+video_name)
        with open("ObjectNPArray/"+video_name+"/"+frame+'.npy', 'wb') as f:
            np.save(f,arr)

# convertObject2Numpy()

def makeMetaObjectData():
    object_files = json.load(open("obj_id.json"))
    object_ids = object_files.keys()
    paths = glob.glob("ObjectsC00_V00/*/*.json")
    for object_id in object_ids:
        data = []
        for path in paths:

            video_name = path.split("\\")[1]
            frame = path.split("\\")[2].split(".")[0]
            file_objects = json.load(open(path))["detection_class_labels"]

            if object_id in file_objects:
                arr=[file_objects.count(object_id), video_name, frame]
                print(arr)
                data.append(arr)
        with open("ObjectFolder/"+object_id+".npy","wb") as f:
            np.save(f,np.array(data))
# makeMetaObjectData()
def lookNPY(npyPath):
    print(np.load(npyPath))
import pickle
def searchObjectDatabase(object_id, object_number):
    # with open("database", "rb") as fp:  # Unpickling
    #     database = pickle.load(fp)
    #     frame=database[1]
    #     value = database[0]


    try:
        arr = np.load("ObjectFolder/"+object_id+".npy")
        index = np.where(arr[:,0]==str(object_number))

        print("Finding videos for object ",object_id,": ",arr[index])
    except:
        print("The object cannot be found!")
    return arr[index]
# lookNPY("E:/Downloads/HCMAIChallenge/AI-Challenge/ObjectFolder/1.npy")

# searchObjectDatabase("1",1)
