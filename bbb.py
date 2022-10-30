import glob

def function_search_text(text,data_base):
    out = []
    for i in data_base:
        with open('Total_Scripts'+'/'+i.split('/')[1]+'.txt') as f:
            if text in f.read():
                out.append(i)
    return out

def function_search_video(video_name):
    p = glob.glob('KeyFramesC00_V00/'+video_name+'/'+'*.jpg')
    out = [i.replace('\\','/').replace('\\','/') for i in p]
    out = [i.replace('\\','/') for i in out]
    return out

bigdata = glob.glob('KeyFramesC00_V00/*/*.jpg')
bigdata = [i.replace('\\','/').replace('\\','/') for i in bigdata]
bigdata = [i.replace('\\','/') for i in bigdata]
