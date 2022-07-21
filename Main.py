import  sys
from gui_monitoring import *
from  PlotData import  *
from  Robot import  *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowKosong()
    window.show()
    sys.exit(app.exec_())