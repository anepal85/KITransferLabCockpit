from PyQt5 import QtWidgets
import PyQt5
from PyQt5.QtWidgets import QPushButton, QLabel, QListWidgetItem, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import os 
from .setup_yolo_training import check_yolo_data_directory
from Pages.Training.yolov8_custom_training import metrics_signal_emitter 
from PyQt5.QtCore import pyqtSignal


from Pages.Training.SelectModel import SelectModelPopup
from Pages.Training.StartTraining import StartTrainingPopup
from Pages.Training.yolov8_custom_training import CustomTextEdit, YoloTrainer, UpdateMetricsSignalEmitter
from Pages.Training.setup_yolo_training import SetupYoloTraining 

class TextEditStream(PyQt5.QtCore.QTextStream):
    """
    Custom QTextStream that writes to a QTextEdit.

    Args:
        text_edit: A QTextEdit object to write to.
    """
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def write(self, string):
        """
        Write string to QTextEdit.

        Args:
            string: The string to write to the text edit.
        """
        self.text_edit.moveCursor(PyQt5.QtGui.QTextCursor.End)
        self.text_edit.insertPlainText(string)


class TrainingWidget(QtWidgets.QWidget):
    """
    The Sub Widget of the Cockpit which handles the training of the AI.

    Attributes:
        model_location: A string representing the location of the model.
        dataset_location: A string representing the location of the dataset.
        hyper_params: A list of hyperparameters for the training.
        yolo_trainer: A YoloTrainer object for handling the training.

    Methods:
        __init__: Initializes the TrainingWidget object.
    """

    model_location = None
    dataset_location = None
    hyper_params = []
    is_training_done = pyqtSignal(bool)
    
    def __init__(self) -> None:
        super(TrainingWidget, self).__init__()
        
        self.selected_data_dir = None 
        self.yolo_output_path = None
        self.yolo_name_of_run = None 

        # Set the font size for the widget
        self.setStyleSheet("font-size: 20px;")

        # Create the layout for the widget
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create rows to house the content of the Tab
        self.button_layout = QtWidgets.QHBoxLayout()
        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()
        self.third_row_layout = QtWidgets.QHBoxLayout()
        self.fourth_row_layout = QtWidgets.QHBoxLayout()

        

        self.select_model_button = QtWidgets.QPushButton(self)
        self.select_model_button.setText('Select AI Model')
        self.select_model_button.setStyleSheet("font-size: 20px; background-color: #007bff; color: #fff; padding: 10px; border-radius: 5px;")
        self.select_model_button.clicked.connect(self.select_model_button_clicked)

        self.start_training_button = QtWidgets.QPushButton(self)
        self.start_training_button.setText('Start Training')
        self.start_training_button.setStyleSheet("font-size: 20px; background-color: #28a745; color: #fff; padding: 10px; border-radius: 5px;")
        self.start_training_button.clicked.connect(self.start_training_button_clicked)

        self.pause_training_button = QtWidgets.QPushButton(self)
        self.pause_training_button.setText('Pause Training')
        self.pause_training_button.setStyleSheet("font-size: 20px; background-color: #ffc107; color: #fff; padding: 10px; border-radius: 5px;")
        self.pause_training_button.clicked.connect(self.pause_training_button_clicked)

        self.stop_training_button = QtWidgets.QPushButton(self)
        self.stop_training_button.setText('Stop Training')
        self.stop_training_button.setStyleSheet("font-size: 20px; background-color: #dc3545; color: #fff; padding: 10px; border-radius: 5px;")
        self.stop_training_button.clicked.connect(self.stop_training_button_clicked)

        self.test_model_button = QtWidgets.QPushButton(self)
        self.test_model_button.setText('Test Model')
        self.test_model_button.setStyleSheet("font-size: 20px; background-color: #8a19d6; color: #fff; padding: 10px; border-radius: 5px;")
        self.test_model_button.clicked.connect(self.test_model_button_clicked)

        
        self.button_layout.addWidget(self.select_model_button)
        self.button_layout.addWidget(self.start_training_button)
        self.button_layout.addWidget(self.pause_training_button)
        self.button_layout.addWidget(self.stop_training_button)
        self.button_layout.addWidget(self.test_model_button)

        self.selected_file_name_label = QLabel(self)
        self.selected_file_path_label = QLabel(self)
        self.first_row_layout.addWidget(self.selected_file_name_label)
        self.second_row_layout.addWidget(self.selected_file_path_label)

        self.metrics_table = QTableWidget(self)
        self.metrics_table.setColumnCount(2)
        self.metrics_table.setHorizontalHeaderLabels(['Metric', 'Value'])

        # Adding Metrics Rows
        self.metrics_table.insertRow(0)
        self.metrics_table.setItem(0, 0, QTableWidgetItem('Accuracy'))
        self.metrics_table.setItem(0, 1, QTableWidgetItem('0.93'))
        self.metrics_table.insertRow(1)
        self.metrics_table.setItem(1, 0, QTableWidgetItem('Loss'))
        self.metrics_table.setItem(1, 1, QTableWidgetItem('0.22'))
        self.metrics_table.insertRow(2)
        self.metrics_table.setItem(2, 0, QTableWidgetItem('Confusion Matrix'))
        self.metrics_table.setItem(2, 1, QTableWidgetItem('[[87, 12], [5, 96]]'))
        self.metrics_table.insertRow(3)
        self.metrics_table.setItem(3, 0, QTableWidgetItem('AUC (Area Under ROC curve)'))
        self.metrics_table.setItem(3, 1, QTableWidgetItem('0.97'))
        self.metrics_table.insertRow(4)
        self.metrics_table.setItem(4, 0, QTableWidgetItem('Mean Absolute Error (MAE)'))
        self.metrics_table.setItem(4, 1, QTableWidgetItem('0.11'))
        self.metrics_table.insertRow(5)
        self.metrics_table.setItem(5, 0, QTableWidgetItem('Root Mean Square Error (RMSE)'))
        self.metrics_table.setItem(5, 1, QTableWidgetItem('0.15'))
        self.metrics_table.insertRow(6)
        self.metrics_table.setItem(6, 0, QTableWidgetItem('R Square'))
        self.metrics_table.setItem(6, 1, QTableWidgetItem('0.81'))


        self.fourth_row_layout.addWidget(self.metrics_table)

        self.select_dataset_button = QPushButton('Select Dataset Test')
        setup_yoloTraining = SetupYoloTraining()
        self.select_dataset_button.clicked.connect(self.select_dataset_for_yolo_training)
        self.fourth_row_layout.addWidget(self.select_dataset_button)

        self.start_training_button_test = QPushButton('Start Training Test')
        
        self.fourth_row_layout.addWidget(self.start_training_button_test)

        # Create the custom text edit widget
        self.custom_text_edit = CustomTextEdit()

        metrics_signal_emitter.update_metrics_signal.connect(self.custom_text_edit.update_custom_text_edit)
        self.start_training_button_test.clicked.connect(self.start_training_test)
        

        # # Set fixed size
        self.custom_text_edit.setFixedSize(PyQt5.QtCore.QSize(900, 200))
        self.third_row_layout.addWidget(self.custom_text_edit)


        # Add all Rows to layout
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.first_row_layout)
        self.layout.addLayout(self.second_row_layout)
        self.layout.addLayout(self.third_row_layout)
        self.layout.addLayout(self.fourth_row_layout)

        self.setLayout(self.layout)

    def select_dataset_for_yolo_training(self):
        data_dir = self.import_folder()
        if data_dir is not None:
            assert os.path.isdir(data_dir)

        self.run_set_up_yolo_on_selected_data_dir(data_dir)
        self.selected_data_dir = data_dir 
    
    def start_training_test(self):
        try:
            if self.selected_data_dir is not None:
                if os.path.isdir(self.selected_data_dir):
                    
                    self.yolo_model = YoloTrainer(self.selected_data_dir, 'execution_test')
                    self.yolo_model.train_model()
                    
                    self.yolo_output_path = self.yolo_model.output_path 
                    self.yolo_name_of_run = self.yolo_model.name_of_run

                    self.is_training_done.emit(True)
            else:
                raise AttributeError("First select data")   
        except AttributeError as e:
            print(str(e))


    def run_set_up_yolo_on_selected_data_dir(self, data_dir):  
        assert check_yolo_data_directory(data_dir) is True 
    
    def import_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select dataset directory", "", options=options)
        if folder_path:
            if not os.path.isdir(folder_path):
                raise ValueError("Selected path is not a directory")
            return folder_path
        
    def set_alignment(self):
        self.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

    def select_model_button_clicked(self):
        """Opens a popup to select a model file and updates the GUI if a model is selected."""
        popup = SelectModelPopup(self)
        if popup.exec_() == PyQt5.QtWidgets.QDialog.Accepted:
            selected_file_name, self.model_location = popup.file_list.currentItem().text().split('|| ')[0:2]
            self.selected_file_name_label.setText(f'Selected file: {selected_file_name}')
            self.selected_file_path_label.setText(f'Selected file path: {self.model_location}')

    def start_training_button_clicked(self):
        """
        Handles the click event of the start training button.
        Opens a popup to select a dataset for training and starts the training process
        """
        if not self.model_location:
            PyQt5.QtWidgets.QMessageBox.warning(self, 'Warning', 'Please select a model first!')
            return

        popup = StartTrainingPopup(self.model_location, self)
        if popup.exec_() == PyQt5.QtWidgets.QDialog.Accepted:
            self.dataset_location = popup.dataset_path

            self.hyper_params = popup.hyperparams
            popup.close()
            self.yolo_trainer = YoloTrainer(self.model_location,self.dataset_location,self.model_location) #output location currently still model location
            #self.yolo_trainer.train_model(TextEditStream(self.text_edit), self.hyper_params)
            print("This is in standard output")
            
        popup.close()

    def pause_training_button_clicked(self):
        """
        This function has not been tested yet

        For future, kill the subtask in which the training process runs and then save the weigths

        """
        try:
            self.yolo_trainer.model.save_weights()
            self.yolo_trainer.model.save_optimizer_state()
            print("paused training")
        except TypeError:
            print("Can pause training because it hase no been started yet")
    
    def stop_training_button_clicked(self):
        """
        implementation needed
        """
        print('Stop Model button clicked')

    def test_model_button_clicked(self):
        """
        implementation needed
        """
        print('Test Model button clicked')

