import numpy as np
import json
import os
import time
import objects_extraction

current_dir = os.getcwd()
test_dir = os.path.join(current_dir,"Data/ObjectsC00_V00", "C00_V0011")
print("Choosen json folders:", test_dir)
list_dir = os.listdir(test_dir)
list_dir.sort()

json_list = [os.path.join(test_dir, dir) for dir in list_dir]
json_list_np = np.asarray(json_list)

start = time.time()

unique_objs_np = objects_extraction.get_unique_json_objs_from_list(json_list=json_list_np)
# print(unique_objs_np)
retrieval_list = objects_extraction.retrieve_imgs_containing_obj(json_list_np, "Footwear")
print(retrieval_list)
end = time.time()
print("Time run:",end - start)
