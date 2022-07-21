import PyQt5
import time
from threading import Thread
from PyQt5.QtWidgets import  QWidget
from Robot import  Robot

import pyqtgraph as pg

DATA_MOTOR = [0, 0, 0, 0]
ARAH_MOTOR = ["", "", "", ""]
TIME_NOW = 0

class SignalCommunicate(PyQt5.QtCore.QObject):
    got_new_sensor_data = PyQt5.QtCore.pyqtSignal(list, float)
    position_updated = PyQt5.QtCore.pyqtSignal(float)


class PlotingData(QWidget):

    def __init__(self, sensor_update_interval=50, graph_update_interval=5):
        super(PlotingData, self).__init__()

        self.sensor_update_interval = sensor_update_interval
        self.graph_update_interval = graph_update_interval
        self.graph_update_interval_tracker = 0

        self.robot = Robot()

        self.current_position = 0
        self.current_position_timestamp = time.time()

        # Init array which stores sensor data
        self.log_time = [self.current_position_timestamp]
        self.log_position_raw = [self.current_position]
        self.log_position_raw1 = [self.current_position]
        self.log_position_raw2 = [self.current_position]
        self.log_position_raw3 = [self.current_position]

        self.log_size = 1 * 60 * 200 / self.sensor_update_interval

        self.plot_widget = pg.GraphicsWindow(show=True, title="PLOT DATA RPM")

        # RPM 1 - PLOT
        self.my_graph = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph.showGrid(x=True, y=True)
        self.my_graph.addLegend()
        self.curve_position_raw = self.my_graph.plot(self.log_time, self.log_position_raw, name='Motor 1(rpm)',
                                                     pen=pg.mkPen(color='#525252'))
        self.plot_widget.nextRow()  # Ganti Baris

        # RPM 2 PLOT
        self.my_graph1 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph1.showGrid(x=True, y=True)
        self.my_graph1.addLegend()

        self.curve_position_raw1 = self.my_graph1.plot(self.log_time, self.log_position_raw1, name='Motor 2(rpm)',
                                                       pen=pg.mkPen(color='#525252'))

        self.plot_widget.nextRow() # Ganti Baris

        # RPM 3
        self.my_graph2 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph2.showGrid(x=True, y=True)
        self.my_graph2.addLegend()
        self.curve_position_raw2 = self.my_graph2.plot(self.log_time, self.log_position_raw2, name='Motor 3(rpm)',
                                                       pen=pg.mkPen(color='#525252'))
        self.plot_widget.nextRow() # Ganti Baris

        # RPM 4
        self.my_graph3 = self.plot_widget.addPlot(axisItems={'bottom': pg.DateAxisItem()})
        self.my_graph3.showGrid(x=True, y=True)
        self.my_graph3.addLegend()

        self.curve_position_raw3 = self.my_graph3.plot(self.log_time, self.log_position_raw3, name='Motor 4(rpm)',
                                                       pen=pg.mkPen(color='#525252'))

        self.signalComm = SignalCommunicate()
        self.position_update_thread = Thread(target=self.read_position,
                                             args=(self.robot, self.sensor_update_interval))
        self.position_update_thread.daemon = True
        self.position_update_thread.start()

    def read_position(self, sensor_obj, update_interval):
        c = SignalCommunicate()
        c.got_new_sensor_data.connect(self.handle_sensor_data)

        while True:
            new_pos = sensor_obj.get_feedbackRobot()
            new_pos_time = time.time()
            c.got_new_sensor_data.emit(new_pos, new_pos_time)
            time.sleep(update_interval / 1000)  # interval update plot

    def handle_sensor_data(self, new_pos, new_pos_time):
        global TIME_NOW

        self.current_position_timestamp = new_pos_time
        data = new_pos

        self.cur_data = data[0]
        self.cur_data1 = data[1]
        self.cur_data2 = data[2]
        self.cur_data3 = data[3]

        self.signalComm.position_updated.emit(self.current_position)

        TIME_NOW = self.current_position_timestamp
        self.log_time.append(self.current_position_timestamp)
        if len(self.log_time) > self.log_size:
            self.log_time.pop(0)

        self.log_position_raw.append(self.cur_data)
        if len(self.log_position_raw) > self.log_size:
            self.log_position_raw.pop(0)

        self.log_position_raw1.append(self.cur_data1)
        if len(self.log_position_raw1) > self.log_size:
            self.log_position_raw1.pop(0)

        self.log_position_raw2.append(self.cur_data2)
        if len(self.log_position_raw2) > self.log_size:
            self.log_position_raw2.pop(0)

        self.log_position_raw3.append(self.cur_data3)
        if len(self.log_position_raw3) > self.log_size:
            self.log_position_raw3.pop(0)

        if len(self.log_time) <= 10:
            return

        self.update_graph_interval_check()

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

