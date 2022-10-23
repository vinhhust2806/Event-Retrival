from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from run import database
import base64
from run import retrival
from database import filter
half = len(database)
output_update = []
update = []
app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
app.config['RESULT_FOLDER'] = UPLOAD_FOLDER+"outputs/"

@app.route('/')
def fetchAPI():
    return render_template("retrieve.html")


@app.route('/', methods=['POST'])
def job():
 text = request.form.get('text1',False)
 if text:
   if 'police' in text: 
    dict = []
    output = filter['police']
    update.append('police')
    if len(update)>1:
      output = list(set(output)&set(output_update[-1]))
    output_update.append(output)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
    return render_template("retrieve.html",image_names=dict)
 
 text = request.form.get('text',False)
 if text: 
    output = retrival(text)
    dict = []
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
    return render_template("retrieve.html",image_names=dict)
 
 text = request.form.get('text2',False)
 if text:
  if 'man' in text: 
    dict = []
    output = filter['man']
    update.append('man')
    if len(update)>1:
      output = list(set(output)&set(output_update[-1]))
    output_update.append(output)
    for id,i in enumerate(output):
        with open(i, "rb") as img_file:
           a = base64.b64encode(img_file.read()).decode('utf-8')
        dict.append({'path':"data:image/jpeg;base64,"+a,'rank':id+1})
    return render_template("retrieve.html",image_names=dict)

#@app.route('/', methods=['POST'])
#def my_form_post():
  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
