from PyQt5 import QtWidgets 
class CncWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super(CncWidget, self).__init__()

        # Set the font size for the widget
        self.setStyleSheet("font-size: 20px;")

        # Create the layout for the widget
        layout = QtWidgets.QVBoxLayout(self)
        
        self.label = QtWidgets.QTextEdit('CNC Input', self)

        layout.addWidget(self.label)