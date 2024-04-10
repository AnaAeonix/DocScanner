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

    def closeEvent(self, event):
        # Perform actions after closing the window
        print("Window closed")
        # For example, you can save some data or perform cleanup operations here
        super(MainWindow, self).closeEvent(event)
    def open_camWindow(self):
        if not self.cam_thread or not self.cam_thread.isRunning():
            self.cam_thread.started.connect(self.cam_window.show)
            self.cam_thread.start()
            
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea
# from PyQt5.QtCore import QThread, pyqtSignal
# from PyQt5.QtGui import QPixmap
# import cv2

# class MainWindow1(QWidget):
#     def __init__(self):
#         super(MainWindow1, self).__init__()
#         self.setWindowTitle("Main Window 1")
#         self.setGeometry(100, 100, 500, 500)

#         self.scroll_area = QScrollArea()
#         self.scroll_widget = QWidget()
#         self.scroll_layout = QVBoxLayout(self.scroll_widget)
#         self.scroll_area.setWidget(self.scroll_widget)
#         self.scroll_area.setWidgetResizable(True)

#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.scroll_area)

#         self.load_images()

#     def load_images(self):
#         # Load and display images (dummy implementation)
#         for i in range(10):
#             label = QLabel()
#             pixmap = QPixmap("image.jpg")  # Replace "image.jpg" with your image path
#             label.setPixmap(pixmap)
#             self.scroll_layout.addWidget(label)

# class ChildWindowThread(QThread):
#     child_window_created = pyqtSignal()

#     def run(self):
#         self.child_window = MainWindow1()
#         self.child_window_created.emit()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle("Main Window")
#         self.setGeometry(200, 200, 500, 300)

#         self.child_window_thread = ChildWindowThread()
#         self.child_window_thread.child_window_created.connect(self.child_window_created)

#         self.btn = QPushButton("Show Child Window", self)
#         self.btn.setGeometry(150, 100, 200, 50)
#         self.btn.clicked.connect(self.show_child_window)

#     def show_child_window(self):
#         self.child_window_thread.start()

#     def child_window_created(self):
#         self.child_window = self.child_window_thread.child_window
#         self.child_window.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
