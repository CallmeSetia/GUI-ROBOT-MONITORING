# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\coba.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import logo_rc


class Ui_LaporanAkhir2021(object):
    def setupUi(self, LaporanAkhir2021):
        LaporanAkhir2021.setObjectName("LaporanAkhir2021")
        LaporanAkhir2021.resize(943, 590)
        LaporanAkhir2021.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(LaporanAkhir2021)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 30, 391, 531))
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(420, 20, 501, 541))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.groupBox_Motor2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_Motor2.setGeometry(QtCore.QRect(10, 140, 471, 101))
        self.groupBox_Motor2.setToolTip("")
        self.groupBox_Motor2.setObjectName("groupBox_Motor2")

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_Motor2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 441, 61))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_Motor2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_Motor2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor2.setObjectName("gridLayout_Motor2")
        self.arahMotor2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.arahMotor2.setObjectName("arahMotor2")

        self.gridLayout_Motor2.addWidget(self.arahMotor2, 1, 0, 1, 1)

        self.kecepatanMotor2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.kecepatanMotor2.setObjectName("kecepatanMotor2")
        self.gridLayout_Motor2.addWidget(self.kecepatanMotor2, 0, 0, 1, 1)
        self.groupBox_Motor1 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_Motor1.setGeometry(QtCore.QRect(10, 20, 471, 101))
        self.groupBox_Motor1.setObjectName("groupBox_Motor1")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_Motor1)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 441, 61))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_Motor1 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_Motor1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor1.setObjectName("gridLayout_Motor1")
        self.kecepatanMotor1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.kecepatanMotor1.setObjectName("kecepatanMotor1")
        self.gridLayout_Motor1.addWidget(self.kecepatanMotor1, 0, 0, 1, 1)
        self.arahMotor1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.arahMotor1.setAutoFillBackground(False)
        self.arahMotor1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.arahMotor1.setObjectName("arahMotor1")
        self.gridLayout_Motor1.addWidget(self.arahMotor1, 1, 0, 1, 1)
        self.groupBox_Motor3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_Motor3.setGeometry(QtCore.QRect(10, 260, 471, 101))
        self.groupBox_Motor3.setObjectName("groupBox_Motor3")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_Motor3)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 30, 441, 61))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_Motor3 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_Motor3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor3.setObjectName("gridLayout_Motor3")
        self.arahMotor3 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.arahMotor3.setObjectName("arahMotor3")
        self.gridLayout_Motor3.addWidget(self.arahMotor3, 1, 0, 1, 1)
        self.kecepatanMotor3 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.kecepatanMotor3.setLocale(QtCore.QLocale(QtCore.QLocale.Indonesian, QtCore.QLocale.Indonesia))
        self.kecepatanMotor3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.kecepatanMotor3.setObjectName("kecepatanMotor3")
        self.gridLayout_Motor3.addWidget(self.kecepatanMotor3, 0, 0, 1, 1)
        self.groupBox_Motor4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_Motor4.setGeometry(QtCore.QRect(10, 390, 471, 101))
        self.groupBox_Motor4.setObjectName("groupBox_Motor4")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_Motor4)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(20, 30, 441, 61))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_Motor4 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_Motor4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_Motor4.setObjectName("gridLayout_Motor4")
        self.arahMotor4 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.arahMotor4.setObjectName("arahMotor4")
        self.gridLayout_Motor4.addWidget(self.arahMotor4, 2, 0, 1, 1)
        self.kecepatanMotor4 = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.kecepatanMotor4.setObjectName("kecepatanMotor4")
        self.gridLayout_Motor4.addWidget(self.kecepatanMotor4, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        LaporanAkhir2021.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LaporanAkhir2021)
        self.statusbar.setObjectName("statusbar")
        LaporanAkhir2021.setStatusBar(self.statusbar)

        self.retranslateUi(LaporanAkhir2021)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(LaporanAkhir2021)

    def retranslateUi(self, LaporanAkhir2021):
        _translate = QtCore.QCoreApplication.translate
        LaporanAkhir2021.setWindowTitle(_translate("LaporanAkhir2021", "MainWindow"))
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
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Sistem Monitoring Putaran Roda Robot Asimetric</span></p>\n"
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
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">D3 Teknik Elektronika</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Teknik Elektro</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Politeknik Negeri Malang</span></p></body></html>"))
        self.groupBox_Motor2.setTitle(_translate("LaporanAkhir2021", "Motor 2"))
        self.arahMotor2.setText(_translate("LaporanAkhir2021", "Arah Motor 2 : KIRI"))
        self.kecepatanMotor2.setText(_translate("LaporanAkhir2021", "Kecepatan Motor 2 : 900 RPM"))
        self.groupBox_Motor1.setTitle(_translate("LaporanAkhir2021", "Motor 1"))
        self.kecepatanMotor1.setText(_translate("LaporanAkhir2021", "Kecepatan Motor 1 : 900 RPM"))
        self.arahMotor1.setText(_translate("LaporanAkhir2021", "Arah Motor 1 : KANAN"))
        self.groupBox_Motor3.setTitle(_translate("LaporanAkhir2021", "Motor 3"))
        self.arahMotor3.setText(_translate("LaporanAkhir2021", "Arah Motor 3 : KIRI"))
        self.kecepatanMotor3.setText(_translate("LaporanAkhir2021", "Kecepatan Motor 3 : 900 RPM"))
        self.groupBox_Motor4.setTitle(_translate("LaporanAkhir2021", "Motor 4"))
        self.arahMotor4.setText(_translate("LaporanAkhir2021", "Arah Motor 4 : STOP"))
        self.kecepatanMotor4.setText(_translate("LaporanAkhir2021", "Kecepatan Motor 4 : 900 RPM"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("LaporanAkhir2021", "Monitoring"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("LaporanAkhir2021", "Log"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LaporanAkhir2021 = QtWidgets.QMainWindow()
    ui = Ui_LaporanAkhir2021()
    ui.setupUi(LaporanAkhir2021)
    LaporanAkhir2021.show()
    sys.exit(app.exec_())