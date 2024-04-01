# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/pdas/AppData/Local/Temp/sidebarNewGxQaaU.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QFont,QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QScrollArea


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 502)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.icon_only_widget = QtWidgets.QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName("icon_only_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.logo_label_1 = QtWidgets.QLabel(self.icon_only_widget)
        self.logo_label_1.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setMaximumSize(QtCore.QSize(50, 50))
        self.logo_label_1.setText("")
        self.logo_label_1.setPixmap(QtGui.QPixmap(r":/icon/icon/logoNew.png"))
        self.logo_label_1.setScaledContents(True)
        self.logo_label_1.setObjectName("logo_label_1")
        self.horizontalLayout_3.addWidget(self.logo_label_1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cam_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.cam_btn_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r":/icon/icon/camera32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(r":/icon/icon/camera48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cam_btn_1.setIcon(icon)
        self.cam_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.cam_btn_1.setCheckable(True)
        self.cam_btn_1.setAutoExclusive(True)
        self.cam_btn_1.setObjectName("cam_btn_1")
        self.verticalLayout.addWidget(self.cam_btn_1)
        self.scan_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.scan_btn_1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r":/icon/icon/scan32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(r":/icon/icon/scan48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.scan_btn_1.setIcon(icon1)
        self.scan_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.scan_btn_1.setCheckable(True)
        self.scan_btn_1.setAutoExclusive(True)
        self.scan_btn_1.setObjectName("scan_btn_1")
        self.verticalLayout.addWidget(self.scan_btn_1)
        self.upload_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.upload_btn_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r":/icon/icon/upload32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(r":/icon/icon/upload48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.upload_btn_1.setIcon(icon2)
        self.upload_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.upload_btn_1.setCheckable(True)
        self.upload_btn_1.setAutoExclusive(True)
        self.upload_btn_1.setObjectName("upload_btn_1")
        self.verticalLayout.addWidget(self.upload_btn_1)
        self.help_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.help_btn_1.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r":/icon/icon/help32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(r":/icon/icon/help48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.help_btn_1.setIcon(icon3)
        self.help_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.help_btn_1.setCheckable(True)
        self.help_btn_1.setAutoExclusive(True)
        self.help_btn_1.setObjectName("help_btn_1")
        self.verticalLayout.addWidget(self.help_btn_1)
        self.settings_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.settings_btn_1.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r":/icon/icon/setting32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(r":/icon/icon/setting48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.settings_btn_1.setIcon(icon4)
        self.settings_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.settings_btn_1.setCheckable(True)
        self.settings_btn_1.setAutoExclusive(True)
        self.settings_btn_1.setObjectName("settings_btn_1")
        self.verticalLayout.addWidget(self.settings_btn_1)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 375, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.exit_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.exit_btn_1.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(r":/icon/icon/close-window-64.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn_1.setIcon(icon5)
        self.exit_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn_1.setObjectName("exit_btn_1")
        self.verticalLayout_3.addWidget(self.exit_btn_1)
        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)
        self.full_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo_label_2 = QtWidgets.QLabel(self.full_menu_widget)
        self.logo_label_2.setMinimumSize(QtCore.QSize(40, 40))
        self.logo_label_2.setMaximumSize(QtCore.QSize(40, 40))
        self.logo_label_2.setText("")
        self.logo_label_2.setPixmap(QtGui.QPixmap(r":/icon/icon/logoNew.png"))
        self.logo_label_2.setScaledContents(True)
        self.logo_label_2.setObjectName("logo_label_2")
        self.horizontalLayout_2.addWidget(self.logo_label_2)
        self.logo_label_3 = QtWidgets.QLabel(self.full_menu_widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.logo_label_3.setFont(font)
        self.logo_label_3.setObjectName("logo_label_3")
        self.horizontalLayout_2.addWidget(self.logo_label_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cam_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.cam_btn_2.setIcon(icon)
        self.cam_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.cam_btn_2.setCheckable(True)
        self.cam_btn_2.setAutoExclusive(True)
        self.cam_btn_2.setObjectName("cam_btn_2")
        self.verticalLayout_2.addWidget(self.cam_btn_2)
        self.scan_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.scan_btn_2.setIcon(icon1)
        self.scan_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.scan_btn_2.setCheckable(True)
        self.scan_btn_2.setAutoExclusive(True)
        self.scan_btn_2.setObjectName("scan_btn_2")
        self.verticalLayout_2.addWidget(self.scan_btn_2)
        self.upload_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.upload_btn_2.setIcon(icon2)
        self.upload_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.upload_btn_2.setCheckable(True)
        self.upload_btn_2.setAutoExclusive(True)
        self.upload_btn_2.setObjectName("upload_btn_2")
        self.verticalLayout_2.addWidget(self.upload_btn_2)
        self.help_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.help_btn_2.setIcon(icon3)
        self.help_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.help_btn_2.setCheckable(True)
        self.help_btn_2.setAutoExclusive(True)
        self.help_btn_2.setObjectName("help_btn_2")
        self.verticalLayout_2.addWidget(self.help_btn_2)
        self.settings_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.settings_btn_2.setIcon(icon4)
        self.settings_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.settings_btn_2.setCheckable(True)
        self.settings_btn_2.setAutoExclusive(True)
        self.settings_btn_2.setObjectName("settings_btn_2")
        self.verticalLayout_2.addWidget(self.settings_btn_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 373, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.exit_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.exit_btn_2.setIcon(icon5)
        self.exit_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.exit_btn_2.setObjectName("exit_btn_2")
        self.verticalLayout_4.addWidget(self.exit_btn_2)
        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.change_btn = QtWidgets.QPushButton(self.widget)
        self.change_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(r":/icon/icon/menu-4-32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.change_btn.setIcon(icon6)
        self.change_btn.setIconSize(QtCore.QSize(14, 14))
        self.change_btn.setCheckable(True)
        self.change_btn.setObjectName("change_btn")
        self.horizontalLayout_4.addWidget(self.change_btn)
        spacerItem2 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search_input = QtWidgets.QLineEdit(self.widget)
        self.search_input.setObjectName("search_input")
        self.horizontalLayout.addWidget(self.search_input)
        self.search_btn = QtWidgets.QPushButton(self.widget)
        self.search_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(r":/icon/icon/search-13-48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon7)
        self.search_btn.setObjectName("search_btn")
        self.horizontalLayout.addWidget(self.search_btn)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_5.addWidget(self.widget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(50, 11, 731, 441)) #(9, 11, 531, 441))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setLineWidth(2)
        self.label.setText("")
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.page)
        self.layoutWidget.setGeometry(QtCore.QRect(800, 170, 54, 94)) #(550, 170, 54, 94)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.capture = QtWidgets.QPushButton(self.layoutWidget)
        self.capture.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(r":/icon/icon/camera48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.capture.setIcon(icon8)
        self.capture.setIconSize(QtCore.QSize(40, 40))
        self.capture.setCheckable(True)
        self.capture.setAutoExclusive(True)
        self.capture.setFlat(True)
        self.capture.setObjectName("capture")
        self.verticalLayout_6.addWidget(self.capture)
        self.show = QtWidgets.QPushButton(self.layoutWidget) 
        self.show.setText("Make Pdf")
        icon9 = QtGui.QIcon()
        # icon9.addPixmap(QtGui.QPixmap(r"C:\Users\pdas\Desktop\Project\icon\camera48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show.setIcon(icon9)
        self.show.setIconSize(QtCore.QSize(30, 30))
        self.show.setCheckable(True)
        self.show.setAutoExclusive(True)
        self.show.setFlat(True)
        self.show.setObjectName("show")
        self.verticalLayout_6.addWidget(self.show)


        # Create a layout for the page
        self.page_layout = QHBoxLayout(self.page)
        self.page_layout.setContentsMargins(0, 500, 0, 0)
        self.page_layout.setSpacing(0)

        # # Create a scroll area to contain the images
        # self.scrollArea = QScrollArea(self.page)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Allow horizontal scrolling
        # self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrolling
        # self.scrollArea.setObjectName("scrollArea")

        # Set the scroll area as the central widget of the main window
        # self.centralwidget(self.scrollArea)

        # Create a widget to contain the images horizontally
        self.image_container = QWidget()
        self.image_container.setObjectName("image_container")

        # Create a layout for the image container
        self.image_layout = QHBoxLayout(self.image_container)
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_layout.setSpacing(0)

        # Add a drop-down menu
        self.dropdown_menu = QtWidgets.QComboBox(self.page)
        self.dropdown_menu.setGeometry(QtCore.QRect(900, 22, 150, 30)) #(550, 270, 150, 30)
        self.dropdown_menu.setObjectName("dropdown_menu")
        # # Add items to the drop-down menu
        # self.dropdown_menu.addItem("Option 1")
        # self.dropdown_menu.addItem("Option 2")
        # self.dropdown_menu.addItem("Option 3")




        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.page_7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.stackedWidget.addWidget(self.page_7)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.change_btn.toggled['bool'].connect(self.icon_only_widget.setVisible) # type: ignore
        self.change_btn.toggled['bool'].connect(self.full_menu_widget.setHidden) # type: ignore
        self.cam_btn_1.toggled['bool'].connect(self.cam_btn_2.setChecked) # type: ignore
        self.scan_btn_1.toggled['bool'].connect(self.scan_btn_2.setChecked) # type: ignore
        self.upload_btn_1.toggled['bool'].connect(self.upload_btn_2.setChecked) # type: ignore
        self.help_btn_1.toggled['bool'].connect(self.help_btn_2.setChecked) # type: ignore
        self.settings_btn_1.toggled['bool'].connect(self.settings_btn_2.setChecked) # type: ignore
        self.cam_btn_2.toggled['bool'].connect(self.cam_btn_1.setChecked) # type: ignore
        self.scan_btn_2.toggled['bool'].connect(self.scan_btn_1.setChecked) # type: ignore
        self.upload_btn_2.toggled['bool'].connect(self.upload_btn_1.setChecked) # type: ignore
        self.help_btn_2.toggled['bool'].connect(self.help_btn_1.setChecked) # type: ignore
        self.settings_btn_2.toggled['bool'].connect(self.settings_btn_1.setChecked) # type: ignore
        self.exit_btn_2.clicked.connect(MainWindow.close) # type: ignore
        self.exit_btn_1.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
        MainWindow.setStyleSheet("""
        /*= Style for mainwindow START
  ==================================================== */
	#MainWindow {
		background-color: #fff;
	}
/*= END
  ==================================================== */

/*= Style for button to change menu style START
  ==================================================== */
	#change_btn {
		padding: 5px;
		border: none;
		width: 30px;
		height: 30px;
	}
/*= END
  ==================================================== */

/*= Style for header widget START
  ==================================================== */
	#widget {
		background-color: #f9fafd;
	}
/*= END
  ==================================================== */

/*= Style for menu with icon only START
  ==================================================== */
  	/* style for widget */
	#icon_only_widget {
		background-color: #ADD8E6;
		width:50px;
	}

    /* style for QPushButton and QLabel */
	#icon_only_widget QPushButton, QLabel {
		height:50px;
		border:none;
		/* border-bottom: 1px solid #b0b0b0; */
	}

	#icon_only_widget QPushButton:hover {
		background-color: rgba( 86, 101, 115, 0.5);
	}

	/* style for logo image */
	#logo_label_1 {
		padding: 5px
	}
/*= END
  ==================================================== */

/*= Style for menu with icon and text START
  ==================================================== */
	/* style for widget */
	#full_menu_widget {
		background-color: #ADD8E6;;
	}

	/* style for QPushButton */
	#full_menu_widget QPushButton {
		border:none;
		border-radius: 3px;
		text-align: left;
		padding: 8px 0 8px 15px;
		color: #788596;
	}

	#full_menu_widget QPushButton:hover {
		background-color: rgba( 86, 101, 115, 0.5);
	}

	#full_menu_widget QPushButton:checked {
		color: #fff;
	}

	/* style for logo image */
	#logo_label_2 {
		padding: 5px;
		color: #fff;
	}

	/* style for APP title */
	#logo_label_3 {
		padding-right: 10px;
		color: #fff;
	}
/*= END
  ==================================================== */

/*= Style for search button START
  ==================================================== */
	#search_btn {
		border: none;
	}
/*= END
  ==================================================== */

/*= Style for search input START
  ==================================================== */
	#search_input {
		border: none;
		padding: 5px 10px;
	}

	#search_input:focus {
		background-color: #70B9FE;
	}
/*= END
  ==================================================== */

/*= Style for user information button START
  ==================================================== */
	#user_btn {
		border: none;
	}
/*= END
  ==================================================== */ 
    """)
        
        


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo_label_3.setText(_translate("MainWindow", "Dashboard"))
        self.cam_btn_2.setText(_translate("MainWindow", "Camera"))
        self.scan_btn_2.setText(_translate("MainWindow", "Scan Image"))
        self.upload_btn_2.setText(_translate("MainWindow", "Uploads"))
        self.help_btn_2.setText(_translate("MainWindow", "Help"))
        self.settings_btn_2.setText(_translate("MainWindow", "Settings"))
        self.exit_btn_2.setText(_translate("MainWindow", "Exit"))
        self.search_input.setPlaceholderText(_translate("MainWindow", "Search..."))
import resourceNew_rc

# class VideoStream:
#     def __init__(self, parent_label: QLabel, camera_index):
#         self.video = cv2.VideoCapture(camera_index)
#         self.parent_label = parent_label
#         self.set_resolution()

#     def set_resolution(self):
#         # Check if 4K resolution is supported by the camera
#         # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 3840) #3840
#         # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160) #2160
#         width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         if width == 3840 and height == 2160:
#             # If 4K resolution is supported, set to 4K
#             self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 3840) #3840
#             self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160) #216
#             return
#         else:
#             # Set to default resolution
#             self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#             self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#     def display_camera_feed(self):
#         if not self.video.isOpened():
#             # If camera is not available, display text in the label
#             font = QFont()
#             font.setPointSize(30)  # Set font size to 20
#             self.parent_label.setFont(font)
#             self.parent_label.setText("<p style='font-size:20pt'>No camera is attached</p>")
#             return
        
#         ret, frame = self.video.read()
#         if ret: 
#             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = rgb_image.shape
#             bytes_per_line = ch * w
#             q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(q_img)
#             self.parent_label.setPixmap(pixmap.scaled(self.parent_label.size(), Qt.KeepAspectRatio))

#     def change_camera(self, camera_index):
#         self.video.release()  # Release previous video capture
#         self.video = cv2.VideoCapture(camera_index)  # Open new video capture with new camera index
#         self.set_resolution()  # Set resolution for new camera
#         self.display_camera_feed()

# class VideoStream:
#     def __init__(self, parent_label: QLabel, camera_index):
#         self.video = cv2.VideoCapture(camera_index)
#         self.parent_label = parent_label
#         self.set_resolution()

#     def set_resolution(self):
#         # Check if camera is open
#         if not self.video.isOpened():
#             print("Error opening camera")
#             return

#         # Check if 4K resolution is supported
#         # Typo fix in height value
#         # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
#         # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
#         # width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
#         # height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         # if width == 3840 and height == 2160:
#         #     print("Using 4K resolution")
#         # else:
#         #     self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#         #     self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#         #     print("Using 1080p resolution")

#     def display_camera_feed(self):
#         if not self.video.isOpened():
#             # Display error message if camera not open
#             font = QFont()
#             font.setPointSize(30)
#             self.parent_label.setFont(font)
#             self.parent_label.setText("<p style='font-size:20pt'>Err opening camera</p>")
#             return

#         ret, frame = self.video.read()
#         if ret:
#             self.show_loader()

#             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = rgb_image.shape
#             bytes_per_line = ch * w
#             q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(q_img)
#             self.parent_label.setPixmap(pixmap.scaled(self.parent_label.size(), Qt.KeepAspectRatio))

#             # Hide loader after setting the frame
#             self.hide_loader()
            
#     def show_loader(self):
#         # Display loader in parent_label while loading camera feed
#         loader_movie = QMovie("loader.gif")  # Replace "loader.gif" with your loader image path
#         self.loader_label.setMovie(loader_movie)
#         loader_movie.start()

#         # Set the loader label to the center of the parent label
#         self.loader_label.setGeometry(
#             self.parent_label.width() // 2 - 50,  # Adjust the loader position as needed
#             self.parent_label.height() // 2 - 50,
#             100,  # Width of the loader label
#             100   # Height of the loader label
#         )
#         self.loader_label.setParent(self.parent_label)
#         self.loader_label.show()

#     # def change_camera(self, camera_index):
#     #     # Wait for 1 second before opening the new camera index
#     #     self.video.release()
        
#     #     # Wait for a moment before opening the new camera index

#     #     # Open the new camera capture
#     #     self.video = cv2.VideoCapture(camera_index)
#     #     self.set_resolution()

#     #     # Create a QTimer object with the appropriate parent widget
#     #     timer = QTimer()
#     #     timer.timeout.connect(self.display_camera_feed)
#     #     timer.start(10) 
#     def hide_loader(self):
#         # Hide loader from parent_label
#         self.parent_label.clear()
#     def change_camera(self, camera_index):
#         # Wait for 1 second before opening the new camera index
#         self.video.release()
        
#         # Wait for a moment before opening the new camera index

#         # Open the new camera capture
#         self.video = cv2.VideoCapture(camera_index)
#         self.set_resolution()

#         # Create a QTimer object with the appropriate parent widget
#         timer = QTimer()
#         timer.timeout.connect(self.display_camera_feed)
#         timer.start(10) 
        
        
        
        
        
import threading

class VideoStream:
    def __init__(self, parent_label: QLabel, camera_index):
        self.video = cv2.VideoCapture(camera_index)
        self.parent_label = parent_label
        self.set_resolution()
        self.timer = None
        self.camera_change_thread = None  # Thread for camera switching

    def set_resolution(self):
        # Check if camera is open
        if not self.video.isOpened():
            print("Error opening camera")
            return

        # Check if 4K resolution is supported
        # Typo fix in height value
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(width)
        print(height)
        # if width == 3840 and height == 2160:
        #     print("Using 4K resolution")
        # else:
        #     self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #     self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #     print("Using 1080p resolution")
        # ... (rest of your set_resolution logic)

    def display_camera_feed(self):
        if not self.video.isOpened():
            # Display error message if camera not open
          font = QFont()
          font.setPointSize(30)
          self.parent_label.setFont(font)
          self.parent_label.setText("<p style='font-size:20pt'>Changing Camera...</p>")
          return

        ret, frame = self.video.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(rgb_image, (640, 480))
            h, w, ch = frame_resized.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_resized.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.parent_label.setPixmap(pixmap.scaled(self.parent_label.size(), Qt.KeepAspectRatio))
        else:
            # Display loader while camera is changing
            self.show_loader()

    def change_camera(self, camera_index):
        # Stop the timer if it's running
        if self.timer is not None:
            self.timer.stop()

        # Create a thread for camera switching (optional, but recommended for responsiveness)
        self.camera_change_thread = threading.Thread(target=self._change_camera_in_thread, args=(camera_index,))
        self.camera_change_thread.start()
        # Display loader immediately
        self.show_loader()

    def _change_camera_in_thread(self, camera_index):
        # Release the current video capture
        self.video.release()

        # Open the new camera capture
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.set_resolution()

        # Create a QTimer object and connect it to the display_camera_feed function (in main thread)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_camera_feed)
        self.timer.start(10)  # Start the timer with a 10ms interval

    def show_loader(self):
        font = QFont()
        font.setPointSize(30)
        self.parent_label.setFont(font)
        self.parent_label.setText("<p style='font-size:20pt'>Changing Camera...</p>")
