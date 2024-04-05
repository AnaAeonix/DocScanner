import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from camDes1 import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import cv2
import os
import tempfile
from datetime import datetime
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QCheckBox
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
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QObject
import tempfile
import threading
from functools import partial
from PyQt5.QtGui import QImage, QPixmap, QFont
from camDes1main import MainWindow1


class ChildWindow(QMainWindow):
    imageCaptured = pyqtSignal(str)

    windowClosed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindoww()
        self.ui.setupUi(self)
        global image_list
        image_list=[]
        

        self.captured_images = []
        self.current_camera_index = 0
        self.video_stream = VideoStream(self.ui.cam_label,self.current_camera_index)  # Initialize video stream with default camera
        self.ui.shutter_btn.clicked.connect(self.capture_image) 
        self.ui.done_btn.clicked.connect(self.clicked_done_btn) 
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown() 
        # self.ui.shutter_btn.clicked.connect(self.capture_image)
        
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
        layout = self.ui.show_label.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Ensure that show_label has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.show_label.setLayout(layout)

        # Display captured images if the list is not empty
        if self.captured_images:
            # Create a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_area.setWidget(scroll_content)

            # Display captured images
            for index, image_path in enumerate(self.captured_images):
                label = QLabel()
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
                pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
                label.setPixmap(pixmap)
                scroll_layout.addWidget(label)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)
        
    def image_clicked(self, index):
        print("Clicked on image:", index)

    def clear_displayed_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.show_label.layout().count())):
            self.ui.show_label.layout().itemAt(i).widget().setParent(None)
            
        
    def populate_camera_dropdown(self):
        global available_cameras
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                backend_id = cap.get(cv2.CAP_PROP_BACKEND)
                camera_name = f"Camera {i} - Backend: {backend_id}"
                available_cameras.append((i, camera_name))
                del cap
        camera_names = [camera_name for _, camera_name in available_cameras]
        self.ui.drop_down.addItems(camera_names)
        self.ui.drop_down.currentIndexChanged.connect(lambda: self._handle_index_change())

    def _handle_index_change(self):
        self.current_camera_index = self.ui.drop_down.currentIndex()  # Access the current index
    # Do something with the new_index value
        self.video_stream.change_camera(self.current_camera_index) # Call your function with the index


    
    def clicked_done_btn(self):
        self.clear_displayed_images()
        global image_list 
        for i in self.captured_images:
            image_list.append(i)
        print(self.captured_images)
        self.captured_images.clear()
        print(image_list)


    def closeEvent(self, event):
        self.windowClosed.emit()
        super().closeEvent(event)






    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.back_btn.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_2.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_3.clicked.connect(self.clicked_back_btn)
        self.ui.pdf_btn.clicked.connect(self.make_pdf)
        # self.ui.crop_btn.clicked.connect(self.clicked_crop_btn)
        self.ui.scan_btn.clicked.connect(self.toggle_child_window)
        self.child_window = ChildWindow()     
        self.captured_imagesParent=[]
        # Thread to start the child window
        self.child_thread = QThread()
        self.child_window.moveToThread(self.child_thread)
        self.child_thread.started.connect(self.child_window.hide)
        self.child_thread.start()

        self.child_window.windowClosed.connect(self.display_captured_images_main)

        # Create a dictionary to store references to labels corresponding to image paths
        self.image_labels = {}
        self.current_displayed_image = None  # Track the currently displayed image

        self.selected_images = []  # Store selected images
        self.all_checkboxes = []   # Store references to all checkboxes


    def clicked_adjust_btn(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        
    def make_pdf(self):
        # Ask the user for the save path
        save_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf)")
        if save_path:
            if self.selected_images:
                pdf_canvas = canvas.Canvas(save_path, pagesize=letter)
                for image_path in self.selected_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        pdf_canvas.setPageSize((width, height))  # Set the PDF page size same as image size
                        pdf_canvas.drawImage(image_path, 0, 0, width, height)  # Place image on PDF
                        pdf_canvas.showPage()  # End current page
                pdf_canvas.save()
                print("PDF saved successfully.")
                # self.clear_displayed_images()
                # self.captured_images.clear()
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

    # def closeEvent(self, event):
    #     # Perform actions after closing the window
    #     print("Window closed")
    #     # For example, you can save some data or perform cleanup operations here
    #     super(MainWindow, self).closeEvent(event)
    # def open_camWindow(self):
    #     if not self.cam_thread or not self.cam_thread.isRunning():
    #         self.cam_thread.started.connect(self.cam_window.show)
    #         self.cam_thread.start()

    def toggle_child_window(self):
        # Toggle visibility of child window
        self.child_window.show()

    def closeEvent(self, event):
        # Ensure the child thread is stopped when closing the main window
        if self.child_thread.isRunning():
            self.child_thread.quit()
            self.child_thread.wait()
        event.accept()

    def display_captured_images_main(self):
        # print(image_list)
        # # Clear existing images
        # layout = self.ui.display_image_frame.layout()
        # if layout is not None:
        #     for i in reversed(range(layout.count())):
        #         layout.itemAt(i).widget().setParent(None)

        # # Ensure that show_label has a layout
        # if layout is None:
        #     layout = QVBoxLayout()
        #     self.ui.display_image_frame.setLayout(layout)

        # # Display captured images if the list is not empty
        # if image_list:
        #     # Create a scroll area
        #     scroll_area = QScrollArea()
        #     scroll_area.setWidgetResizable(True)
        #     scroll_content = QWidget()
        #     scroll_layout = QVBoxLayout(scroll_content) #QVBoxLayout(scroll_content)
        #     scroll_area.setWidget(scroll_content)

        #     # Display captured images
        #     for index, image_path in enumerate(image_list):
        #         label = QLabel()
        #         pixmap = QPixmap(image_path)
        #         pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
        #         pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
        #         label.setPixmap(pixmap)
        #         scroll_layout.addWidget(label)

        #     # Add the scroll area to the main layout
        #     layout.addWidget(scroll_area)
        # ---------------------------------------------

        # print(image_list)
        # # Clear existing images
        # layout = self.ui.display_image_frame.layout()
        # if layout is not None:
        #     for i in reversed(range(layout.count())):
        #         layout.itemAt(i).widget().setParent(None)

        # # Ensure that display_image_frame has a layout
        # if layout is None:
        #     layout = QVBoxLayout()
        #     self.ui.display_image_frame.setLayout(layout)

        # # Display captured images if the list is not empty
        # if image_list:
        #     # Display captured images
        #     for index, image_path in enumerate(image_list):
        #         # Create a custom widget to display image, timestamp, and checkbox
        #         image_widget = QWidget()
        #         image_layout = QVBoxLayout(image_widget)

        #         label = QLabel()
        #         pixmap = QPixmap(image_path)
        #         pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
        #         pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
        #         label.setPixmap(pixmap)

        #         # Add timestamp label
        #         timestamp_label = QLabel()
        #         now = datetime.now()
        #         timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        #         timestamp_label.setText(timestamp)

        #         # Add checkbox
        #         checkbox = QCheckBox("Select")

        #         # Add widgets to the layout
        #         image_layout.addWidget(label)
        #         image_layout.addWidget(timestamp_label)
        #         image_layout.addWidget(checkbox)

        #         # Add the custom widget to the main layout
        #         layout.addWidget(image_widget)
        #----------------------------------------------------

        print(image_list)
        # Clear existing images
        layout = self.ui.display_image_frame.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Ensure that display_image_frame has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.display_image_frame.setLayout(layout)

        # Display captured images if the list is not empty
        if image_list:
            # Create a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # Create a widget to contain the layout
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)

            # Create a "Select All" checkbox
            select_all_checkbox = QCheckBox("Select All")
            select_all_checkbox.stateChanged.connect(self.select_all_images)
            scroll_layout.addWidget(select_all_checkbox)

            # Display captured images
            for index, image_path in enumerate(image_list):
                # Create a custom widget to display image, timestamp, and checkbox
                image_widget = QWidget()
                image_layout = QVBoxLayout(image_widget)

                label = QLabel()
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
                pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
                label.setPixmap(pixmap)

                # Add timestamp label
                timestamp_label = QLabel()
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                timestamp_label.setText(timestamp)

                # Add checkbox
                checkbox = QCheckBox("Select")
                checkbox.stateChanged.connect(lambda state, index=index: self.update_selected_images(state, index))
                

                # Add widgets to the layout
                image_layout.addWidget(label)
                image_layout.addWidget(timestamp_label)
                image_layout.addWidget(checkbox)

                # Add the custom widget to the scroll layout
                scroll_layout.addWidget(image_widget)

                # Store a reference to the checkbox
                self.all_checkboxes.append(checkbox)

                # Store a reference to the label corresponding to the image path
                

                # Connect the click event of each image to the image_clicked method
                label.mousePressEvent = lambda event, index=index: self.image_clicked(label,index)
                
                # layout.addWidget(label)

            # Set the scroll content widget
            scroll_area.setWidget(scroll_content)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)

    def image_clicked(self, label,index):
        # Get the image path corresponding to the clicked label
        # image_path = self.image_labels.get(label)
        
        # Load the clicked image into the show_image label
        self.image_labels[label] = image_list[index]
        pixmap = QPixmap(image_list[index])
        pixmap = pixmap.scaled(391, 541, Qt.KeepAspectRatio)
        self.ui.show_image.setPixmap(pixmap)



    def update_selected_images(self, state, index):
        if state == Qt.Checked:
            image_path = image_list[index]
            if image_path not in self.selected_images:
                self.selected_images.append(image_path)
        else:
            image_path = image_list[index]
            if image_path in self.selected_images:
                self.selected_images.remove(image_path)

    def select_all_images(self, state):
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

            if state == Qt.Checked:
                image_path = image_list[self.all_checkboxes.index(checkbox)]
                if image_path not in self.selected_images:
                    self.selected_images.append(image_path)
            else:
                image_path = image_list[self.all_checkboxes.index(checkbox)]
                if image_path in self.selected_images:
                    self.selected_images.remove(image_path)

    def get_selected_images(self):
        return self.selected_images
            





    

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
