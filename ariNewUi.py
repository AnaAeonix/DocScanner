import Stackresource_rc
import UiRes_rc
import camResource_rc
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
import numpy as np


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setStyleSheet("# MainWindow{\n"
                                 "display: flex;\n"
                                 "flex-direction: column;\n"
                                 "align-item : center;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.pdf_btn = QtWidgets.QPushButton(self.centralwidget)
        self.pdf_btn.setGeometry(QtCore.QRect(610, 20, 211, 31))
        self.pdf_btn.setStyleSheet("QPushButton {\n"
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/pdf.svg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pdf_btn.setIcon(icon)
        self.pdf_btn.setIconSize(QtCore.QSize(20, 20))
        self.pdf_btn.setCheckable(True)
        self.pdf_btn.setAutoExclusive(True)
        self.pdf_btn.setFlat(False)
        self.pdf_btn.setObjectName("pdf_btn")

        self.show_page = QtWidgets.QLabel(self.centralwidget)
        # self.show_page.setGeometry(QtCore.QRect(700, 10, 231, 601))
        self.show_page.setFrameShape(QtWidgets.QFrame.Box)
        self.show_page.setText("")
        self.show_page.setStyleSheet("#show_page {"
                                     #  "border: 2px solid #0e86f6;"  # Change 'red' to desired border color
                                     "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                     "border-radius: 10px;"   # Adjust the value for desired curve
                                     "}")
       
        self.show_page.setMinimumSize(231, 880)  # Set minimum size
        self.show_page.setMaximumSize(231, 880)  # Set maximum size
        self.show_page.setObjectName("show_page")
        # Create QVBoxLayout for buttons
        self.buttons_layout = QtWidgets.QVBoxLayout()
        # Add QLabel to layout
        self.layout.addWidget(self.show_page, alignment=QtCore.Qt.AlignRight)
        # Set layout to central widget
        # self.centralwidget.setLayout(self.layout)
        # self.btn_label = QtWidgets.QLabel(self.centralwidget)
        # self.btn_label.setGeometry(QtCore.QRect(206, 479, 381, 41))
        # self.btn_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.btn_label.setText("")
        # self.btn_label.setObjectName("btn_label")
        # self.buttons_layout.addWidget(self.btn_label)
        # self.pdf_btn = QtWidgets.QPushButton(self.centralwidget)
        # self.pdf_btn.setGeometry(QtCore.QRect(610, 20, 211, 31))
        # self.pdf_btn.setStyleSheet("QPushButton {\n"
        #                            "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
        #                            "        border-radius: 20px; \n"
        #                            "    color: white; /* Text color */\n"
        #                            "    font-weight: bold;\n"
        #                            "border:none; /* Border color */\n"
        #                            "    padding: 10px 10px; /* Adjust padding as needed */\n"
        #                            "    margin:0px; /* Margin to create distance between buttons */\n"
        #                            "}\n"
        #                            " QPushButton {\n"
        #                            "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
        #                            "    color: white; /* Text color */\n"
        #                            "    font-weight: bold;\n"
        #                            "\n"
        #                            "    padding: 10px 20px;\n"
        #                            "        /*height:50px;*/\n"
        #                            "margin: 0px;\n"
        #                            "        \n"
        #                            "        /* border-bottom: 1px solid #b0b0b0; */\n"
        #                            "    }\n"
        #                            "QPushButton:hover {\n"
        #                            "        background-color:#073c6d;\n"
        #                            "    }")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/newPrefix/pdf.svg"),
        #                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pdf_btn.setIcon(icon)
        # self.pdf_btn.setIconSize(QtCore.QSize(20, 20))
        # self.pdf_btn.setCheckable(True)
        # self.pdf_btn.setAutoExclusive(True)
        # self.pdf_btn.setFlat(False)
        # self.pdf_btn.setObjectName("pdf_btn")
        self.buttons_layout.addWidget(
            self.pdf_btn, alignment=QtCore.Qt.AlignTop)
        self.camset_btn = QtWidgets.QPushButton(self.centralwidget)
        self.camset_btn.setGeometry(QtCore.QRect(710, 60, 101, 31))
        self.camset_btn.setStyleSheet("QPushButton {\n"
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
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/pdf.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.camset_btn.setIcon(icon1)
        self.camset_btn.setIconSize(QtCore.QSize(20, 20))
        self.camset_btn.setObjectName("jpeg_btn")
        self.buttons_layout.addWidget(
            self.camset_btn, alignment=QtCore.Qt.AlignTop)
        self.edit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_btn.setGeometry(QtCore.QRect(710, 60, 101, 31))
        self.edit_btn.setStyleSheet("QPushButton {\n"
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
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/edit1.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_btn.setIcon(icon1)
        self.edit_btn.setObjectName("edit_btn")
        self.buttons_layout.addWidget(
            self.edit_btn, alignment=QtCore.Qt.AlignTop)
        self.settings_btn = QtWidgets.QPushButton(self.centralwidget)
        self.settings_btn.setGeometry(QtCore.QRect(820, 60, 101, 31))
        self.settings_btn.setStyleSheet("QPushButton {\n"
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
                                        " QPushButton:hover {\n"
                                        "        background-color:#073c6d\n"
                                        "    }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/crop1.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_btn.setIcon(icon1)
        self.settings_btn.setObjectName("settings_btn")
        self.buttons_layout.addWidget(
            self.settings_btn, alignment=QtCore.Qt.AlignTop)
        self.delete_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_btn.setGeometry(QtCore.QRect(920, 60, 101, 31))
        self.delete_btn.setStyleSheet("QPushButton {\n"
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
                                      " QPushButton:hover {\n"
                                      "        background-color:#073c6d\n"
                                      "    }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/discard.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon2)
        self.delete_btn.setObjectName("delete_btn")
        self.buttons_layout.addWidget(
            self.delete_btn, alignment=QtCore.Qt.AlignTop)
        self.hor_line = QtWidgets.QFrame(self.centralwidget)
        self.hor_line.setGeometry(QtCore.QRect(730, 100, 171, 16))
        self.hor_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.hor_line.setStyleSheet("QFrame {"
                                    # "border: 2px solid #0e86f6;"  # Change '#0e86f6' to desired border color
                                    "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                    "border-radius: 10px;"   # Adjust the value for desired curve
                                    "}")
        self.hor_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.hor_line.setObjectName("hor_line")
        self.buttons_layout.addWidget(
            self.hor_line, alignment=QtCore.Qt.AlignTop)

        # Create additional QLabel below the hor_line
        self.additional_label = QtWidgets.QLabel(self.centralwidget)
        self.additional_label.setGeometry(QtCore.QRect(
            730, 120, 171, 950))  # Adjust geometry as needed
        # self.additional_label.setFrameShape(QtWidgets.QFrame.Box)
        # self.additional_label.setStyleSheet("QLabel {"
        #                                      "border: 2px solid #0e86f6;"  # Change '#0e86f6' to desired border color
        #                                      "border-radius: 10px;"   # Adjust the value for desired curve
        #                                      "}")
        self.additional_label.setObjectName("additional_label")
        self.additional_label.setStyleSheet("#additional_label {"
                                            #  "border: 2px solid #0e86f6;"  # Change 'red' to desired border color
                                            "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                            "border-radius: 10px;"   # Adjust the value for desired curve
                                            "}")
        self.additional_label.setFixedSize(210, 635)  # 680
        self.buttons_layout.addWidget(
            self.additional_label, alignment=QtCore.Qt.AlignTop)

        # Add some stretch to move the buttons to the bottom
        self.buttons_layout.addStretch()

        # Set layout for show_page
        self.show_page.setLayout(self.buttons_layout)

        # Set layout to central widget
        self.centralwidget.setLayout(self.layout)
        # Set layout to central widget
        self.centralwidget.setLayout(self.layout)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 40, 1650, 1051))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.cam_label = QtWidgets.QLabel(self.page)
        self.cam_label.setGeometry(QtCore.QRect(300, 80, 1191, 731))
        self.cam_label.setFrameShape(QtWidgets.QFrame.Box)
        self.cam_label.setText("")
        self.cam_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cam_label.setObjectName("cam_label")
        self.cam_label.setStyleSheet("QLabel {"
                                     #  "border: 2px solid #0e86f6;"  # Change 'red' to desired border color
                                     "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                     "border-radius: 10px;"   # Adjust the value for desired curve
                                     "}")
        self.cam_drop_down = QtWidgets.QComboBox(self.page)
        self.cam_drop_down.setGeometry(QtCore.QRect(750, 20, 281, 22))
        self.cam_drop_down.setObjectName("cam_drop_down")
        self.shutter_btn = QtWidgets.QPushButton(self.page)
        self.shutter_btn.setGeometry(QtCore.QRect(750, 880, 101, 61))
        self.shutter_btn.setText("")
        self.shutter_btn.setStyleSheet("QPushButton {\n"
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
                                       " QPushButton:hover {\n"
                                       "        background-color:#073c6d\n"
                                       "    }")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/newPrefix/shutter.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shutter_btn.setIcon(icon3)
        self.shutter_btn.setIconSize(QtCore.QSize(40, 40))
        self.shutter_btn.setCheckable(True)
        self.shutter_btn.setAutoExclusive(True)
        self.shutter_btn.setFlat(True)
        self.shutter_btn.setObjectName("shutter_btn") 
        # self.ai_btn = QtWidgets.QRadioButton(self.page)
        # self.ai_btn.setGeometry(QtCore.QRect(60, 30, 100, 57))
        # self.ai_btn.setCheckable(True)
        # self.ai_btn.setAutoExclusive(False)
        # self.ai_btn.setObjectName("ai_btn")

        # # Create a QFont object
        # font = QtGui.QFont()
        # font.setPointSize(10)  # Set the desired font size

        # # Apply the font to the button
        # self.ai_btn.setFont(font)
        self.autoSave_btn = QtWidgets.QRadioButton(self.page)
        self.autoSave_btn.setGeometry(QtCore.QRect(150, 30, 80, 57))
        self.autoSave_btn.setCheckable(True)
        self.autoSave_btn.setAutoExclusive(False)
        self.autoSave_btn.setObjectName("autoSave_btn")

        # Create a QFont object
        font = QtGui.QFont()
        font.setPointSize(10)  # Set the desired font size

        # Apply the font to the button
        self.autoSave_btn.setFont(font)
        self.trim_btn = QtWidgets.QRadioButton(self.page)
        self.trim_btn.setGeometry(QtCore.QRect(240, 30, 80, 57))
        self.trim_btn.setCheckable(True)
        self.trim_btn.setAutoExclusive(False)
        self.trim_btn.setObjectName("trim_btn")

        # Create a QFont object
        font = QtGui.QFont()
        font.setPointSize(10)  # Set the desired font size

        # Apply the font to the button
        self.trim_btn.setFont(font)
        self.foc_drop = QtWidgets.QComboBox(self.page)
        self.foc_drop.setGeometry(QtCore.QRect(530, 20, 101, 22))
        self.foc_drop.addItems(["Auto Focus", "Fixed Focus"])
        self.foc_drop.setObjectName("foc_drop")
        self.foc_label = QtWidgets.QLabel(self.page)
        self.foc_label.setGeometry(QtCore.QRect(460, 20, 61, 21))
        self.foc_label.setObjectName("foc_label")
        self.resolution_drop = QtWidgets.QComboBox(self.page)
        self.resolution_drop.setGeometry(QtCore.QRect(530, 900, 101, 22))
        self.resolution_drop.setObjectName("resolution_drop")
        self.resolution_label = QtWidgets.QLabel(self.page)
        self.resolution_label.setGeometry(QtCore.QRect(460, 900, 61, 21))
        self.resolution_label.setObjectName("resolution_label")
        self.crop_drop = QtWidgets.QComboBox(self.page)
        self.crop_drop.setGeometry(QtCore.QRect(150, 20, 101, 22))
        self.crop_drop.addItems(["Manual Crop", "Ai Crop"])
        self.crop_drop.setObjectName("crop_drop")
        self.crop_label = QtWidgets.QLabel(self.page)
        self.crop_label.setGeometry(QtCore.QRect(100, 20, 61, 21))
        self.crop_label.setObjectName("crop_label")
        self.dpi_drop = QtWidgets.QComboBox(self.page)
        self.dpi_drop.setGeometry(QtCore.QRect(330, 20, 101, 22))
        self.dpi_drop.addItems(["72", "96", "150","200", "300"])
        self.dpi_drop.setObjectName("dpi_drop")
        self.dpi_label = QtWidgets.QLabel(self.page)
        self.dpi_label.setGeometry(QtCore.QRect(260, 20, 61, 21))
        self.dpi_label.setObjectName("dpi_label")
        self.choosecam_label = QtWidgets.QLabel(self.page)
        self.choosecam_label.setGeometry(QtCore.QRect(650, 20, 101, 21))
        self.choosecam_label.setObjectName("choosecam_label")
        self.export_drop = QtWidgets.QComboBox(self.page)
        self.export_drop.setGeometry(QtCore.QRect(1130, 20, 101, 22))
        self.export_drop.addItems(["PDF", "JPEG", "TIFF"])
        self.export_drop.setObjectName("export_drop")
        self.export_label = QtWidgets.QLabel(self.page)
        self.export_label.setGeometry(QtCore.QRect(1060, 20, 61, 21))
        self.export_label.setObjectName("export_label")
        self.effect_drop = QtWidgets.QComboBox(self.page)
        self.effect_drop.setGeometry(QtCore.QRect(1330, 20, 131, 22))
        self.effect_drop.addItems(["Original","Gray", "Binarized", "Optimized Document"])
        self.effect_drop.setObjectName("effect_drop")
        self.effect_label = QtWidgets.QLabel(self.page)
        self.effect_label.setGeometry(QtCore.QRect(1280, 20, 61, 21))
        self.effect_label.setObjectName("effect_label")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.menu = QtWidgets.QWidget(self.page_2)
        self.menu.setGeometry(QtCore.QRect(10, 25, 200, 880))
        self.menu.setStyleSheet("#menu {\n"
                                "        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                                "        width:50px;\n"
                                "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                "    }\n"
                                "\n"
                                "    /* style for QPushButton and QLabel */\n"
                                "    #menu QPushButton {\n"
                                "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                "    color: white; /* Text color */\n"
                                "    font-weight: bold;\n"
                                " border: 2px solid #4CAF50; /* Border color */\n"
                                "    padding: 10px 20px;\n"
                                "        /*height:50px;*/\n"
                                "margin: 10px;\n"
                                "        \n"
                                "        /* border-bottom: 1px solid #b0b0b0; */\n"
                                "    }\n"
                                "#menu Qlabel{\n"
                                "border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                "    color: white; /* Text color */\n"
                                "    font-weight: bold;\n"
                                " border: 2px solid #4CAF50; /* Border color */\n"
                                "    padding: 10px 20px;\n"
                                "        /*height:50px;*/\n"
                                "margin: 10px;\n"
                                "}\n"
                                "\n"
                                "    #menu QPushButton:hover {\n"
                                "        background-color:#073c6d\n"
                                "    }\n"
                                "")
        self.menu.setObjectName("menu")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.menu)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.dash_label = QtWidgets.QLabel(self.menu)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dash_label.setFont(font)
        self.dash_label.setStyleSheet(" #menu QLabel{\n"
                                      "padding-top: 10px;\n"
                                      "    color: white; /* Text color */\n"
                                      "    font-weight: bold;\n"
                                      " \n"
                                      "}")
        self.dash_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dash_label.setObjectName("dash_label")
        self.verticalLayout_16.addWidget(self.dash_label)
        self.adjust_btn = QtWidgets.QPushButton(self.menu)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.adjust_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/adjust.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/adjust.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.adjust_btn.setIcon(icon3)
        self.adjust_btn.setCheckable(True)
        self.adjust_btn.setAutoExclusive(True)
        self.adjust_btn.setFlat(False)
        self.adjust_btn.setObjectName("adjust_btn")
        self.verticalLayout_16.addWidget(self.adjust_btn)
        self.color_btn = QtWidgets.QPushButton(self.menu)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/colorFilter.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/colorFilter.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.color_btn.setIcon(icon4)
        self.color_btn.setCheckable(True)
        self.color_btn.setAutoExclusive(True)
        self.color_btn.setObjectName("color_btn")
        self.verticalLayout_16.addWidget(self.color_btn)
        self.rotate_btn = QtWidgets.QPushButton(self.menu)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/rotate.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotate_btn.setIcon(icon5)
        self.rotate_btn.setObjectName("rotate_btn")
        self.verticalLayout_16.addWidget(self.rotate_btn)
        self.crop_btn = QtWidgets.QPushButton(self.menu)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/crop1.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/crop1.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.crop_btn.setIcon(icon6)
        self.crop_btn.setCheckable(True)
        self.crop_btn.setAutoExclusive(True)
        self.crop_btn.setObjectName("crop_btn")
        self.verticalLayout_16.addWidget(self.crop_btn)
        self.cam_back = QtWidgets.QPushButton(self.menu)
        self.cam_back.setStyleSheet("QPushButton {\n"
                                    "\n"
                                    "        border-radius: 20px; \n"
                                    "    color: white; /* Text color */\n"
                                    "    font-weight: bold;\n"
                                    "border:none; /* Border color */\n"
                                    "    padding: 10px 10px; /* Adjust padding as needed */\n"
                                    "    margin: 10px; /* Margin to create distance between buttons */\n"
                                    "}")
        self.cam_back.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/newPrefix/camera_back.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cam_back.setIcon(icon7)
        self.cam_back.setIconSize(QtCore.QSize(35, 35))
        self.cam_back.setCheckable(True)
        self.cam_back.setAutoExclusive(True)
        self.cam_back.setObjectName("cam_back")
        self.verticalLayout_16.addWidget(self.cam_back)
        self.verticalLayout_15.addLayout(self.verticalLayout_16)
        spacerItem = QtWidgets.QSpacerItem(
            20, 322, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_15.addItem(spacerItem)
        self.show_image = QtWidgets.QLabel(self.page_2)
        self.show_image.setGeometry( QtCore.QRect(400, 30, 1100, 661))  # 921, 661
        self.show_image.setFrameShape(QtWidgets.QFrame.Box)
        self.show_image.setText("")
        self.show_image.setStyleSheet("QLabel {"
                                      #   "border: 2px solid #0e86f6;"  # Change 'red' to desired border color
                                      "border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);"
                                      "border-radius: 10px;"   # Adjust the value for desired curve
                                      "}")
        self.show_image.setObjectName("show_image")
        label_focus_policy = self.show_image.focusPolicy()
        print(label_focus_policy)
        self.edit_stack = QtWidgets.QStackedWidget(self.page_2)
        self.edit_stack.setGeometry(QtCore.QRect(480, 720, 871, 150))
        self.edit_stack.setObjectName("edit_stack")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalSlider = QtWidgets.QSlider(self.page_3)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 50, 260, 22))
        self.horizontalSlider.setRange(-100, 100)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.page_3)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(500, 50, 260, 22))
        self.horizontalSlider_2.setRange(0, 100)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_2.setTickInterval(10)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label = QtWidgets.QLabel(self.page_3)
        self.label.setGeometry(QtCore.QRect(180, 10, 81, 41))
        self.label.setStyleSheet("QLabel {\n"
                                 "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                 "    color: #3020ee; /* Change the font color to red */\n"
                                 "}")
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.page_3)
        self.label_2.setGeometry(QtCore.QRect(680, 10, 71, 41))
        self.label_2.setStyleSheet("QLabel {\n"
                                   "    font-size: 16px; /* Change the font size to 16 pixels */\n"
                                   "    color: #3020ee; /* Change the font color to red */\n"
                                   "}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.ok_btn = QtWidgets.QPushButton(self.page_3)
        self.ok_btn.setGeometry(QtCore.QRect(340, 40, 41, 41))
        self.ok_btn.setStyleSheet("QPushButton {\n"
                                       "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                                       "        border-radius: 20px; \n"
                                       "    color: white; /* Text color */\n"
                                       "    font-weight: bold;\n"
                                       "border:none; /* Border color */\n"
                                       "    padding: 1px 1px; /* Adjust padding as needed */\n"
                                       "    margin:0px; /* Margin to create distance between buttons */\n"
                                       "}\n"
                                       " QPushButton {\n"
                                       "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                       "    color: white; /* Text color */\n"
                                       "    font-weight: bold;\n"
                                       "\n"
                                       "    padding: 1px 2px;\n"
                                       "        /*height:50px;*/\n"
                                       "margin: 0px;\n"
                                       "        \n"
                                       "        /* border-bottom: 1px solid #b0b0b0; */\n"
                                       "    }\n"
                                       " QPushButton:hover {\n"
                                       "        background-color:#073c6d\n"
                                       "    }")
        self.ok_btn.setObjectName("ok_btn")
        self.ok1_btn = QtWidgets.QPushButton(self.page_3)
        self.ok1_btn.setGeometry(QtCore.QRect(800, 40, 41, 41))
        self.ok1_btn.setStyleSheet("QPushButton {\n"
                                  "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                                  "        border-radius: 20px; \n"
                                  "    color: white; /* Text color */\n"
                                  "    font-weight: bold;\n"
                                  "border:none; /* Border color */\n"
                                  "    padding: 1px 1px; /* Adjust padding as needed */\n"
                                  "    margin:0px; /* Margin to create distance between buttons */\n"
                                  "}\n"
                                  " QPushButton {\n"
                                  "        border-radius: 10px; /* Adjust the value to change the curve radius */\n"
                                  "    color: white; /* Text color */\n"
                                  "    font-weight: bold;\n"
                                  "\n"
                                  "    padding: 1px 2px;\n"
                                  "        /*height:50px;*/\n"
                                  "margin: 0px;\n"
                                  "        \n"
                                  "        /* border-bottom: 1px solid #b0b0b0; */\n"
                                  "    }\n"
                                  " QPushButton:hover {\n"
                                  "        background-color:#073c6d\n"
                                  "    }")
        self.ok1_btn.setObjectName("ok1_btn")
        self.edit_stack.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.enhance_btn = QtWidgets.QPushButton(self.page_4)
        self.enhance_btn.setGeometry(QtCore.QRect(100, 0, 211, 41))
        self.enhance_btn.setStyleSheet("QPushButton {\n"
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
                                       " QPushButton:hover {\n"
                                       "        background-color:#073c6d\n"
                                       "    }")
        self.enhance_btn.setObjectName("enhance_btn")
        self.mag1_btn = QtWidgets.QPushButton(self.page_4)
        self.mag1_btn.setGeometry(QtCore.QRect(604, 0, 211, 41))
        self.mag1_btn.setStyleSheet("QPushButton {\n"
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
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        self.mag1_btn.setObjectName("mag1_btn")
        self.color_btn_2 = QtWidgets.QPushButton(self.page_4)
        self.color_btn_2.setGeometry(QtCore.QRect(100, 50, 211, 41))
        self.color_btn_2.setStyleSheet("QPushButton {\n"
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
                                       " QPushButton:hover {\n"
                                       "        background-color:#073c6d\n"
                                       "    }")
        self.color_btn_2.setObjectName("color_btn_2")
        self.mag2_btn = QtWidgets.QPushButton(self.page_4)
        self.mag2_btn.setGeometry(QtCore.QRect(604, 50, 211, 41))
        self.mag2_btn.setStyleSheet("QPushButton {\n"
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
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        self.mag2_btn.setObjectName("mag2_btn")
        self.edit_stack.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.rotateleft_btn = QtWidgets.QPushButton(self.page_5)
        self.rotateleft_btn.setGeometry(QtCore.QRect(100, 30, 211, 41))
        self.rotateleft_btn.setStyleSheet("QPushButton {\n"
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
                                          " QPushButton:hover {\n"
                                          "        background-color:#073c6d\n"
                                          "    }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/newPrefix/rotateLeft.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateleft_btn.setIcon(icon9)
        self.rotateleft_btn.setObjectName("rotateleft_btn")
        self.rotateright_btn = QtWidgets.QPushButton(self.page_5)
        self.rotateright_btn.setGeometry(QtCore.QRect(604, 30, 211, 41))
        self.rotateright_btn.setStyleSheet("QPushButton {\n"
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
                                           " QPushButton:hover {\n"
                                           "        background-color:#073c6d\n"
                                           "    }")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(
            ":/newPrefix/rotateRight.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateright_btn.setIcon(icon10)
        self.rotateright_btn.setObjectName("rotateright_btn")
        self.edit_stack.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.edit_stack.addWidget(self.page_6)
        self.undo_btn = QtWidgets.QPushButton(self.page_2)
        self.undo_btn.setGeometry(QtCore.QRect(350, 850, 211, 41))
        self.undo_btn.setStyleSheet("QPushButton {\n"
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
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/newPrefix/undo1.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undo_btn.setIcon(icon8)
        self.undo_btn.setObjectName("undo_btn")
        self.discard_btn = QtWidgets.QPushButton(self.page_2)
        self.discard_btn.setGeometry(QtCore.QRect(840, 850, 211, 41))
        self.discard_btn.setStyleSheet("QPushButton {\n"
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
                                       " QPushButton:hover {\n"
                                       "        background-color:#073c6d\n"
                                       "    }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/newPrefix/discard.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.discard_btn.setIcon(icon9)
        self.discard_btn.setObjectName("discard_btn")
        self.save_btn = QtWidgets.QPushButton(self.page_2)
        self.save_btn.setGeometry(QtCore.QRect(1350, 850, 211, 41))
        self.save_btn.setStyleSheet("QPushButton {\n"
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
                                    "\n"
                                    " QPushButton:hover {\n"
                                    "        background-color:#073c6d\n"
                                    "    }")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/newPrefix/save.svg"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_btn.setIcon(icon10)
        self.save_btn.setObjectName("save_btn")
        self.stackedWidget.addWidget(self.page_2)
        self.nav = QtWidgets.QWidget(self.centralwidget)
        self.nav.setGeometry(QtCore.QRect(0, 0, 1980, 40))
        self.nav.setStyleSheet("#nav {\n"
                               "        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa);\n"
                               "        width:50px;\n"
                               "        /*border-radius: 10px; *//* Adjust the value to change the curve radius */\n"
                               "    }\n"
                               "\n"
                               "    /* style for QPushButton and QLabel */\n"
                               "    #nav QPushButton {\n"
                               "        border-radius: 1px; /* Adjust the value to change the curve radius */\n"
                               "    color: white; /* Text color */\n"
                               "    font-weight: bold;\n"
                               " /*border: 2px solid #4CAF50; *//* Border color */\n"
                               "    padding: 10px 20px;\n"
                               "        /*height:50px;*/\n"
                               "margin: 10px;\n"
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
        self.nav.setObjectName("nav")
        self.label_3 = QtWidgets.QLabel(self.nav)
        self.label_3.setGeometry(QtCore.QRect(10, 5, 31, 30))
        self.label_3.setMinimumSize(QtCore.QSize(20, 20))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/newPrefix/logo (1).svg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.name = QtWidgets.QLabel(self.nav)
        self.name.setGeometry(QtCore.QRect(50, -10, 461, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setStyleSheet("#name{\n"
                                "    color: white; /* Text color */\n"
                                "    font-weight: bold;\n"
                                "}\n"
                                "\n"
                                "")
        self.name.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignJustify)
        self.name.setObjectName("name")
        self.minimize = QtWidgets.QPushButton(self.nav)
        self.minimize.setGeometry(QtCore.QRect(1830, -10, 51, 61))
        self.minimize.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/newPrefix/minimize.svg"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize.setIcon(icon13)
        self.minimize.setIconSize(QtCore.QSize(18, 18))
        self.minimize.setObjectName("minimize")
        self.close = QtWidgets.QPushButton(self.nav)
        self.close.setGeometry(QtCore.QRect(1870, -10, 51, 61))
        self.close.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/newPrefix/close.svg"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon14)
        self.close.setIconSize(QtCore.QSize(20, 20))
        self.close.setObjectName("close")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.edit_stack.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DocScanner"))
        self.pdf_btn.setText(_translate("MainWindow", " Export"))
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.camset_btn.setText(_translate("MainWindow", "Camera Settings"))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.dash_label.setText(_translate("MainWindow", "Customize"))
        self.adjust_btn.setText(_translate("MainWindow", "Adjust"))
        self.color_btn.setText(_translate("MainWindow", "Color Mode"))
        self.rotate_btn.setText(_translate("MainWindow", "Rotate"))
        self.crop_btn.setText(_translate("MainWindow", "Crop"))
        self.label.setText(_translate("MainWindow", "Contrast"))
        self.label_2.setText(_translate("MainWindow", "Sharpness"))
        self.enhance_btn.setText(_translate("MainWindow", "Enhance"))
        self.mag1_btn.setText(_translate("MainWindow", "Magic Color 1"))
        self.color_btn_2.setText(_translate("MainWindow", "Color"))
        self.mag2_btn.setText(_translate("MainWindow", "Magic Color 2"))
        self.rotateleft_btn.setText(_translate("MainWindow", " Left"))
        self.rotateright_btn.setText(_translate("MainWindow", " Right"))
        self.undo_btn.setText(_translate("MainWindow", "Undo"))
        self.discard_btn.setText(_translate("MainWindow", "Discard"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.ok_btn.setText(_translate("MainWindow", "OK"))
        self.ok1_btn.setText(_translate("MainWindow", "OK"))
        self.settings_btn.setText(_translate("MainWindow", "Manual Crop"))
        self.name.setText(_translate("MainWindow", "Aeonix Document Scanner"))
        # self.ai_btn.setText(_translate("MainWindow", "AI Mode"))
        self.foc_label.setText(_translate("MainWindow", "Set Focus:"))
        self.export_label.setText(_translate("MainWindow", "Export to:"))
        self.choosecam_label.setText(_translate("MainWindow", "Select Camera:"))
        self.dpi_label.setText(_translate("MainWindow", "Select DPI:"))
        self.resolution_label.setText(_translate("MainWindow", "Resolution:"))
        self.effect_label.setText(_translate("MainWindow", "Effect:"))
        self.autoSave_btn.setText(_translate("MainWindow", "Auto Save"))
        self.trim_btn.setText(_translate("MainWindow", "Trim"))
        self.crop_label.setText(_translate("MainWindow", "Crop:"))




