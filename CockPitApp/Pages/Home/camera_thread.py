import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    """
    Thread class for capturing frames from a camera.

    This class extends the QThread class to create a separate thread for capturing frames from a camera.
    It continuously reads frames from the camera and emits them as signals. It also provides a method to stop
    the thread and release the camera capture object.

    Signals:
    - image_signal: emitted when a new frame is captured, sending the frame as a numpy array.

    """
    image_signal = pyqtSignal(np.ndarray)
    
    def __init__(self, parent=None):
        """
        Initialize the CameraThread object.

        :param parent: Parent QObject (default: None)
        """
        super().__init__(parent)
        
        self._is_running = False
        
    def run(self):
        self._is_running = True
        
        # Open the camera capture object
        capture = cv2.VideoCapture(0)
        #capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Continuously read frames from the camera and emit them as signals
        while self._is_running:
            ret, frame = capture.read()
            if ret:
                self.image_signal.emit(frame)
        
        # Release the camera capture object
        capture.release()
    
    def stop(self):
        self._is_running = False
        self.wait()