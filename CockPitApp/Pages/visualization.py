from PyQt5 import QtWidgets 
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Pages.figure_canvas import MyFigureCanvas
from datetime import timedelta 
from .utils.get_data_from_json import get_json_as_list

        

class VisualizationWidget(QtWidgets.QWidget):

    def __init__(self) -> None:
        super(VisualizationWidget, self).__init__()

        # Set the font size for the widget
        self.setStyleSheet("font-size: 12px;")
        # Set the size policy to expanding
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


        # Create the layout for the widget
        self.layout = QtWidgets.QVBoxLayout(self)
        
        ### Here comes the default Data for figure 
        self.measurements_list = get_json_as_list()

        # Create the first row containing labels and combo boxes
        row1 = QtWidgets.QHBoxLayout()
        label1 = QtWidgets.QLabel('Velocity', self)
        
        self.combo1 = QtWidgets.QComboBox(self)
        self.velocity_label = ["Gx", "Gy", "Gz"]
        self.combo1.addItems(self.velocity_label)

        label2 = QtWidgets.QLabel('Temperature', self)
        self.combo2 = QtWidgets.QComboBox(self)
        self.temperature = ['None', 'temp_ambient','temp_tool']
        self.combo2.addItems(self.temperature)

        label3 = QtWidgets.QLabel('Current', self)
        self.combo3 = QtWidgets.QRadioButton(self)
        
        row1.addWidget(label1)
        row1.addWidget(self.combo1)
        row1.addWidget(label2)
        row1.addWidget(self.combo2)
        row1.addWidget(label3)
        row1.addWidget(self.combo3)

        submit_button = QtWidgets.QPushButton('Plot', self)
        row1.addStretch()
        row1.addWidget(submit_button)

        # Add the rows to the layout
        self.layout.addLayout(row1)


        # Create the second row containing Plot
        self.row2 = QtWidgets.QHBoxLayout()

        # self.data_ambient = [dictionary['temp_ambient'] for dictionary in self.measurements_list]
        # self.data_tool = [dictionary['temp_tool'] for dictionary in self.measurements_list]

        self.time_unformatted = [timedelta(seconds = dictionary['time']).seconds for dictionary in self.measurements_list]
        self.current = [dictionary['current'] for dictionary in self.measurements_list]
        self.velocity_x = [dictionary['Gx'] for dictionary in self.measurements_list]

        self.myFig = MyFigureCanvas(self.time_unformatted, [self.velocity_x, self.current], ['Gx','Current'])
        self.row2.addWidget(self.myFig)
        

        # Connect the button to the callback function
        submit_button.clicked.connect(self.submit)
        self.layout.addLayout(self.row2)




    def submit(self):
        
        self.row2.removeWidget(self.myFig)
        self.myFig.deleteLater()

        # Get the selected options from the combo boxes
        velocity = self.combo1.currentText()
        temp = self.combo2.currentText()
        current = self.combo3.isChecked()

        # Do something with the selected options, such as plotting the data
        print('Selected options:',velocity, current, temp)
        y_axis = [[dictionary[velocity] for dictionary in self.measurements_list]]
        y_label_name = [velocity] #, temp, current]

        if temp != "None":
            y_axis.append([dictionary[temp] for dictionary in self.measurements_list])
            y_label_name.append(temp)

        if current:
            y_axis.append([dictionary['current'] for dictionary in self.measurements_list])
            y_label_name.append('Current')
        
        self.myFig = MyFigureCanvas(self.time_unformatted, y=y_axis, y_label_name = y_label_name)
        self.myFig.update()
        self.myFig.flush_events()

        self.row2.addWidget(self.myFig)

        self.layout.addLayout(self.row2)        
        # Clear the canvas and plot the data
             

    