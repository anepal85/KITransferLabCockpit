
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from .LabelStudio.label_studio_interface import LabelStudioInterfaceWidget


class AnnotationWidget(QtWidgets.QWidget):

    """
        Widget for label-studio annotation.

        This widget provides an interface for label-studio annotation within the application.
        It includes a title, a label-studio interface widget, and a layout to organize the components.

        The main functionality includes:
        - Setting the font size for the widget.
        - Creating a vertical layout to hold the components.
        - Adding a title label with a specified font size and alignment.
        - Creating an instance of the LabelStudioInterfaceWidget, which handles the label-studio interface.
        - Setting the layout for the widget.

        """

    def __init__(self) -> None:
        super(AnnotationWidget, self).__init__()

        # Set the font size for the widget
        self.setStyleSheet("font-size: 12px;")
        
        # Create the layout for the widget
        self.layout = QtWidgets.QVBoxLayout(self)

        self.title_annotation = QtWidgets.QLabel()
        self.title_annotation.setText("Label-Studio Annotation")
        self.title_annotation.setStyleSheet("font-size: 18px;")
        self.title_annotation.setAlignment(Qt.AlignCenter)
        self.title_annotation.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.title_annotation.setMinimumHeight(30)

        self.layout.addWidget(self.title_annotation)

        #Title for label-studio annotation 
        self.firstrowlayoutWidget = LabelStudioInterfaceWidget()
        self.layout.addWidget(self.firstrowlayoutWidget)
        self.setLayout(self.layout)

        




