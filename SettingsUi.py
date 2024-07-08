

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QMainWindow, QPushButton, QSlider, QWidget, QApplication, QFrame
from PyQt5 import QtCore, QtWidgets, QtGui


import Stackresource_rc
import UiRes_rc
import camResource_rc


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(405, 488)
        font = MainWindow.font()
        font.setPointSize(10)
        MainWindow.setFont(font)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.nav = QtWidgets.QWidget(self.centralwidget)
        self.nav.setObjectName("nav")
        self.nav.setStyleSheet("#nav {\n"
                               "        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                               "        width:50px;\n"
                               "        /*border-radius: 10px; *//* Adjust the value to change the curve radius */\n"
                               "    }\n"
                               "\n"
                               "    /* style for QPushButton and QLabel */\n"
                               "    #nav QPushButton {\n"
                               "        border-radius: 1px; /* Adjust the value to change the curve radius */\n"
                               "   /* color: white; *//* Text color */\n"
                               "    font-weight: bold;\n"
                               " /*border: 2px solid #4CAF50; *//* Border color */\n"
                               "    /*padding: 10px 20px;*/\n"
                               "        /*height:50px;*/\n"
                               "/*margin: 10px;*/\n"
                               "        \n"
                               "        /* border-bottom: 1px solid #b0b0b0; */\n"
                               "    }\n"
                               "#nav Qlabel{\n"
                               "border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                               "    color: white; /* Text color */\n"
                               "    font-weight: bold;\n"
                               " border: 2px solid #4CAF50; /* Border color */\n"
                               "    padding: 10px 20px;\n"
                               "        /*height:50px;*/\n"
                               "margin: 10px;\n"
                               "}\n"
                               "\n"
                               "    #nav QPushButton:hover {\n"
                               "        background-color:#073c6d\n"
                               "    }\n"
                               "")
        self.nav.setGeometry(0, 0, 481, 41)

        self.label = QLabel(self.centralwidget)
        self.label.setStyleSheet("#label{\n"
                                 "    color: white; /* Text color */\n"
                                 "    font-weight: bold;\n"
                                 "}\n"
                                 "\n"
                                 "")
        self.label.setObjectName("label")
        self.label.setGeometry(10, 10, 81, 21)
        font1 = self.label.font()
        font1.setPointSize(12)
        self.label.setFont(font1)

        self.close_btn = QPushButton(self.nav)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setGeometry(364, 5, 31, 33)  # 31, 23
        self.close_btn.setFlat(True)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/newPrefix/close.svg"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_btn.setIcon(icon14)
        self.close_btn.setIconSize(QtCore.QSize(20, 20))
        # self.close_btn.setStyleSheet("  QPushButton:hover {\n"
        #                        "        background-color:#073c6d\n"
        #                        "    }\n")

        self.minimize_btn = QPushButton(self.nav)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setFlat(True)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/newPrefix/minimize.svg"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize_btn.setIcon(icon14)
        self.minimize_btn.setGeometry(330, 5, 31, 33)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setStyleSheet("QLabel {\n"
                                   "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                   "    color: #3020ee; /* Change the font color to red */\n"
                                   "}")
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(20, 50, 81, 31)
        self.label_2.setFont(font1)

        self.brightness_slider = QSlider(self.centralwidget)
        self.brightness_slider.setObjectName("brightness_slider")
        self.brightness_slider.setOrientation(1)  # Horizontal
        self.brightness_slider.setMinimum(-60)
        self.brightness_slider.setMaximum(60)
        # self.brightness_slider.setValue(0)
        self.brightness_slider.setGeometry(20, 100, 360, 22)
        self.brightness_slider.setOrientation(Qt.Horizontal)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                   "    color: #3020ee; /* Change the font color to red */\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(20, 150, 91, 21)
        self.label_3.setFont(font1)

        self.contrast_slider = QSlider(self.centralwidget)
        self.contrast_slider.setObjectName("contrast_slider")
        self.contrast_slider.setOrientation(1)  # Horizontal
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(60)
        self.contrast_slider.setValue(0)
        self.contrast_slider.setGeometry(20, 195, 360, 22)
        self.contrast_slider.setOrientation(Qt.Horizontal)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setStyleSheet("QLabel {\n"
                                   "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                   "    color: #3020ee; /* Change the font color to red */\n"
                                   "}")
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(20, 240, 81, 31)
        self.label_4.setFont(font1)

        self.exposure_slider = QSlider(self.centralwidget)
        self.exposure_slider.setObjectName("exposure_slider")
        self.exposure_slider.setOrientation(1)  # Horizontal
        self.exposure_slider.setMinimum(-13)
        self.exposure_slider.setMaximum(-1)
        self.exposure_slider.setValue(-5)
        self.exposure_slider.setGeometry(20,295, 360, 22)
        self.exposure_slider.setOrientation(Qt.Horizontal)

        # self.exposure_checkBox = QCheckBox(self.centralwidget)
        # self.exposure_checkBox.setStyleSheet(
        #     "color: #3020ee; font-weight: bold; font-family: Arial;")  # Add this line
        # self.exposure_checkBox.setObjectName("exposure_checkBox")
        # self.exposure_checkBox.setGeometry(20, 335, 131, 17)
        # self.exposure_checkBox.setFont(font)

        self.default_btn = QPushButton(self.centralwidget)
        self.default_btn.setStyleSheet("QPushButton {\n"
                                    "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                                    "        border-radius: 20px; \n"
                                    "    color: white; /* Text color */\n"
                                    "    font-weight: bold;\n"
                                    "border:none; /* Border color */\n"
                                    "    padding: 10px 10px; /* Adjust padding as needed */\n"
                                    "    margin:0px; /* Margin to create distance between buttons */\n"
                                    "}\n"
                                    " QPushButton {\n"
                                    "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                    "    color: white; /* Text color */\n"
                                    "    font-weight: bold;\n"
                                    "\n"
                                    "    padding: 10px 20px;\n"
                                    "        /*height:50px;*/\n"
                                    "margin: 0px;\n"
                                    "        \n"
                                    "        /* border-bottom: 1px solid #b0b0b0; */\n"
                                    "    }\n"
                                    "QPushButton:hover {\n"
                                    "        background-color:#073c6d;\n"
                                    "    }")
        self.default_btn.setObjectName("more_btn")
        self.default_btn.setGeometry(300, 340, 89, 35)
        self.default_btn.setFont(font)

        # self.save_btn = QPushButton(self.centralwidget)
        # self.save_btn.setStyleSheet("QPushButton {\n"
        #                             "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
        #                             "        border-radius: 20px; \n"
        #                             "    color: white; /* Text color */\n"
        #                             "    font-weight: bold;\n"
        #                             "border:none; /* Border color */\n"
        #                             "    padding: 10px 10px; /* Adjust padding as needed */\n"
        #                             "    margin:0px; /* Margin to create distance between buttons */\n"
        #                             "}\n"
        #                             " QPushButton {\n"
        #                             "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
        #                             "    color: white; /* Text color */\n"
        #                             "    font-weight: bold;\n"
        #                             "\n"
        #                             "    padding: 10px 20px;\n"
        #                             "        /*height:50px;*/\n"
        #                             "margin: 0px;\n"
        #                             "        \n"
        #                             "        /* border-bottom: 1px solid #b0b0b0; */\n"
        #                             "    }\n"
        #                             "QPushButton:hover {\n"
        #                             "        background-color:#073c6d;\n"
        #                             "    }")
        # self.save_btn.setObjectName("save_btn")
        # self.save_btn.setGeometry(30, 400, 71, 31)
        self.autoSave_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.autoSave_btn.setGeometry(QtCore.QRect(30, 330, 120, 57))
        self.autoSave_btn.setCheckable(True)
        self.autoSave_btn.setAutoExclusive(False)
        self.autoSave_btn.setObjectName("autoSave_btn")
        self.autoSave_btn.setStyleSheet("""
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton {
                color: blue;
            }
        """)
        # Create a QFont object
        font = QtGui.QFont()
        font.setPointSize(10)  # Set the desired font size

        # Apply the font to the button
        self.autoSave_btn.setFont(font)
        
        self.hor_line =QFrame(self.centralwidget)
        self.hor_line.setObjectName("hor_line")
        self.hor_line.setGeometry(20, 380, 351, 20)
        self.hor_line.setFrameShadow(QFrame.Plain)
        self.hor_line.setFrameShape(QFrame.HLine)
        # self.hor_line.setStyleSheet("#hor_line {"
        #                             # "border: 2px solid #0e86f6;"  # Change '#0e86f6' to desired border color
        #                             "border: 1px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
        #                               # Adjust the value for desired curve
        #                             "}")
        self.hor_line.setStyleSheet(
            "QFrame#hor_line { color: blue }")
        
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(20, 400, 101, 31)
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet("QLabel {\n"
                                         "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                         "    color: #3020ee; /* Change the font color to red */\n"
                                         "}")

        self.browse_btn = QPushButton(self.centralwidget)
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.setGeometry(310, 432, 89, 35)
        self.browse_btn.setStyleSheet("QPushButton {\n"
                                       "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                                       "        border-radius: 20px; \n"
                                       "    color: white; /* Text color */\n"
                                       "    font-weight: bold;\n"
                                       "border:none; /* Border color */\n"
                                       "    padding: 10px 10px; /* Adjust padding as needed */\n"
                                       "    margin:0px; /* Margin to create distance between buttons */\n"
                                       "}\n"
                                       " QPushButton {\n"
                                       "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                       "    color: white; /* Text color */\n"
                                       "    font-weight: bold;\n"
                                       "\n"
                                       "    padding: 10px 20px;\n"
                                       "        /*height:50px;*/\n"
                                       "margin: 0px;\n"
                                       "        \n"
                                       "        /* border-bottom: 1px solid #b0b0b0; */\n"
                                       "    }\n"
                                       "QPushButton:hover {\n"
                                       "        background-color:#073c6d;\n"
                                       "    }")

        self.storage_label = QLabel(self.centralwidget)
        self.storage_label.setObjectName("storage_label")
        self.storage_label.setGeometry(20, 440, 281, 21)
        self.storage_label.setFrameShape(QFrame.Box)
        self.storage_label.setStyleSheet("QLabel {"
                                     #  "border: 2px solid #0e86f6;"  # Change 'red' to desired border color
                                     "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                     "/*border-radius: 10px;*/"   # Adjust the value for desired curve
                                     "}")
        # self.open_btn = QPushButton(self.centralwidget)
        # self.open_btn.setObjectName("open_btn")
        # self.open_btn.setGeometry(320, 432, 80, 35)
        # self.open_btn.setStyleSheet("QPushButton {\n"
        #                               "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
        #                               "        border-radius: 20px; \n"
        #                               "    color: white; /* Text color */\n"
        #                               "    font-weight: bold;\n"
        #                               "border:none; /* Border color */\n"
        #                               "    padding: 10px 10px; /* Adjust padding as needed */\n"
        #                               "    margin:0px; /* Margin to create distance between buttons */\n"
        #                               "}\n"
        #                               " QPushButton {\n"
        #                               "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
        #                               "    color: white; /* Text color */\n"
        #                               "    font-weight: bold;\n"
        #                               "\n"
        #                               "    padding: 10px 20px;\n"
        #                               "        /*height:50px;*/\n"
        #                               "margin: 0px;\n"
        #                               "        \n"
        #                               "        /* border-bottom: 1px solid #b0b0b0; */\n"
        #                               "    }\n"
        #                               "QPushButton:hover {\n"
        #                               "        background-color:#073c6d;\n"
        #                               "    }")


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Settings"))
        self.label_2.setText(_translate("MainWindow", "Brightness"))
        self.label_3.setText(_translate("MainWindow", "Contrast"))
        self.label_4.setText(_translate("MainWindow", "Exposure"))
        # self.exposure_checkBox.setText(
        #     _translate("MainWindow", "Auto Exposure"))
        self.default_btn.setText(_translate("MainWindow", "Default"))
        # self.save_btn.setText(_translate("MainWindow", "Save"))
        self.label_5.setText(_translate("MainWindow", "Storage Path:"))
        self.browse_btn.setText(_translate("MainWindow", "Browse"))
        self.storage_label.setText("")
        self.autoSave_btn.setText(_translate("MainWindow", "Auto Save"))
        # self.open_btn.setText(_translate("MainWindow", "Open"))
