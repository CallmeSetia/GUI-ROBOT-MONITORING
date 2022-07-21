import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextBrowser, QGroupBox, QGridLayout, QTabWidget, QTextEdit, \
    QScrollArea, QMdiSubWindow
from PyQt5.QtGui import QPixmap, QFont, QTextCursor

from PyQt5.QtCore import Qt, QRect, QCoreApplication, QLocale, QObject, QThread, pyqtSignal
from  PlotData import  PlotingData, SignalCommunicate
import  logo_rc
from PlotData import  *


class RPM_Motor(QThread):
    # finished = pyqtSignal(int)
    global DATA_MOTOR, ARAH_MOTOR
    dataMotor = pyqtSignal(list)

    def __init__(self, Motor=1):
        super(RPM_Motor, self).__init__()
        self.motor = Motor
        self.time_last = 0

    def Ticks(self):
        return time.time * 1000

    def run(self):

        while True:

            x = 0
            y = 0

            arah = "stop"

            if self.motor == 1:
                x = DATA_MOTOR[0]
                arah = ARAH_MOTOR[0]

            elif self.motor == 2:
                x = DATA_MOTOR[1]
                arah = ARAH_MOTOR[1]

            elif self.motor == 3:
                x = DATA_MOTOR[2]
                arah = ARAH_MOTOR[2]

            elif self.motor == 4:
                x = DATA_MOTOR[3]
                arah = ARAH_MOTOR[3]

                # if int(y) == 0 :
                #     arah = "stop"
                # elif int(y) == 1 :
                #     arah = "kanan"
                # elif int(y) == 2 :
                #     arah = "stop"

            print("MOTOR", self.motor)
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
        self.getRPMMotor_1 = RPM_Motor(Motor=1)
        self.getRPMMotor_2 = RPM_Motor(Motor=2)
        self.getRPMMotor_3 = RPM_Motor(Motor=3)
        self.getRPMMotor_4 = RPM_Motor(Motor=4)

        self.getRPMMotor_1.start()  # Mulai Proses
        self.getRPMMotor_2.start()  # Mulai Proses
        self.getRPMMotor_3.start()  # Mulai Proses
        self.getRPMMotor_4.start()  # Mulai Proses

        self.getRPMMotor_1_StateFinnished = 0  # State Finnish
        self.getRPMMotor_2_StateFinnished = 0  # State Finnish
        self.getRPMMotor_3_StateFinnished = 0  # State Finnish
        self.getRPMMotor_4_StateFinnished = 0  # State Finnish

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

        if isinstance(dataMotor, list):  # cek tipe data list
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
                self.kecepatanMotor3.setText("Kecepatan Motor " + str(motor) + " : " + str(vMotor) + " RPM")
                self.arahMotor3.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))
            elif int(motor) == 4:
                self.kecepatanMotor4.setText("Kecepatan Motor " + str(motor) + " : " + str(vMotor) + " RPM")
                self.arahMotor4.setText("Arah Motor " + str(motor) + " : " + str(arahMotor.upper()))

            self.logStr += "\n"
            self.logStr += "[" + str(my_time) + "] Kecepatan Motor " + str(motor) + " : " + str(
                vMotor) + " RPM - ARAH PUTAR MOTOR : " + str(arahMotor.upper())

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

        self.dataPlot = PlotingData(sensor_update_interval=50, graph_update_interval=5)
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
        self.gridLayout_Motor4.addWidget(self.arahMotor4, 2, 0, 1, 1)

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

