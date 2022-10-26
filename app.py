from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
#from run import database
import numpy as np
import base64
from run import retrival_main, retrival_small, device, model, key_main, value_main
from database import filter
from extract_object import label_function, filter_function
import pandas as pd
from correct import keys,values

change = dict(zip(keys,values))
database_main = dict(zip(key_main,value_main))

output_update = []
label_update = []

app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
app.config['RESULT_FOLDER'] = UPLOAD_FOLDER+"outputs/"
recommend = []

@app.route('/')
def fetchAPI():
    return render_template("retrieve.html",normal_text = 'Keywords')


@app.route('/', methods=['POST'])
def job():
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
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
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
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
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
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
    return render_template("retrieve.html",normal_text=recommend[-1],image_names=dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
