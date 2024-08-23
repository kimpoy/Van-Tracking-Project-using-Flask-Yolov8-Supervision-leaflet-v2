from flask import Flask, render_template, Response,jsonify,request,session,url_for
import cv2
import argparse
from ultralytics import YOLO
import supervision as sv
import numpy as np
from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import keyboard
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = ['KIM']

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    def __repr__(self):
        return '<ID %r>' % self.id
    
class Sales(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    cash = db.Column(db.Integer)
    def __repr__(self):
        return '<ID %r>' % self.id
""" with app.app_context():
    db.create_all() """

ZONE_POLYGON = np.array([
    [0,0],
    [1280 // 2,0],
    [1250 // 2,720],
    [0,720],
])


def parse_arguments()->argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution",
        default=[1280,720],
        nargs=2,
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    #frame resolution
    args = parse_arguments()
    frame_width,frame_height = args.webcam_resolution

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)
    x,y,w,h = 10,10,200,50

    model = YOLO("yolov8n.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone = sv.PolygonZone(polygon=ZONE_POLYGON,frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone,
        color = sv.Color.blue(),
        thickness=2,
        text_thickness=4,
        text_scale=2
        )

    while True:
        global total_passenger
        ret, frame = cap.read()
        #result = model(frame) #with no supervision
        #result = model(frame)[0] #with supervision
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        detections = detections[detections.class_id == 0]
        #detections = sv.Detections.from_ultralytics(result)

        counter_frame = frame

        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _ 
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
            )
        
        #sample = zone.trigger(detections=detections)
        sample = zone.trigger(detections=detections)
        #counting the number
        #print(len(sample))
        frame = zone_annotator.annotate(scene=frame)
        total = len(list(filter(None,sample)))

        cv2.rectangle(counter_frame, (x, x), (x + w, y + h), (0,0,0), -1)
        cv2.putText(counter_frame, f'Total:{total}', (x + int(w/10),y + int(h) - int(h/3)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 4)
        
        #debounce = False
        #if keyboard.is_pressed('a') and debounce == False and total == 1: 
        #    debounce = True
        #    #10 passenger with 50 pesos fare
        #    try:
        #        print('fare added for all passenger') 
        #        time.sleep(.5)
        #        debounce = False
        # 
        #    except:
        #        return "error"
        #    
        #if keyboard.is_pressed('s') and debounce == False and total == 1: 
        #    debounce = True
        #    print('added 1 discounted fare for all passenger') 
        #    time.sleep(.5)
        #    debounce = False
        #if keyboard.is_pressed('d') and debounce == False: 
        #    debounce = True
        #    print('1 discounted added') 
        #    time.sleep(.5)
        #    debounce = False
        #if keyboard.is_pressed('f') and debounce == False: 
        #    debounce = True
        #    print('pick up fare added') 
        #    time.sleep(.5)
        #    debounce = False

        total_passenger = total
        
        yield frame
        #cv2.imshow("yolov8",frame)
        #cv2.imshow("image",frame)
        #print(frame.shape)

        #if cv2.waitKey(30) == 27:
        #    break

def generate_frames():
    yolo_output = main()
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
@app.route('/', methods=['GET','POST'])
def index():
    session.clear()
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    session.clear()
    return render_template('register.html')

@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('index.html')

@app.route("/video", methods=['GET','POST'])
def webcam():
    session.clear()
    return render_template('video.html')

@app.route("/gps", methods=['GET','POST'])
def gps():
    session.clear()
    return render_template('gps.html')
@app.route("/earnings", methods=['GET','POST'])
def earnings():
    session.clear()
    return render_template('earnings.html')


# To display the Output Video on Webcam page
@app.route('/webapp')
def webapp():
    #return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save')
def save():
    price = 100
    discount = 20
    discounted_price = price - (100 * .2)
    discounted_passenger = 0
    while True:
        
        if keyboard.is_pressed('a'):
            print("Key pressed")
            if total_passenger >= 1:
                normal_fare_passenger = total_passenger - discounted_passenger
                tcash = (discounted_passenger * discounted_price) + (normal_fare_passenger * price)
                new_task = Sales(cash=tcash)
                db.session.add(new_task)
                db.session.commit()
                discounted_passenger = 0
                time.sleep(3)
        if keyboard.is_pressed('s') and not total_passenger > 4:
            discounted_passenger += 1
            time.sleep(3)
        else:
            time.sleep(0.01)
    
if __name__ == "__main__":
    app.run(debug=True)