import cv2
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QLabel, QVBoxLayout
 

class CameraWidget(QLabel):
    """
        Widget for displaying camera frames.

        This class extends QLabel and provides a widget for displaying camera frames. It automatically scales and
        updates the displayed image when set_image method is called.

        """
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1, 1)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('background-color: black')
        self.frame = None

    def set_image(self, image):
        """
        Set the camera frame image to be displayed.

        :param image: The camera frame image (numpy array).
        :return: None
        """
        self.frame = image
        self.update()

    def paintEvent(self, event):
        """
        Handle the paint event to display the camera frame.

        :param event: Paint event
        :return: None
        """
        if self.frame is not None:
            # Scale the image to fit the label
            qimage = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qimage).scaled(self.width(), self.height(), Qt.KeepAspectRatio)
            self.setPixmap(pixmap)
        super().paintEvent(event)


