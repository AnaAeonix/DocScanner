import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from StackDesign import Ui_MainWindow  # replace 'your_ui_file' with the name of your UI file
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
# from Sidebar1 import Ui_MainWindow,  VideoStream
import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QLabel, QScrollArea, QHBoxLayout, QWidget, QMenu, QFileDialog
from PyQt5.QtCore import QTimer,  Qt
from PyQt5.QtGui import QPixmap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import tempfile
import threading
from functools import partial
from PyQt5.QtGui import QImage, QPixmap, QFont
from camDes1main import MainWindow1

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.captured_images=[]
        self.cam_thread = None
        self.cam_thread = QThread()
        self.cam_window = MainWindow1()
        self.cam_window.moveToThread(self.cam_thread)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.back_btn.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_2.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_3.clicked.connect(self.clicked_back_btn)
        self.ui.pdf_btn.clicked.connect(self.make_pdf)
        self.ui.scan_btn.clicked.connect(self.open_camWindow)



    def clicked_adjust_btn(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        
    def make_pdf(self):
        # Ask the user for the save path
        save_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf)")
        if save_path:
            if self.captured_images:
                pdf_canvas = canvas.Canvas(save_path, pagesize=letter)
                for image_path in self.captured_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        pdf_canvas.setPageSize((width, height))  # Set the PDF page size same as image size
                        pdf_canvas.drawImage(image_path, 0, 0, width, height)  # Place image on PDF
                        pdf_canvas.showPage()  # End current page
                pdf_canvas.save()
                print("PDF saved successfully.")
                self.clear_displayed_images()
                self.captured_images.clear()
            else:
                print("No images to save.")
        else:
            print("Save operation cancelled by the user.")
        

    def clicked_color_btn(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def clicked_rotate_btn(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def clicked_back_btn(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def open_camWindow(self):
        if not self.cam_thread or not self.cam_thread.isRunning():
            self.cam_thread.started.connect(self.cam_window.show)
            self.cam_thread.start()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
