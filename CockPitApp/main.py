from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from UI.ui_MainWindow import Ui_MainWindow
from Pages.Annotation.annotation import AnnotationWidget 
import os 
from PyQt5.QtCore import pyqtSlot

from Pages.home import HomeWidget
from Pages.Training.training import TrainingWidget 
from Pages.Visualization.yolov8_visualization import CustomYOLOWidget 


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Initialize the main application window.

    This method sets up the GUI by connecting signals and slots, creating and adding widgets to the stacked widget,
    and initializing default values for certain components. It also sets up the initial view to be displayed.

    The main functionality includes:
    - Handling menu button clicks to switch between different pages (views) within the stacked widget.
    - Creating and managing the QStackedWidget to hold the different views.
    - Loading the initial view (HomeWidget) and adding it to the stacked widget.
    - Setting up the TrainingWidget to listen for a signal when training is done, and updating the visualization page
      with the latest results.
    - Setting up the CustomYOLOWidget with default CSV and image files.
    - Displaying the main window and starting the application event loop.

    """
    def __init__(self):
        super().__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.yolo_result_widget = None 
        
        ## Menubuttons
        self.annotation_button.clicked.connect(self.showAnnotationPage)

        self.training_button.clicked.connect(self.showTrainingPage)

        self.home_button.clicked.connect(self.showHomePage)

        self.visualization_button.clicked.connect(self.showVizualizationPage)

        
        # Create the QStackedWidget and add it to the container widget
        self.stacked_widget = QtWidgets.QStackedWidget(self.content_frame)
        

        # Add the views to the QStackedWidget
        self.stacked_widget.addWidget(HomeWidget())
        self.stacked_widget.addWidget(AnnotationWidget())

        self.training_widget = TrainingWidget()

        self.training_widget.is_training_done.connect(self.update_vizualization_after_training)

        self.stacked_widget.addWidget(self.training_widget)
        

        self.horizontalLayout_8.addWidget(self.stacked_widget)

        # Get the path to the directory where main.py is located
        root_dir = os.path.dirname(os.path.abspath(__file__))

        name_of_run_full_path_default = os.path.join(root_dir, 'Data','YOLOv8','execution_test', 'test_yolov82')

        csv_file = os.path.join(name_of_run_full_path_default, 'results.csv')
        image_files = [os.path.join(name_of_run_full_path_default, 'results.png'), os.path.join(name_of_run_full_path_default, 'confusion_matrix.png')]
        
        self.yolo_result_widget = CustomYOLOWidget(csv_file, image_files)

        self.stacked_widget.addWidget(self.yolo_result_widget)

        
        ### Home 
        self.stacked_widget.setCurrentIndex(0)
                                                                 
    def showHomePage(self):
        # Set the current index to the first view
        self.stacked_widget.setCurrentIndex(0)
        ### visualizaiton Button 
        

    def showAnnotationPage(self):
        self.stacked_widget.setCurrentIndex(1)

        #self.stackedWidget.setCurrentWidget()

    def showTrainingPage(self):
        self.stacked_widget.setCurrentIndex(2)

    def showVizualizationPage(self):
        self.stacked_widget.setCurrentIndex(3)
            

    @pyqtSlot()
    def update_vizualization_after_training(self):
        if self.training_widget.yolo_output_path and self.training_widget.yolo_name_of_run is not None:
            ## newest Vizualization needs to be active 
            name_of_run_full_path = os.path.join(self.training_widget.yolo_output_path, self.training_widget.yolo_name_of_run)

            csv_file = os.path.join(name_of_run_full_path, 'results.csv')
            image_files = [os.path.join(name_of_run_full_path, 'results.png'), os.path.join(name_of_run_full_path, 'confusion_matrix.png')]

            self.yolo_result_widget = CustomYOLOWidget(csv_file, image_files)

            self.stacked_widget.addWidget(self.yolo_result_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
