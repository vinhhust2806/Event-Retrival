import os
import numpy as np

def load_audio_list(folder):
    data = os.listdir(folder)
    data.sort()

    return
def search_word(word, audio_path_list):
    paths = []
    for path in audio_path_list:
        f = open(path,"r")
        if word.lower() in f.read().lower():
            paths.append(path)
    return paths
if __name__ == "__main__":
    current_dir = os.getcwd()
    folder = os.path.join(current_dir, "audio","Data_scripts","Total_scripts")
    # print(folder)
    filenames = os.listdir(folder)
    # print(filenames)
    audio_path_list = [os.path.join(folder, name) for name in filenames]
    paths = search_word("cubic 19", audio_path_list)
    print(paths)    
    