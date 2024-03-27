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
from fpdf import FPDF
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

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
      
        self.captured_images=[]

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.cam_btn_2.setChecked(True)
        
        
        # self.video_stream = VideoStream(self.ui.label)  # Pass the label to display camera feed
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.video_stream.display_camera_feed)
        # self.timer.start(50)  # Update camera feed every 50 milliseconds
        

        self.current_camera_index = 0  # Index of the currently selected camera
        self.video_stream = VideoStream(self.ui.label,self.current_camera_index)  # Initialize video stream with default camera
        
        self.populate_camera_dropdown()  # Populate the dropdown menu with available cameras
        # self.ui.dropdown_menu.currentIndexChanged.connect(self.cam.switch_camera)  # Connect dropdown change event to switch_camera method

        

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None



        self.ui.capture.clicked.connect(self.capture_image)  # Connect capture button to capture_image method
        
        ### to add functionality to make pdf
        self.ui.show.clicked.connect(self.make_pdf)


    ## Function for searching
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                   + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_dashborad_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        # camera_window = VideoStream()  # Instantiate the main window class
        # camera_window.show()

    def on_dashborad_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_orders_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_orders_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_products_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_products_btn_2_toggled(self, ):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_customers_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def on_customers_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)


    


    def capture_image(self):
        ret, frame = self.video_stream.video.read()
        
        if ret:
            # Define the cropping geometry
            crop_x = 987
            crop_y = 448
            crop_width = 1828
            crop_height = 1333
            
            # Ensure that the cropping rectangle does not exceed the dimensions of the frame
            max_width = frame.shape[1]
            max_height = frame.shape[0]
            
            crop_x = min(crop_x, max_width)
            crop_y = min(crop_y, max_height)
            crop_width = min(crop_width, max_width - crop_x)
            crop_height = min(crop_height, max_height - crop_y)
            
            # Crop the frame
            cropped_frame = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]
            
            if not cropped_frame.size == 0:  # Check if the cropped frame is not empty
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
                filename = f"captured_image_{timestamp}.jpg"
                
                
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()

                # Specify the filepath within the temporary directory
                filepath = os.path.join(temp_dir, filename)

                try:
                    cv2.imwrite(filepath, cropped_frame)  # Save the cropped image with timestamp
                    print("Image saved successfully.")

                    # Append the filepath to the captured images list
                    self.captured_images.append(filepath)

                    # Call display_captured_images to update the display
                    self.display_captured_images()

                except Exception as e:
                    print(f"Error saving image: {e}")


    


    def display_captured_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.page_layout.count())):
            self.ui.page_layout.itemAt(i).widget().setParent(None)

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
        self.ui.page_layout.addWidget(scroll_area)


    def clear_displayed_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.page_layout.count())):
            self.ui.page_layout.itemAt(i).widget().setParent(None)

    def open_context_menu(self, point, index, label):
        menu = QMenu()
        crop_action = menu.addAction("Crop")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(label.mapToGlobal(point))
        if action == crop_action:
            self.crop_image(index)
        elif action == delete_action:
            self.delete_image(index)

    def image_clicked(self, index):
        print("Clicked on image:", index)

    def crop_image(self, index):
        image_path = self.captured_images[index]
        img = cv2.imread(image_path)
        if img is not None:
            crop_rect = cv2.selectROI("Select ROI", img, fromCenter=False, showCrosshair=True)
            if crop_rect[2] > 0 and crop_rect[3] > 0:  # Check if a valid ROI was selected
                cropped_img = img[int(crop_rect[1]):int(crop_rect[1] + crop_rect[3]), int(crop_rect[0]):int(crop_rect[0] + crop_rect[2])]
                if cropped_img.size > 0:  # Check if cropped image is not empty
                    cv2.imwrite(image_path, cropped_img)
                    self.display_captured_images()
                else:
                    print("Failed to crop image. The selected region is empty.")
            else:
                print("No valid ROI selected. Crop operation canceled.")

    def delete_image(self, index):
        if index < len(self.captured_images):
            image_path = self.captured_images.pop(index)
            self.display_captured_images()  # Update displayed images
            # Also remove the file from disk if needed
            if os.path.exists(image_path):
                os.remove(image_path)



    
                

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
        self.ui.dropdown_menu.addItems(camera_names)
        self.ui.dropdown_menu.currentIndexChanged.connect(lambda index: self.switch_camera_async(index))

    # @staticmethod
    # def get_camera_serial_number(device_index):
    #     try:
    #         # Execute the v4l2-ctl command to get camera information
    #         output = subprocess.check_output(['v4l2-ctl', '-d', f'/dev/video{device_index}', '--all']).decode()
    #         # Extract the serial number from the output
    #         serial_number_line = [line for line in output.split('\n') if 'Serial' in line][0]
    #         serial_number = serial_number_line.split(':')[-1].strip()
    #         return serial_number
    #     except Exception as e:
    #         print(f"Error retrieving serial number for camera {device_index}: {e}")
    #         return None

   


    # def switch_camera(self, index):
    #     self.current_camera_index=index
    #     # if self.cap is not None:
    #     #     self.cap.release()
    #     # camera_index = self.available_cameras[index][0]  # Get the camera index from available cameras list
    #     # self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    #     # self.video_stream = VideoStream(self.ui.label, camera_index)  # Initialize video stream with selected camera
    #     # self.timer.timeout.connect(self.video_stream.display_camera_feed)  # Connect timer to display updated camera feed
    #     camera_index = self.available_cameras[index][self.current_camera_index]  # Get the camera index from available cameras list
    #     print(index)
        
        
    #     if self.cap is not None:
    #         # Release the existing capture and VideoStream instance
    #         # self.cap.release()
    #         del self.cap
    #         if self.video_stream is not None:
    #             self.video_stream.video.release()
            
    #     # Create a new VideoCapture instance
    #     self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        
    #     if not self.cap.isOpened():
    #         # If the new capture is not opened, log an error and return
    #         print(f"Error: Unable to open camera {camera_index}")
    #         return
        
    #     # Create a new VideoStream instance with the selected camera index
    #     self.video_stream = VideoStream(self.ui.label, camera_index)
    #     self.timer.timeout.connect(self.video_stream.display_camera_feed)  # Connect timer to display updated camera feed
        
    def switch_camera_async(self, index):
        self.current_camera_index = index
        cap = self.cap
        video_stream = self.video_stream
        if cap is not None:
            cap.release()
            if video_stream is not None:
                video_stream.video.release()

        camera_index = available_cameras[index][self.current_camera_index]
        self.video_stream.change_camera(camera_index)
        # camera_thread = QThread()
        # camera_thread.start()
        # self.start_camera(camera_index, camera_thread)

    def switch_camera(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Error: Unable to open camera {camera_index}")
            return

        self.video_stream = VideoStream(self.ui.label, camera_index)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(1000 // 30)  # Adjust the frame rate as needed   

    def update_camera_feed(self):
        cap = self.cap
        video_stream = self.video_stream
        if cap is not None:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.parent_label.setPixmap(pixmap.scaled(self.parent_label.size(), Qt.KeepAspectRatio))


    def start_camera(self,camera_index,  camera_thread): 
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print(f"Error: Unable to open camera {camera_index}")
            return

        video_stream = VideoStream(self.ui.label, camera_index)
        self.timer = QTimer()  # Timer for periodic updates
        self.timer.timeout.connect(lambda: self.update_camera_feed(self))
        self.timer.moveToThread(camera_thread)  # Move the timer to the camera thread
        self.timer.start(1000 // 30)  # Start the timer for periodic updates
        self.cap = cap
        self.video_stream = video_stream


    def stop_camera(self):
        timer = self.timer
        cap = self.cap
        video_stream = self.video_stream
        if timer is not None:
            timer.stop()
        if cap is not None:
            cap.release()
        if video_stream is not None:
            video_stream.video.release()



    # def closeEvent(self, event):
    #     if self.cap is not None:
    #         # self.cap.release()
    #         del self.cap
    #     event.accept()





if __name__ == "__main__":
    app = QApplication(sys.argv)

    ## loading style file
    # with open("style.qss", "r") as style_file:
    #     style_str = style_file.read()
    # app.setStyleSheet(style_str)

    ## loading style file, Example 2
    # style_file = QFile("Style.css")
    # style_file.open(QFile.ReadOnly | QFile.Text)
    # style_stream = QTextStream(style_file)
    # app.setStyleSheet(style_stream.readAll())

    
    

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

    # app = QApplication(sys.argv)

    # window = MainWindow()  # Creating an instance of MainWindow from camera1.py
    # window.ui.stackedWidget.setCurrentIndex(5)  # Set the camera tab as the default
    # window.show()

    # sys.exit(app.exec())