from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
import urllib.request
import os
from werkzeug.utils import secure_filename
# from run import database
import numpy as np
import base64
#from run import retrival_main, retrival_small, device, model, key_main, value_main
from database import filter
from extract_object import label_function, filter_function
import pandas as pd
from correct import keys,values
import glob as glob
from bbb import function_search_video, function_search_text, bigdata
from numpy import genfromtxt


# change = dict(zip(keys,values))
# database_main = dict(zip(key_main,value_main))


label_update = []
output_update = [bigdata]
app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
app.config['RESULT_FOLDER'] = UPLOAD_FOLDER+"outputs/"
recommend = []

@app.route('/')
def fetchAPI():
    return render_template("retrieve_new.html",normal_text = 'Keywords')


@app.route('/', methods=['POST'])
def job():
 text = request.form.get('textsubmit',False)
 if text:
  if text=='u':    
    label_update.clear()
    output_update.clear()
    output_update.append(bigdata)
    recommend.clear()
    return render_template("retrieve.html",normal_text = 'Keywords')
    
 text = request.form.get('text',False)
 if text:    
    output = filter_function(text, label_data = label_update[-1], output_update = output_update[-1])
    label_update.append(label_function(output))
    recommend.append(','.join(label_update[-1]))
    output_update.append(output)
    dict = []
    submit = []
    for i in output:
      submit.append({'video':i.split('/')[1]+'.mp4','key_frame':change[i.split('/')[1]+'/'+i.split('/')[2]]})
    data = [[i['video'],i['key_frame']] for i in submit]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1,"video":i.split('/')[1],'key_frame':i.split('/')[2].split('.')[0] })
    return render_template("retrieve.html",normal_text = recommend[-1],image_names=dict)
 
 text = request.form.get('text1',False)
 if text: 
    output = retrival_main(text)
    output_update.append(output)
    label_update.append(label_function(output))
    recommend.append(','.join(label_update[-1]))
    dict = []
    submit = []
    for i in output:
      submit.append({'video':i.split('/')[1]+'.mp4','key_frame':change[i.split('/')[1]+'/'+i.split('/')[2]]})
    data = [[i['video'],i['key_frame']] for i in submit]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1,"video":i.split('/')[1],'key_frame':i.split('/')[2].split('.')[0] })
    return render_template("retrieve.html",normal_text=recommend[-1],image_names=dict)
 
 text = request.form.get('text2',False)
 if text: 
    feature_correspond = np.array([database_main[i] for i in output_update[-1]])
    retrival_new = retrival_small(output_update[-1],feature_correspond,device,model)
    output = retrival_new(text)
    output_update.append(output)
    label_update.append(label_function(output))
    recommend.append(','.join(label_update[-1]))
    dict = []
    submit = []
    for i in output:
      submit.append({'video':i.split('/')[1]+'.mp4','key_frame':change[i.split('/')[1]+'/'+i.split('/')[2]]})
    data = [[i['video'],i['key_frame']] for i in submit]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1,"video":i.split('/')[1],'key_frame':i.split('/')[2].split('.')[0] })
    return render_template("retrieve.html",normal_text=recommend[-1],image_names=dict)
   
 text = request.form.get('text3',False) 
 if text: 
    output = function_search_video(text)
    output_update.append(output)
    label_update.append(label_function(output))
    recommend.append(','.join(label_update[-1]))
    dict = []
    submit = []
    for i in output:
      submit.append({'video':i.split('/')[1]+'.mp4','key_frame':change[i.split('/')[1]+'/'+i.split('/')[2]]})
    data = [[i['video'],i['key_frame']] for i in submit]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1,"video":i.split('/')[1],'key_frame':i.split('/')[2].split('.')[0] })
    return render_template("retrieve.html",normal_text=recommend[-1],image_names=dict)
   
 text = request.form.get('text4',False) 
 if text: 
    output = function_search_audio(text, output_update[-1])
    output_update.append(output)
    label_update.append(label_function(output))
    recommend.append(','.join(label_update[-1]))
    dict = []
    submit = []
    for i in output:
      submit.append({'video':i.split('/')[1]+'.mp4','key_frame':change[i.split('/')[1]+'/'+i.split('/')[2]]})
    data = [[i['video'],i['key_frame']] for i in submit]
    file = pd.DataFrame(data=data)
    file.to_csv('result.csv',header=None,index=None)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1,"video":i.split('/')[1],'key_frame':i.split('/')[2].split('.')[0] })
    return render_template("retrieve.html",normal_text=recommend[-1],image_names=dict)

@app.route("/modal",methods=["GET"])
def show_modal():
    dict=[]
    args=request.args
    frame_id = args.get("frame_id").zfill(6)
    frames = glob.glob("KeyFramesC00_V00/"+args.get("video")+"/*.jpg")
    frame_idx_vid = frames.index("KeyFramesC00_V00/"+args.get("video")+"\\"+frame_id+".jpg")
    prev_idx = max(frame_idx_vid-10,0)
    after_idx= min(frame_idx_vid+10,len(frames))
    for idx in range(prev_idx,after_idx):
        with open(frames[idx], "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'id':change[frames[idx].split('\\')[0].split('/')[1]+'/'+frames[idx].split('\\')[1]]})
    return jsonify({"htmlresponse":render_template("modal_nearframe.html",image_names=dict)})

@app.route("/toTop1",methods=["GET"])
def to_top1():
    data = pd.read_csv("result.csv", header=None)
    args = request.args
    # Delete the row in the result
    data.drop(data.index[int(args.get("current_rank"))-1],axis=0,inplace=True)
    # Append the row to the top of the result
    data.loc[-1] = [args.get("video")+".mp4", args.get("frame_id")]
    data.index = data.index+1
    data.sort_index(inplace=True)
    data.to_csv("result.csv",index=False, header=False)

    return render_template("retrieve.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)