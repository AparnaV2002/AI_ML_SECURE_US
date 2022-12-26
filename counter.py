
from multiprocessing.sharedctypes import Value
from typing import List
import json
from flask import Flask,Response,render_template,request,make_response
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0)

locations=[{
    "location":"12345",
    "phone_no":"123456789"
},
{
    "location":"123456",
    "phone_no":"12345678"
},
{
    "location":"123457",
    "phone_no":"1234567"
},{
    "location":"123458",
    "phone_no":"123456"
},{
    "location":"123459",
    "phone_no":"12345"
}]

data1=json.dumps(locations)
data1=json.loads(data1)
print(type(data1))
def generate_frames():
    currentframe = 0
    while True:          
        ## read the camera frame
        success,frame=camera.read()
        cv2.imwrite('Frame' + str(currentframe) + '.jpg', frame)
        if currentframe<=4:
                currentframe+=1
        else:
            pass
        if not success:
            break
        else:
            

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
        

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Frame')
def img():
    img = cv2.imread('Frame'+request.args['value']+'.jpg')
    ret, jpeg = cv2.imencode('.jpg', img)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return  response

@app.route('/pincode')
def pincode():
    images=[]
    

    img = cv2.imread('Frame0.jpg')
    ret, jpeg = cv2.imencode('.jpg', img)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/png'
    images.append(response)
    print(images[0])
    a=next(x for x in data1 if x["location"] == request.args['pincode'])
    return render_template('pincode.html',num= a["phone_no"],img=images)
@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.debug = True
    app.run()
    





