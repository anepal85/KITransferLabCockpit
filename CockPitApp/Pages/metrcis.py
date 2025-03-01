from PyQt5 import QtWidgets 
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MetricsWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super(MetricsWidget, self).__init__()

        # Set the font size for the widget
        self.setStyleSheet("font-size: 20px;")

        # Create the layout for the widget
        layout = QtWidgets.QVBoxLayout(self)
        
        self.label = QtWidgets.QLabel('Selected KI Model Metric', self)

        

        layout.addWidget(self.label)