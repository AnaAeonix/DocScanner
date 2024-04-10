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
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QInputDialog,QComboBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
import keyboard

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
        
        self.ui.contrast_btn.clicked.connect(self.adjust_contrast)
        self.ui.sharp_btn.clicked.connect(self.adjust_sharpness)
        
        
        
        # self.ui.color_btn.clicked.connect(self.adjust_color_mode)
        self.ui.rotateleft_btn.clicked.connect(self.rotate_image_left)
        self.ui.rotaterigth_btn.clicked.connect(self.rotate_image_right)
        self.ui.undo_btn.clicked.connect(self.undo)
        self.ui.bnw_btn.clicked.connect(self.blackAndWhite)
        self.ui.gray_btn.clicked.connect(self.grayscale)
        self.ui.enhance_btn.clicked.connect(self.AutoEnhance)
        self.ui.save_btn.clicked.connect(self.save)
        # self.ui.crop_btn.clicked.connect(self.clicked_crop_btn)
        self.ui.scan_btn.clicked.connect(self.toggle_child_window)
        self.ui.delete_btn.clicked.connect(self.delete_image)
        self.child_window = ChildWindow()     
        # self.captured_imagesParent=[]
        # Thread to start the child window
        self.child_thread = QThread()
        self.child_window.moveToThread(self.child_thread)
        self.child_thread.started.connect(self.child_window.hide)
        self.child_thread.start()
        

        self.latestImage = []
        
        self.child_window.windowClosed.connect(self.display_captured_images_main)

        # Create a dictionary to store references to labels corresponding to image paths
        self.image_labels = {}
        self.image = None  # Track the currently displayed image
        self.imageIndex = None
        self.rotation_state = 0  # Initial rotation state
        self.current_displayed_image = None  # Track the currently displayed image

        self.selected_images = []  # Store selected images
        self.all_checkboxes = []   # Store references to all checkboxes
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(screen_geometry)


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
        print(image_list)
        # Clear existing images
        layout = self.ui.display_image_frame.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Clear the list of checkboxes
        self.all_checkboxes = []

        # Ensure that display_image_frame has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.display_image_frame.setLayout(layout)

        # Display captured images if the list is not empty
        if image_list:
            # Check which images are already displayed
            displayed_images = [layout.itemAt(i).widget().findChild(QLabel) for i in range(layout.count())]

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

            # Display captured images that are not already displayed
            for index, image_path in enumerate(image_list):
                if image_path not in displayed_images:
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
                    image_layout.addWidget(checkbox)

                    self.all_checkboxes.append(checkbox)

                    # Add widgets to the layout
                    image_layout.addWidget(label)
                    image_layout.addWidget(timestamp_label)

                    # Add the custom widget to the scroll layout
                    scroll_layout.addWidget(image_widget)

                    # Store a reference to the label corresponding to the image path
                    displayed_images.append(image_path)

                    # Connect the click event of each image to the image_clicked method
                    label.mousePressEvent = lambda event, index=index: self.image_clicked(label, index)

            # Set the scroll content widget
            scroll_area.setWidget(scroll_content)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)



    def image_clicked(self, label,index):
        # Get the image path corresponding to the clicked label
        # image_path = self.image_labels.get(label)
        
        # Load the clicked image into the show_image label
        self.image_labels[label] = image_list[index]
        self.image = image_list[index]
        self.imageIndex = index
        self.latestImage.append(self.read())
        self.load_image()
        
    def revert_image_clicked(self):
        if self.image is not None:
            # Remove the image path from self.image_labels
            self.image = None
            self.imageIndex = None
            

            # Remove the latest image from self.latestImage
            if self.latestImage:
                self.latestImage.pop()

            # Reload the previously displayed image if available
            if self.latestImage:
                self.load_image()

        
    def open_context_menu(self, point, index, label):
        menu = QMenu()
        crop_action = menu.addAction("Crop")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(label.mapToGlobal(point))
        if action == crop_action:
            self.crop_image(index)
        elif action == delete_action:
            self.delete_image(index)
    def load_image(self):
        pixmap = QPixmap(self.image)
        pixmap = pixmap.scaled(391, 541, Qt.KeepAspectRatio)

        # Set alignment to center
        self.ui.show_image.setAlignment(Qt.AlignCenter)
        self.ui.show_image.setPixmap(pixmap)

        
    def delete_image(self):
        global image_list
        image_list = [elem for elem in image_list if elem not in self.selected_images]
        self.revert_image_clicked()
        self.child_window.windowClosed.emit()
    
    def adjust_contrast(self):

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))
            
            # Apply contrast enhancement
            contrast_value = 1.5
            contrast_enhancer = ImageEnhance.Contrast(pil_image)
            enhanced_image = contrast_enhancer.enhance(contrast_value)
            
            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
            
            # Display the enhanced image
            self.latestImage.append(enhanced_image_np)
            # self.image = enhanced_image_np
            self.write(enhanced_image_np)
            self.load_image()

    def write(self,imagee):
        cv2.imwrite(self.image, imagee)
    def read(self):
       return cv2.imread(self.image)

    def undo(self):
        if len(self.latestImage)>1:
            self.latestImage.pop()
            self.write(self.latestImage[-1])
            self.load_image()
    def save(self):
        global image_list
        if self.imageIndex is not None:
            image_list[self.imageIndex] = self.image
            self.child_window.windowClosed.emit()
        
    def adjust_sharpness(self):

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))
            
            # Apply sharpness enhancement
            sharpness_value = 2.0
            sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
            enhanced_image = sharpness_enhancer.enhance(sharpness_value)
            
            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
            
            # Display the enhanced image
            self.latestImage.append(enhanced_image_np)
            # self.image = enhanced_image_np
            self.write(enhanced_image_np)
            self.load_image()

    def AutoEnhance(self):
        pil_image = Image.fromarray(cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))
                
            # Apply color enhancement
        enhanced_image = ImageEnhance.Color(pil_image).enhance(1.5)
                
            # Convert the enhanced image back to a NumPy array
        enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
                
        # Display the enhanced image
        self.latestImage.append(enhanced_image_np)
        # self.image = enhanced_image_np
        self.write(enhanced_image_np)
        self.load_image()
        
    def blackAndWhite(self):
        bw_image = cv2.cvtColor(self.read(), cv2.COLOR_BGR2GRAY)
        self.latestImage.append(bw_image)
        # self.image = bw_image
        self.write(bw_image)
        self.load_image()
    
    def grayscale(self):
                grayscale_image = cv2.cvtColor(self.read(), cv2.COLOR_BGR2GRAY)
                self.latestImage.append(grayscale_image)
                # self.image = grayscale_image
                self.write(grayscale_image)
                self.load_image()
    # def adjust_color_mode(self):
    #     if self.image is not None:
    #         choice = self.color_mode_combo.currentText()
                
    #         elif choice == "Black and White":
    #             bw_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    #             self.latestImage.append(bw_image)
    #             self.image = bw_image
    #             self.load_image()
    #         elif choice == "Grayscale":
    #             grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    #             self.latestImage.append(grayscale_image)
    #             self.image = grayscale_image
    #             self.load_image()
    #         elif choice == "No Filters":
    #             self.load_image()
                



                
    def rotate_image_left(self):
        if self.read() is not None:
            if self.rotation_state == 270:
                self.rotation_state = 0
            else:
                self.rotation_state += 90
            rotated_image = self.read().copy()
            for _ in range(self.rotation_state // 90):
                rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()


    def rotate_image_right(self):
        if self.read() is not None:
            self.rotation_state -= 90
            if self.rotation_state < 0:
                self.rotation_state = 270
            rotated_image = self.read().copy()
            for _ in range(abs(self.rotation_state // 90)):
                rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()



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
