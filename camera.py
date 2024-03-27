import cv2
import threading
from functools import partial
from PyQt5.QtCore import QTimer,  Qt
from Sidebar1 import VideoStream, Ui_MainWindow



class CameraManager:
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.available_cameras = []
        self.cap = None
        self.video_stream = None
        self.current_camera_index = None
        self.timer = QTimer()  # Assuming you are using QTimer for periodic updates

        
        
    def populate_camera_dropdown(self):
        self.available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use cv2.CAP_DSHOW for better compatibility
            if cap.isOpened():
                backend_id = cap.get(cv2.CAP_PROP_BACKEND)
                camera_name = f"Camera {i} - Backend: {backend_id}"
                self.available_cameras.append((i, camera_name))
                del cap
        camera_names = [camera_name for _, camera_name in self.available_cameras]
        # self.ui.dropdown_menu.addItems(camera_names)
        self.ui.dropdown_menu.addItems(camera_names)
        self.ui.dropdown_menu.currentIndexChanged.connect(self.switch_camera_async)
        
    def switch_camera_async(self, index):
        self.current_camera_index = index
        if self.cap is not None:
            self.cap.release()
            if self.video_stream is not None:
                self.video_stream.video.release()

        camera_index = self.available_cameras[index][0]
        thread = threading.Thread(target=partial(self.switch_camera, camera_index))
        thread.start()

    def switch_camera(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Error: Unable to open camera {camera_index}")
            return

        self.video_stream = VideoStream(self.ui.label, camera_index)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(1000 // 30)  # Adjust the frame rate as needed

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
        if self.video_stream is not None:
            self.video_stream.video.release()
