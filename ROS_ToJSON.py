#!/usr/bin/env python
# import imp
import rospy
import cv2
from threading import Thread, Event
# from flask import Flask, render_template, Response
import signal, sys
# from cv_bridge import CvBridge
# from sensor_msgs.msg import Image
import random
from std_msgs.msg import Float32
from geometry_msgs.msg import Quaternion

from flask import Flask, request, session, g
from flask import render_template, flash
from flask import send_from_directory
from flask import jsonify

import time

frame = None
# bridge = CvBridge()
# event = Event()
oe = [0, 0 ,0 ,0, 0]

def DataRoda(data):
    global oe
    print ('Dari Ros : ', data)
    # print(oe)
    oe[0] = data.x
    oe[1] = data.y
    oe[2] = data.z
    oe[3] = data.w

    # oe[0] = random.randint(-100, 100)
    # oe[1] = random.randint(0, 100)
    # oe[2] =  random.randint(-100, 100)
    # oe[3] = random.randint(0, 100)

Thread(target=lambda: rospy.init_node('ros_ke_recv', disable_signals=True)).start()
rospy.Subscriber("/robot_riset/Motor/Feedback/Raw/rpm", Quaternion, DataRoda) 

app = Flask(__name__)


@app.route('/')
def index():
    global oe
    
    rpm1 = oe[0]
    rpm2 = oe[1]
    rpm3 = oe[2]
    rpm4 = oe[3]
    t = time.time()
    t_ms = int(t * 1000)
    oe[4] = t_ms

    return jsonify(oe)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 ,debug=True)
