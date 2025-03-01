from PyQt5 import QtWidgets

from .Home.camera import CameraWidget
from .Home.camera_thread import CameraThread

class LiveViewWidget(QtWidgets.QWidget):
    """A custom widget for live camera view with object detection capabilities.

    The widget provides a camera view and options to enable/disable the camera, select an object detection model,
    and change the model.

    Attributes:
        camera_is_on (bool): Flag indicating whether the camera is currently enabled.
        enable_camera_button (QtWidgets.QPushButton): Button to enable/disable the camera.
        combo1 (QtWidgets.QComboBox): Combo box to select the object detection model.
        camera_widget (CameraWidget): Widget to display the camera view.
        camera_thread (CameraThread): Thread for processing camera frames.
    """

    def __init__(self) -> None:
        super(LiveViewWidget, self).__init__()

        self.camera_is_on = False

        # Set the font size for the widget
        self.setStyleSheet("font-size: 12px;")
        # Set the size policy to expanding
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


        # Create the layout for the widget
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create the first row containing labels and combo boxes
        row1 = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel('Object Detection MODEl', self)
        self.combo1 = QtWidgets.QComboBox(self)
        
        
        row1.addWidget(label1)
        row1.addWidget(self.combo1)
        
        submit_button = QtWidgets.QPushButton('Change Model', self)
        row1.addStretch()
        row1.addWidget(submit_button)

        ### Camera Enable 
        self.enable_camera_button = QtWidgets.QPushButton('ON', self)
        self.enable_camera_button.setCheckable(True)

        row1.addWidget(self.enable_camera_button)

        # Add the rows to the layout
        layout.addLayout(row1)


        # Create the second row containing Plot
        row2 = QtWidgets.QHBoxLayout()
        
        self.camera_widget = CameraWidget()

        self.camera_thread = CameraThread()

        self.camera_thread.image_signal.connect(self.on_new_frame)
      
        row2.addWidget(self.camera_widget)

        layout.addLayout(row2)


        # Connect the button to the callback function
        submit_button.clicked.connect(self.submit)
        self.enable_camera_button.clicked.connect(self.start_camera_thread)

    def start_camera_thread(self, checked):

        if checked:
            self.enable_camera_button.setText('Off')
            self.camera_thread.start()
            self.camera_is_on = True 
        else:
            self.enable_camera_button.setText('On')
            self.camera_thread.stop()
            self.camera_is_on = False
        

    def submit(self):
        """Callback function for the submit button.

        Placeholder method for handling the event when the submit button is clicked.
        Implement the desired functionality to change the object detection model.
        """
        pass 

    def resizeEvent(self, event):
        # Resize the camera widget when the main window is resized
        super().resizeEvent(event)
        self.camera_widget.setMinimumSize(1, 1)

    def closeEvent(self, event):
        """Stop the camera thread when the widget is closed.

        Args:
            event (QtGui.QCloseEvent): The close event.
        """
        self.camera_thread.stop()
        event.accept()

    def on_new_frame(self, frame):
        self.camera_widget.set_image(frame)
    
    