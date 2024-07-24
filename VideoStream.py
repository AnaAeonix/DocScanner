import cv2
import threading
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
import numpy as np


class VideoStream:
    def __init__(self, parent_label: QLabel, camera_index):
        self.video = cv2.VideoCapture()

        self.points = None
        self.firstTime = True
        self.parent_label = parent_label
        self.set_resolution()
        self.timer = None
        self.camera_change_thread = None  # Thread for camera switching
        self.scan_document = False
        self.checked = False
        self.ai_crop = None
        self.current_focus = 0
        self.brightness = 0
        self.contrast = 0
        self.exposure = -5
        self.left = False
        self.right = False
        self.rotation_state = 0
        self.available_cameras = []

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
        
    def update_display(self):
        self.video.set(cv2.CAP_PROP_BRIGHTNESS, self.brightness)
        self.video.set(cv2.CAP_PROP_CONTRAST, self.contrast)
        self.video.set(cv2.CAP_PROP_EXPOSURE, float(self.exposure))



    def display_camera_feed1(self, checked):
        self.checked = checked
        if not self.video.isOpened():
                # Display error message if camera not open
                font = QFont()
                font.setPointSize(30)
                self.parent_label.setFont(font)
                if self.firstTime:
                    self.parent_label.setText(
                        "<p style='font-size:20pt'>Please Select the Camera...</p>")
                else:
                    self.parent_label.setText(
                        "<p style='font-size:20pt'>Changing Camera...</p>")
                return

        ret, frame = self.video.read()

        if ret:
                self.firstTime = False

                if self.points is not None and self.checked == False:
                    cv2.polylines(
                        frame, [np.array(self.points)], True, (0, 255, 0), 6)

                # Check if contour detection is enabled
                if self.checked:
                    # self.points = None
                    document_contour = self.detect_document(frame)

                    if document_contour is not None:
                        # Calculate the area of the detected contour         
                        area = cv2.contourArea(document_contour)

                        # Update the biggest contour if the detected one is larger
                        biggest_contour = document_contour
                        # Draw the biggest contour on the frame
                        cv2.drawContours(
                            frame, [biggest_contour], -1, (0, 255, 0), 6)
                        p = self.order_points(biggest_contour.reshape(4, 2))

                        self.ai_crop = p

                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(rgb_image, (3264, 2448))
                self.image = frame_resized

                if self.image is not None:
                    if self.right:
                        self.rotation_state = (self.rotation_state + 90) % 360
                        self.right = False  # Reset the flag after rotation

                    if self.left:
                        self.rotation_state = (self.rotation_state - 90) % 360
                        self.left = False  # Reset the flag after rotation

                    # Apply cumulative rotation based on rotation_state
                    if self.rotation_state == 90:
                        self.image = cv2.rotate(
                            self.image, cv2.ROTATE_90_CLOCKWISE)
                    elif self.rotation_state == 180:
                        self.image = cv2.rotate(self.image, cv2.ROTATE_180)
                    elif self.rotation_state == 270:
                        self.image = cv2.rotate(
                            self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)

                h, w, ch = self.image.shape
                bytes_per_line = 3 * w
                q_img = QImage(self.image.data, w, h,
                            bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.parent_label.setPixmap(pixmap.scaled(
                    self.parent_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.parent_label.setAlignment(Qt.AlignCenter)
        else:
                # Display loader while camera is changing
                self.show_loader()

    def change_camera(self, camera_index):
        # Stop the timer if it's running
        if self.timer is not None:
            self.timer.stop()
        # Extract the actual camera index from available_cameras based on dropdown selection
        selected_index, _ = self.available_cameras[camera_index]
        # Create a thread for camera switching (optional, but recommended for responsiveness)
        self.camera_change_thread = threading.Thread(
            target=self._change_camera_in_thread, args=(camera_index,))
        self.camera_change_thread.start()
        # Display loader immediately
        self.show_loader()

    def _change_camera_in_thread(self, camera_index):
        # Release the current video capture
        if self.video.isOpened():
            self.video.release()


        # Open the new camera capture
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.set_resolution()

        # Create a QTimer object and connect it to the display_camera_feed function (in main thread)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_camera_feed1)
        self.timer.start(10)  # Start the timer with a 10ms interval

    def show_loader(self):
        font = QFont()
        font.setPointSize(30)
        self.parent_label.setFont(font)
        self.parent_label.setAlignment(Qt.AlignCenter)
        self.parent_label.setText(
            "<p style='font-size:20pt'>Changing Camera...</p>")

    def l_inter(self, line1, line2):
        r1, t1 = line1
        r2, t2 = line2
        A = np.array([[np.cos(t1), np.sin(t1)], [np.cos(t2), np.sin(t2)]])
        b = np.array([r1, r2])
        if abs(t1 - t2) > 1.3:
            return np.round(np.linalg.solve(A, b)).astype(int)
        return None

    def points_inter(self, lines):
        intersections = []
        for i, g in enumerate(lines[:-1]):
            for g2 in lines[i+1:]:
                inter_pt = self.l_inter(g, g2)
                if inter_pt is not None:
                    intersections.append(inter_pt)
        return intersections

    def update_frame(self):
        self.display_camera_feed1(self.checked)


    def set_focus(self, index):
        # Simulate changing focus
        self.current_focus = (self.current_focus + 10) % 30
        print(f'Focus set to: {self.current_focus}')
        if index == 1:
            if self.current_focus >= 0 and self.current_focus < 20:
                self.video.set(cv2.CAP_PROP_FOCUS, self.current_focus)

        if index == 0:
            if self.current_focus == 20:
                self.video.set(cv2.CAP_PROP_AUTOFOCUS, 1)


    def detect_document(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, gray = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        gray = cv2.GaussianBlur(gray, (1, 1), 0)
        edged = cv2.Canny(gray, 75, 200)
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edged = cv2.dilate(edged, kernel, iterations=1)
        edged = cv2.erode(edged, kernel, iterations=1)
        contours, _ = cv2.findContours(
            edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx

        return None
    
    
    def order_points(self,pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        print("i")
        print(rect)
        return rect
