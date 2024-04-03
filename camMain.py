from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from camDesign import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
from Sidebar1 import Ui_MainWindow,  VideoStream
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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindoww()
        self.ui.setupUi(self)
        self.captured_images=[]
        self.current_camera_index = 0  # Index of the currently selected camera
        self.video_stream = VideoStream(self.ui.cam_label,self.current_camera_index)  # Initialize video stream with default camera
        self.ui.shutter_btn.clicked.connect(self.capture_image) 
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.ui.shutter_btn.clicked.connect(self.capture_image) 
        
        
    def capture_image(self):
        ret, frame = self.video_stream.video.read()
        
        if ret:
            # Define the cropping geometry
            # crop_x = 987
            # crop_y = 448
            # crop_width = 1828
            # crop_height = 1333
            
            # # Ensure that the cropping rectangle does not exceed the dimensions of the frame
            # max_width = frame.shape[1]
            # max_height = frame.shape[0]
            
            # crop_x = min(crop_x, max_width)
            # crop_y = min(crop_y, max_height)
            # crop_width = min(crop_width, max_width - crop_x)
            # crop_height = min(crop_height, max_height - crop_y)
            
            # # Crop the frame
            # cropped_frame = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]
            
            # if not cropped_frame.size == 0:  # Check if the cropped frame is not empty
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
                filename = f"captured_image_{timestamp}.jpg"
                
                
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()

                # Specify the filepath within the temporary directory
                filepath = os.path.join(temp_dir, filename)

                try:
                    cv2.imwrite(filepath, frame)  # Save the cropped image with timestamp
                    print("Image saved successfully.")

                    # Append the filepath to the captured images list
                    self.captured_images.append(filepath)

                    # Call display_captured_images to update the display
                    self.display_captured_images()

                except Exception as e:
                    print(f"Error saving image: {e}")
                    
                    
    def display_captured_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.horizontalLayout.count())):
            self.ui.horizontalLayout.itemAt(i).widget().setParent(None)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Display captured images
        for index, image_path in enumerate(self.captured_images):
            label = QLabel()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
            pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda event, index=index: self.image_clicked(index)  # Connect click event
            scroll_layout.addWidget(label)
            # Add context menu for each image
            label.setContextMenuPolicy(Qt.CustomContextMenu)
            label.customContextMenuRequested.connect(lambda point, index=index, label=label: self.open_context_menu(point, index, label))

        # Add the scroll area to the main layout
        self.ui.horizontalLayout.addWidget(scroll_area)
    def image_clicked(self, index):
        print("Clicked on image:", index)

    def clear_displayed_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.horizontalLayout.count())):
            self.ui.horizontalLayout.itemAt(i).widget().setParent(None)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
