import glob
import numpy as np
dir_files = glob.glob("E:\Downloads\C000_scripts-20221022T084022Z-001/*")
txt_files = []
sentences = []
for dir in dir_files:
  temp = glob.glob(dir+"/*.txt")
  for txt_file in temp:
    txt_files.append(txt_file)
    f = open(txt_file, encoding="utf8")
    sentences.append(f.read())

init_idxs = np.arange(len(sentences))
def simpleSearch(keyword, idxs):
    out_idx = []
    for sentence_idx in idxs:
        if(sentences[sentence_idx].find(keyword))!=-1:
            out_idx.append(sentence_idx)
            print("Keyword: ",keyword,txt_files[sentence_idx])
    return out_idx

simpleSearch("U19",simpleSearch("Brunei", init_idxs))