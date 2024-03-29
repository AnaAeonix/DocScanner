import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Feed")
        self.setGeometry(100, 100, 640, 480)

        self.camera_label = QLabel(self)
        self.camera_label.resize(640, 480)

        self.capture_button = QPushButton("Capture", self)
        self.capture_button.clicked.connect(self.capture_image)

        self.camera_combobox = QComboBox(self)
        self.populate_camera_combobox()
        self.camera_combobox.currentIndexChanged.connect(self.change_camera)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.camera_label)
        self.layout.addWidget(self.capture_button)
        self.layout.addWidget(self.camera_combobox)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

        self.setLayout(self.layout)

        self.cap = None

    # def populate_camera_combobox(self): 
    #     self.available_cameras = []
    #     for i in range(10):
    #         cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use cv2.CAP_DSHOW for better compatibility
    #         if cap.isOpened():
    #             camera_name = f"Camera {i}"
    #             self.available_cameras.append((i, camera_name))
    #             cap.release()
    #     self.camera_combobox.addItems([f"{camera_name}" for _, camera_name in self.available_cameras])

    def populate_camera_combobox(self):
        self.available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use cv2.CAP_DSHOW for better compatibility
            if cap.isOpened():
                backend_id = cap.get(cv2.CAP_PROP_BACKEND)
                camera_name = f"Camera {i} - Backend: {backend_id}"
                self.available_cameras.append((i, camera_name))
                cap.release()
        self.camera_combobox.addItems([f"{camera_name}" for _, camera_name in self.available_cameras])


    def change_camera(self):
        if self.cap is not None:
            self.cap.release()
        camera_index = self.available_cameras[self.camera_combobox.currentIndex()][0]
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # if width == 3840 and height == 2160:
        print(width)
        print(height)
        # else:
        #     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #     print("Using 1080p resolution")
    #     self.set_fps(30)  # Set FPS to 60

    # def set_fps(self, fps):
    #     if self.cap is not None and self.cap.isOpened():
    #         self.cap.set(cv2.CAP_PROP_FPS, fps)
    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame, (640, 480))
                h, w, ch = frame_resized.shape
                bytes_per_line = ch * w
                q_image = QImage(frame_resized.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.camera_label.setPixmap(QPixmap.fromImage(q_image))

    def capture_image(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite("captured_image.jpg", frame)
                print("Image captured successfully!")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    camera_app = CameraApp()
    camera_app.show()
    sys.exit(app.exec_())
