from PyQt5 import QtWidgets 
from Pages.visualization import VisualizationWidget
from Pages.live_view import LiveViewWidget
from Pages.metrcis import MetricsWidget
from Pages.cnc_input import CncWidget

class HomeWidget(QtWidgets.QWidget):
    """A custom widget for the home screen.

    The widget consists of visualization, live view, CNC input, and metrics widgets.

    Attributes:
        second_row_layout (QtWidgets.QHBoxLayout): Layout for the second row of widgets.
    """

    def __init__(self) -> None:
        super(HomeWidget, self).__init__()

        # Set the font size for the widget
        self.setStyleSheet("font-size: 12px;")

        main_layout = QtWidgets.QVBoxLayout(self)

        firs_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()

        firs_row_layout.addWidget(VisualizationWidget())
        firs_row_layout.addWidget(LiveViewWidget())

        self.second_row_layout.addWidget(CncWidget())
        self.second_row_layout.addWidget(MetricsWidget())
        

        main_layout.addLayout(firs_row_layout)
        main_layout.addLayout(self.second_row_layout)
        
        


        

        
