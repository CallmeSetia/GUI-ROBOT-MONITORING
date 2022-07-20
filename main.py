import time
import numpy as np
from threading import Thread
import pyqtgraph as pg
import bottleneck as bn
import PyQt5
import random
import math
class MySensor():
    def get_position(self, mean=0.0, standard_dev=0.1):
        # Random sensor data
        return np.random.normal(mean, standard_dev, 1)[0]


class SignalCommunicate(PyQt5.QtCore.QObject):
    # https://stackoverflow.com/a/45620056
    got_new_sensor_data = PyQt5.QtCore.pyqtSignal(float, float)
    position_updated = PyQt5.QtCore.pyqtSignal(float)


class LiveSensorViewer():

    def __init__(self, sensor_update_interval=50, graph_update_interval=5):
        # super().__init__()

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
        self.log_position_raw = [self.current_position]
        self.log_position_raw1 = [self.current_position]
        # Define the array size on max amount of data to store in the list
        self.log_size = 1 * 60 * 200 / self.sensor_update_interval

        # Setup the graphs which will display sensor data
        self.plot_widget = pg.GraphicsWindow(show=True)
        self.my_graph = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph.showGrid(x=True, y=True, alpha=0.25)
        self.my_graph.addLegend()

        # Curves to be drawn on the graph
        self.curve_position_raw = self.my_graph.plot(self.log_time, self.log_position_raw, name='Position raw (mm)',
                                                     pen=pg.mkPen(color='#525252'))
        self.curve_position_moving_avg = self.my_graph.plot(self.log_time, self.log_position_raw,
                                                            name='Position avg. 5 periods (mm)',
                                                            pen=pg.mkPen(color='#FFF'))
        self.plot_widget.nextRow()
        self.my_graph1 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph1.showGrid(x=True, y=True, alpha=0.25)
        self.my_graph1.addLegend()

        # Curves to be drawn on the graph
        self.curve_position_raw = self.my_graph.plot(self.log_time, self.log_position_raw, name='Position raw (mm)',
                                                     pen=pg.mkPen(color='#525252'))
        self.curve_position_moving_avg = self.my_graph.plot(self.log_time, self.log_position_raw,
                                                            name='Position avg. 5 periods (mm)',
                                                            pen=pg.mkPen(color='#FFF'))
        # Curves to be drawn on the graph
        self.curve_position_raw1 = self.my_graph1.plot(self.log_time, self.log_position_raw1, name='Position raw1 (mm)',
                                                     pen=pg.mkPen(color='#525252'))
        self.curve_position_moving_avg1 = self.my_graph1.plot(self.log_time, self.log_position_raw1,
                                                            name='Position avg. 5 periods (mm)',
                                                            pen=pg.mkPen(color='#FFF'))
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
            new_pos = sensor_obj.get_position(mean=0.0, standard_dev=0.1)
            new_pos_time = time.time()

            # Emit signal with sensor data and  timestamp
            c.got_new_sensor_data.emit(new_pos, new_pos_time)

            # Wait before quering the sensor again
            time.sleep(update_interval / 1000)

    def handle_sensor_data(self, new_pos, new_pos_time):

        # Get the sensor position/timestamp emitted from the separate thread
        self.current_position_timestamp = new_pos_time
        self.current_position = new_pos
        self.cur_data = self.getdata()

        # Emit a singal with new position info
        self.signalComm.position_updated.emit(self.current_position)

        # Add data to log array
        self.log_time.append(self.current_position_timestamp)
        if len(self.log_time) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_time.pop(0)

        self.log_position_raw.append(self.current_position)
        if len(self.log_position_raw) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw.pop(0)

        self.log_position_raw1.append(self.cur_data)
        if len(self.log_position_raw1) > self.log_size:
            # Append new data to the log and remove old data to maintain desired log size
            self.log_position_raw1.pop(0)

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
        # self.curve_position_moving_avg.setData(self.log_time, self.log_position_moving_avg)


if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets, uic, QtCore, QtGui

    app = QtWidgets.QApplication(sys.argv)

    z = LiveSensorViewer()

    app.exec_()
    sys.exit(app.exec_())