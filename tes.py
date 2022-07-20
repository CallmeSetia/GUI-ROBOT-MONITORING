from ast import Import
import sys
import time
import logo_rc
import random

from threading import Thread
# import pyqtgraph as pg
# import numpy as np
import sys
import random
import time
import  serial
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextBrowser, QGroupBox, QGridLayout, QTabWidget, QTextEdit, QScrollArea, QMdiSubWindow
from PyQt5.QtGui import QPixmap, QFont, QTextCursor, QWindow
import Xlib.display
from PyQt5.QtCore import Qt, QRect, QCoreApplication, QLocale, QObject, QThread, pyqtSignal, QRunnable, QThreadPool

import time
import numpy as np
from threading import Thread
import pyqtgraph as pg
import bottleneck as bn
import PyQt5
import random
import math
import requests

# import rospy
# # import cv2
# from threading import Thread, Event
# from flask import Flask, render_template, Response
# import signal, sys
# # from cv_bridge import CvBridge
# # from sensor_msgs.msg import Image
# from std_msgs.msg import Float32
DATA_MOTOR = [0, 0, 0, 0]
ARAH_MOTOR = ["", "","", ""]
TIME_NOW = 0
class MySensor():
    def get_position(self, mean=0.0, standard_dev=0.1):
        # Random sensor data
        return np.random.normal(mean, standard_dev, 1)[0]

    def get_feedbackRobot(self):
        global DATA_MOTOR, ARAH_MOTOR
        try:
            url = 'http://192.168.244.245:5000'
            resp = requests.get(url=url)
            data = resp.json()  # Check the JSON
            DATA_MOTOR = data
            print("JSON", data)
            for i, data in enumerate(DATA_MOTOR):
                if data < 0 :
                    ARAH_MOTOR[i] = "KIRI"
                elif data > 0 :
                    ARAH_MOTOR[i] = "KANAN"
                elif data == 0 :
                    ARAH_MOTOR[i] = "STOP"

        except :
            DATA_MOTOR = [0,0,0,0]
        return DATA_MOTOR
        



class SignalCommunicate(PyQt5.QtCore.QObject):
    # https://stackoverflow.com/a/45620056
    got_new_sensor_data = PyQt5.QtCore.pyqtSignal(list, float)
    position_updated = PyQt5.QtCore.pyqtSignal(float)


class LiveSensorViewer(QWidget):

    def __init__(self, sensor_update_interval=50, graph_update_interval=5):
        super(LiveSensorViewer, self).__init__()

        # How frequently to get sensor data and update graph
        self.sensor_update_interval = sensor_update_interval
        self.graph_update_interval = graph_update_interval
        self.graph_update_interval_tracker = 0

        # Init sensor object which gives live data
        self.my_sensor = MySensor()

        # Init with default values
        self.current_position = self.my_sensor.get_position(mean=0.0, standard_dev=0.1)
        self.current_position_timestamp = time.time()
        

        # Init array which stores sensor data
        self.log_time = [self.current_position_timestamp]
        self.log_position_raw  = [self.current_position]
        self.log_position_raw1 = [self.current_position]
        self.log_position_raw2 = [self.current_position]
        self.log_position_raw3 = [self.current_position]
        # Define the array size on max amount of data to store in the list
        self.log_size = 1 * 60 * 200 / self.sensor_update_interval

        # Setup the graphs which will display sensor data
        self.plot_widget = pg.GraphicsWindow(show=True, title="PLOT DATA RPM")
        self.my_graph = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph.showGrid(x=True, y=True)
        self.my_graph.addLegend()

        # Curves to be drawn on the graph
        self.plot_widget.nextRow()
        self.my_graph1 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph1.showGrid(x=True, y=True)
        self.my_graph1.addLegend()
        self.plot_widget.nextRow()
        self.my_graph2 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph2.showGrid(x=True, y=True)
        self.my_graph2.addLegend()
        self.plot_widget.nextRow()
        self.my_graph3 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph3.showGrid(x=True, y=True)
        self.my_graph3.addLegend()

        # Curves to be drawn on the graph
        self.curve_position_raw = self.my_graph.plot(self.log_time, self.log_position_raw, name='Motor 1(rpm)',
                                                     pen=pg.mkPen(color='#525252'))

        # Curves to be drawn on the graph
        self.curve_position_raw1 = self.my_graph1.plot(self.log_time, self.log_position_raw1, name='Motor 2(rpm)',
                                                     pen=pg.mkPen(color='#525252'))

        self.curve_position_raw2 = self.my_graph2.plot(self.log_time, self.log_position_raw2, name='Motor 3(rpm)',
                                                       pen=pg.mkPen(color='#525252'))

        self.curve_position_raw3 = self.my_graph3.plot(self.log_time, self.log_position_raw3, name='Motor 4(rpm)',
                                                       pen=pg.mkPen(color='#525252'))


        # # A dialog box which displays the sensor value only. No graph.
        # self.my_dialog = PyQt5.QtWidgets.QWidget()
        # self.verticalLayout = PyQt5.QtWidgets.QVBoxLayout(self.my_dialog)
        #
        # self.my_label = PyQt5.QtWidgets.QLabel()
        # self.verticalLayout.addWidget(self.my_label)
        # self.my_label.setText('Current sensor position:')
        #
        # self.my_sensor_value = PyQt5.QtWidgets.QDoubleSpinBox()
        # self.verticalLayout.addWidget(self.my_sensor_value)
        # self.my_sensor_value.setDecimals(6)
        #
        # self.my_dialog.show()

        # Signals that can be emitted
        self.signalComm = SignalCommunicate()
        # Connect the signal 'position_updated' to the QDoubleSpinBox
        # self.signalComm.position_updated.connect(self.my_sensor_value.setValue)

        # Setup thread which will continuously query the sensor for data
        self.position_update_thread = Thread(target=self.read_position,
                                             args=(self.my_sensor, self.sensor_update_interval))
        self.position_update_thread.daemon = True
        self.position_update_thread.start()  # Start the thread to query sensor data



    def read_position(self, sensor_obj, update_interval):
        # This function continuously runs in a seprate thread to continuously query the sensor for data

        c = SignalCommunicate()  # https://stackoverflow.com/a/45620056
        c.got_new_sensor_data.connect(self.handle_sensor_data)

        while True:
            # Get data and timestamp from sensor
            new_pos = sensor_obj.get_feedbackRobot()
            new_pos_time = time.time()

            # Emit signal with sensor data and  timestamp
            c.got_new_sensor_data.emit(new_pos, new_pos_time)

            # Wait before quering the sensor again
            time.sleep(update_interval / 1000)

    def handle_sensor_data(self, new_pos, new_pos_time):
        global TIME_NOW
        # Get the sensor position/timestamp emitted from the separate thread
        self.current_position_timestamp = new_pos_time
        data = new_pos
        # self.current_position = data[0]
        self.cur_data =  data[0]
        self.cur_data1 = data[1]
        self.cur_data2 = data[2]
        self.cur_data3 = data[3]
        # Emit a singal with new position info
        self.signalComm.position_updated.emit(self.current_position)

        # Add data to log array
        TIME_NOW = self.current_position_timestamp
        self.log_time.append(self.current_position_timestamp)
        if len(self.log_time) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_time.pop(0)

        self.log_position_raw.append(self.cur_data)
        if len(self.log_position_raw) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw.pop(0)

        self.log_position_raw1.append(self.cur_data1)
        if len(self.log_position_raw1) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw1.pop(0)

        self.log_position_raw2.append(self.cur_data2)
        if len(self.log_position_raw2) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw2.pop(0)

        self.log_position_raw3.append(self.cur_data3)
        if len(self.log_position_raw3) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw3.pop(0)

        if len(self.log_time) <= 10:
            # Skip calculating moving avg if only 10 data points collected from sensor to prevent errors
            return

        # Determine if graph needs to be updated
        self.update_graph_interval_check()

    def getdata(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10. * math.sin(time.time() * frequency * 2 * math.pi) + noise
        return new

    def getdata1(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10. * math.sin(time.time() * frequency * 2 * math.pi) + noise
        return new

    def getdata2(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10. * math.sin(time.time() * frequency * 2 * math.pi) + noise
        return new

    def getdata3(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10. * math.sin(time.time() * frequency * 2 * math.pi) + noise
        return new

    def calculate_moving_avg(self):
        # Get moving average of the position
        self.log_position_moving_avg = bn.move_mean(self.log_position_raw, window=5, min_count=1)
        self.log_position_moving_avg1 = bn.move_mean(self.log_position_raw1, window=5, min_count=1)

    def update_graph_interval_check(self):
        # Update less frequently to reduce load on the application

        self.graph_update_interval_tracker += 1
        if self.graph_update_interval_tracker % self.graph_update_interval == 0:
            self.graph_update_interval_tracker = 0  # Reset back to 0
            self.update_graph()  # Get graph to update

    def update_graph(self):
        self.curve_position_raw.setData(self.log_time, self.log_position_raw)
        self.curve_position_raw1.setData(self.log_time, self.log_position_raw1)
        self.curve_position_raw2.setData(self.log_time, self.log_position_raw2)
        self.curve_position_raw3.setData(self.log_time, self.log_position_raw3)
        # self.curve_position_moving_avg.setData(self.log_time, self.log_position_moving_avg)


# Thread Calc
class RPM_Motor(QThread):
    # finished = pyqtSignal(int)
    global DATA_MOTOR, ARAH_MOTOR
    dataMotor = pyqtSignal(list)
    
    def __init__(self, Motor = 1) :
        super(RPM_Motor, self).__init__()
        self.motor = Motor
        self.time_last = 0
    
    def Ticks():
        return time.time * 1000

    def run(self):

        while True:
            
            x = 0
            y = 0
                
            arah = "stop"

            if self.motor == 1 :
                x = DATA_MOTOR[0]
                arah = ARAH_MOTOR[0]

            elif self.motor == 2 :
                x = DATA_MOTOR[1]
                arah = ARAH_MOTOR[1]
                    
            elif self.motor == 3:
                x = DATA_MOTOR[2]
                arah = ARAH_MOTOR[2]
                    
            elif self.motor == 4 :
                x = DATA_MOTOR[3]
                arah = ARAH_MOTOR[3]

                # if int(y) == 0 :
                #     arah = "stop"
                # elif int(y) == 1 :
                #     arah = "kanan"
                # elif int(y) == 2 :
                #     arah = "stop"

                

            print("MOTOR",self.motor)
            print("Spped MOTOR", DATA_MOTOR)

                
            self.dataMotor.emit([self.motor, x, arah])

            time.sleep(0.5)
                # print("Kecepatan Motor " + str(self.motor) +" : " + str(x) + "RPM")

                # time.sleep(random.randint(700, 2500) / 100000)

           



class WindowKosong(QWidget):
    def __init__(self):
        super().__init__()
        self.lebarWindow = 1000
        self.tinggiWindow = 600

        # INIT GUI
        self.initUI()

        # INIT THREAD
        self.getRPMMotor_1 = RPM_Motor(Motor= 1)
        self.getRPMMotor_2 = RPM_Motor(Motor= 2)
        self.getRPMMotor_3 = RPM_Motor(Motor= 3)
        self.getRPMMotor_4 = RPM_Motor(Motor= 4)

        self.getRPMMotor_1.start() # Mulai Proses
        self.getRPMMotor_2.start() # Mulai Proses
        self.getRPMMotor_3.start() # Mulai Proses
        self.getRPMMotor_4.start() # Mulai Proses

        self.getRPMMotor_1_StateFinnished = 0 # State Finnish
        self.getRPMMotor_2_StateFinnished = 0 # State Finnish
        self.getRPMMotor_3_StateFinnished = 0 # State Finnish
        self.getRPMMotor_4_StateFinnished = 0 # State Finnish

        # THREAD SIGNAL
        ## Signal - Motor 1
        self.getRPMMotor_1.finished.connect(self.getRPMMotor1_Finished)
        self.getRPMMotor_1.dataMotor.connect(self.updateRPMMotor)

        ## Signal - Motor 2
        self.getRPMMotor_2.finished.connect(self.getRPMMotor2_Finished)
        self.getRPMMotor_2.dataMotor.connect(self.updateRPMMotor)

        ## Signal - Motor 3
        self.getRPMMotor_3.finished.connect(self.getRPMMotor3_Finished)
        self.getRPMMotor_3.dataMotor.connect(self.updateRPMMotor)

        ## Signal - Motor 4
        self.getRPMMotor_4.finished.connect(self.getRPMMotor4_Finished)
        self.getRPMMotor_4.dataMotor.connect(self.updateRPMMotor)



    def updateRPMMotor(self, dataMotor):
        global DATA_MOTOR, ARAH_MOTOR, TIME_NOW

        if isinstance(dataMotor, list): # cek tipe data list
            motor = dataMotor[0]
            vMotor = dataMotor[1]
            arahMotor = dataMotor[2].lower()

            my_time = time.strftime('%H:%M:%S', time.localtime(TIME_NOW))
            # print(motor)
            # print(vMotor)
            if int(motor) == 1:
                self.kecepatanMotor1.setText("Kecepatan Motor " + str(motor) + " : " + str(vMotor) + " RPM")
                self.arahMotor1.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))
            elif int(motor) == 2:
                self.kecepatanMotor2.setText("Kecepatan Motor " + str(motor) + " : " + str(vMotor) + " RPM")
                self.arahMotor2.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))
            elif int(motor) == 3:
                self.kecepatanMotor3.setText("Kecepatan Motor " + str(motor) + " : " + str( vMotor) + " RPM")
                self.arahMotor3.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))
            elif int(motor) == 4:
                self.kecepatanMotor4.setText("Kecepatan Motor " + str(motor) + " : " + str( vMotor) + " RPM")
                self.arahMotor4.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))

            self.logStr += "\n"
            self.logStr += "["+ str(my_time) + "] Kecepatan Motor " + str(motor) + " : " + str( vMotor) + " RPM - ARAH PUTAR MOTOR : " + str(arahMotor.upper())


            self.display_files_edit.setText(self.logStr)
            self.display_files_edit.moveCursor(QTextCursor.End)



    # === Process Untuk Thread === #
    def getRPMMotor1_Finished(self):
        self.logStr += "\n"
        self.logStr += "RPM 1 FINISHED"
        self.display_files_edit.setText(self.logStr)

        self.kecepatanMotor1.setText("Kecepatan Motor : STOP")
        self.arahMotor1.setText("Arah Motor 1 : STOP")

    def getRPMMotor2_Finished(self):
        self.logStr += "\n"
        self.logStr += "RPM 2 FINISHED"
        self.display_files_edit.setText(self.logStr)

        self.kecepatanMotor2.setText("Kecepatan Motor : STOP")
        self.arahMotor2.setText("Arah Motor 2 : STOP")

    def getRPMMotor3_Finished(self):
        self.logStr += "\n"
        self.logStr += "RPM 3 FINISHED"
        self.display_files_edit.setText(self.logStr)

        self.kecepatanMotor3.setText("Kecepatan Motor : STOP")
        self.arahMotor3.setText("Arah Motor 3 : STOP")

    def getRPMMotor4_Finished(self):
        self.logStr += "\n"
        self.logStr += "RPM 4 FINISHED"
        self.display_files_edit.setText(self.logStr)

        self.kecepatanMotor4.setText("Kecepatan Motor : STOP")
        self.arahMotor4.setText("Arah Motor 4 : STOP")

    # === FUNCTION UI ==== #
    def initUI(self):
        self.setGeometry(100, 100, self.lebarWindow, self.tinggiWindow)
        self.setWindowTitle("LaporanAkhir2021")
        self.tampilCredits()
        self.tampilTab()
        self.tampilGroupBox()
        self.show()
        
    def tampilLabel(self):
        text = QLabel(self)
        text.setText("Hallo")
        text.move(105, 15)

        img = "../logoPolinema.png"

        try:
            with open(img):
                pnm_img = QLabel(self)
                pixmap = QPixmap(img)
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)

                pnm_img.setPixmap(pixmap)
                pnm_img.move(100, 100)

        except FileNotFoundError:
            print("Gambar Tidak Ditemukan")
    def tampilGambar(self):
        img = "../logoPolinema.png"

        try:
            with open(img):
                pnm_img = QLabel(self)
                pixmap = QPixmap(img)
                pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)

                pnm_img.setPixmap(pixmap)
                pnm_img.move(self.lebarWindow // 2, 10)

        except FileNotFoundError:
            print("Gambar Tidak Ditemukan")

    def tampilTab(self):
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(420, 20, 501, 540))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QWidget()
        self.tab.setObjectName("tab")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")

        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.addTab(self.tab_3, "")

        # Desc Tab
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Monitoring")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Log")
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Plot")

        self.display_files_edit = QTextEdit(self.tab_2)
        # self.groupBox_Motor1.setGeometry(QRect(10, 20, 471, 101))
        self.display_files_edit.setGeometry(QRect(0, 0, 500, 541))
        self.display_files_edit.setFont(QFont('Courier New', 8))
        self.display_files_edit.setReadOnly(True)

        self.logStr = ""
        self.logStr += "Hallo"
        self.display_files_edit.setText(self.logStr)

        # self.scrollbar = QScrollArea(self.tab_3, widgetResizable=True)


        self.dataPlot = LiveSensorViewer(sensor_update_interval=50, graph_update_interval=5)
        # self.dataPlot_winId = self.get_window_id("PLOT DATA RPM")
        # self.window = QWindow.fromWinId(self.dataPlot_winId)
        # self.widgetPlot = QWidget.createWindowContainer(window)

        self.subWind = QMdiSubWindow()
        self.subWind.setWidget(self.dataPlot)

        # self.scrollbar.setWidget(  self.subWind)






    def tampilGroupBox(self):
        self.tampilGroupBox1()
        self.tampilGroupBox2()
        self.tampilGroupBox3()
        self.tampilGroupBox4()

    def tampilGroupBox1(self):
        self.groupBox_Motor1 = QGroupBox(self.tab)
        self.groupBox_Motor1.setGeometry(QRect(10, 20, 471, 101))
        self.groupBox_Motor1.setObjectName("groupBox_Motor1")

        self.gridLayoutWidget = QWidget(self.groupBox_Motor1)
        self.gridLayoutWidget.setGeometry(QRect(20, 30, 441, 61))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout_Motor1 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_Motor1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor1.setObjectName("gridLayout_Motor1")

        self.kecepatanMotor1 = QLabel(self.gridLayoutWidget)
        self.kecepatanMotor1.setFont(QFont('Arial', 14))
        self.kecepatanMotor1.setObjectName("kecepatanMotor1")
        self.gridLayout_Motor1.addWidget(self.kecepatanMotor1, 0, 0, 1, 1)

        self.arahMotor1 = QLabel(self.gridLayoutWidget)
        self.arahMotor1.setFont(QFont('Arial', 14))

        self.arahMotor1.setAutoFillBackground(False)
        self.arahMotor1.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.arahMotor1.setObjectName("arahMotor1")
        self.gridLayout_Motor1.addWidget(self.arahMotor1, 1, 0, 1, 1)

        self.groupBox_Motor1.setTitle("Motor 1")
        self.kecepatanMotor1.setText("Kecepatan Motor 1 : 900 RPM")
        self.arahMotor1.setText("Arah Motor 1 : KANAN")

    def tampilGroupBox2(self):
        self.groupBox_Motor2 = QGroupBox(self.tab)
        self.groupBox_Motor2.setGeometry(QRect(10, 140, 471, 101))
        self.groupBox_Motor2.setToolTip("")
        self.groupBox_Motor2.setObjectName("groupBox_Motor2")

        self.gridLayoutWidget_2 = QWidget(self.groupBox_Motor2)
        self.gridLayoutWidget_2.setGeometry(QRect(20, 20, 441, 61))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")

        self.gridLayout_Motor2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_Motor2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor2.setObjectName("gridLayout_Motor2")

        self.arahMotor2 = QLabel(self.gridLayoutWidget_2)

        self.arahMotor2.setObjectName("arahMotor2")
        self.arahMotor2.setFont(QFont('Arial', 14))
        self.gridLayout_Motor2.addWidget(self.arahMotor2, 1, 0, 1, 1)

        self.kecepatanMotor2 = QLabel(self.gridLayoutWidget_2)
        self.kecepatanMotor2.setFont(QFont('Arial', 14))
        self.kecepatanMotor2.setObjectName("kecepatanMotor2")
        self.gridLayout_Motor2.addWidget(self.kecepatanMotor2, 0, 0, 1, 1)

        self.groupBox_Motor2.setTitle("Motor 2")
        self.arahMotor2.setText("Arah Motor 2 : KIRI")
        self.kecepatanMotor2.setText("Kecepatan Motor 2 : 900 RPM")

    def get_window_id(self, name):
        import Xlib.display

        d = Xlib.display.Display()
        r = d.screen().root

        window_ids = r.get_full_property(
            d.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType
        ).value

        for window_id in window_ids:
            window = d.create_resource_object('window', window_id)
            if window.get_wm_name() == name:
                return window_id

    def tampilGroupBox3(self):

        self.groupBox_Motor3 = QGroupBox(self.tab)
        self.groupBox_Motor3.setGeometry(QRect(10, 260, 471, 101))
        self.groupBox_Motor3.setObjectName("groupBox_Motor3")

        self.gridLayoutWidget_3 = QWidget(self.groupBox_Motor3)
        self.gridLayoutWidget_3.setGeometry(QRect(20, 30, 441, 61))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")

        self.gridLayout_Motor3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_Motor3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor3.setObjectName("gridLayout_Motor3")

        self.arahMotor3 = QLabel(self.gridLayoutWidget_3)
        self.arahMotor3.setFont(QFont('Arial', 14))
        self.arahMotor3.setObjectName("arahMotor3")
        self.gridLayout_Motor3.addWidget(self.arahMotor3, 1, 0, 1, 1)

        self.kecepatanMotor3 = QLabel(self.gridLayoutWidget_3)
        self.kecepatanMotor3.setFont(QFont('Arial', 14))
        self.kecepatanMotor3.setLocale(QLocale(QLocale.Indonesian, QLocale.Indonesia))
        self.kecepatanMotor3.setInputMethodHints(Qt.ImhNone)
        self.kecepatanMotor3.setObjectName("kecepatanMotor3")
        self.gridLayout_Motor3.addWidget(self.kecepatanMotor3, 0, 0, 1, 1)

        self.groupBox_Motor3.setTitle("Motor 3")
        self.arahMotor3.setText("Arah Motor 3 : KIRI")
        self.kecepatanMotor3.setText("Kecepatan Motor 3 : 900 RPM")

    def tampilGroupBox4(self):
        self.groupBox_Motor4 = QGroupBox(self.tab)
        self.groupBox_Motor4.setGeometry(QRect(10, 390, 471, 101))
        self.groupBox_Motor4.setObjectName("groupBox_Motor4")

        self.gridLayoutWidget_5 = QWidget(self.groupBox_Motor4)
        self.gridLayoutWidget_5.setGeometry(QRect(20, 30, 441, 61))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")

        self.gridLayout_Motor4 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_Motor4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor4.setObjectName("gridLayout_Motor4")

        self.arahMotor4 = QLabel(self.gridLayoutWidget_5) 
        self.arahMotor4.setFont(QFont('Arial', 14))
        self.arahMotor4.setObjectName("arahMotor4")
        self.gridLayout_Motor4.addWidget(self.arahMotor4, 2, 0 , 1, 1)

        self.kecepatanMotor4 = QLabel(self.gridLayoutWidget_5)
        self.kecepatanMotor4.setFont(QFont('Arial', 14))
        self.kecepatanMotor4.setObjectName("kecepatanMotor4")
        self.gridLayout_Motor4.addWidget(self.kecepatanMotor4, 1, 0, 1, 1)

        self.groupBox_Motor4.setTitle("Motor 4")
        self.arahMotor4.setText("Arah Motor 4 : STOP")
        self.kecepatanMotor4.setText("Kecepatan Motor 4 : 900 RPM")

    def tampilCredits(self):
        _translate = QCoreApplication.translate

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(10, 30, 391, 531))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setHtml(_translate("LaporanAkhir2021",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/logo/logoPolinema.png\" width=\"100\" /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">SISTEM <i> MONITORING </i> KECEPATAN PUTARAN MOTOR PADA ROBOT RODA 4 <i> OMNI ASIMETRIS DIRECTIONAL </i> </span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Dwi Setia Fardhana</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">1931110044</span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Wiji Ningsih</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">1931110002</span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\"-bqt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">D3 Teknik Elektronika</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Teknik Elektro</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Politeknik Negeri Malang</span></p></body></html>"))



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = WindowKosong()
    window.show()
    sys.exit(app.exec_())
