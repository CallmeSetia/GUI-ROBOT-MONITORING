#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

data = [0]
raw=  serial.Serial('COM6', baudrate=9600, timeout=1,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
raw.set_buffer_size(rx_size = 2, tx_size =2)
timeout = 0
def update():
    global curve, data, timeout
    timeout += 1
    if raw.is_open == True:
        if raw.in_waiting:
            eol = b'\n'
            leneol = len(eol)
            line = bytearray()
            line = raw.readline()
            line = line.rstrip()
            line_data = line.decode("utf-8")
            data.append(int(line_data))
            print(line_data)
            xdata = np.array(data, dtype='float64')
            curve.setData(xdata)
            app.processEvents()
            timeout = 0

    if timeout >= 10:
        raw.close()
    # data.append(int(line))
    # xdata = np.array(data, dtype='float64')
    # curve.setData(xdata)
    # app.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()