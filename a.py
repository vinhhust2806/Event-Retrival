#imgpath = request.args.get('imgpath')
import cv2
import base64
#image = cv2.imread('static/outputs/005522.jpg')

with open("static/outputs/005522.jpg", "rb") as img_file:
    #print()
    a = base64.b64encode(img_file.read()).decode('utf-8')
    #print(a)
#print(a)
#print(a[2:-1])
#print(a)
