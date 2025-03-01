from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTextEdit
from ultralytics import YOLO
from PyQt5 import QtCore
import os
import argparse
from ultralytics.yolo.v8 import detect
from ultralytics.yolo.engine.model import TASK_MAP 

class UpdateMetricsSignalEmitter(QObject):
    """
    A class to emit a signal when metrics are updated.

    Attributes:
        update_metrics_signal (pyqtSignal): Signal emitted when metrics are updated.
    """
    update_metrics_signal = pyqtSignal(str)

# Create a global instance of UpdateMetricsSignalEmitter
metrics_signal_emitter = UpdateMetricsSignalEmitter()

class CustomDetectionTrainer(detect.DetectionTrainer):
    """
    A custom detection trainer class.

    Args:
        overrides (dict): Dictionary of overrides for the trainer.

    Inherits from detect.DetectionTrainer.
    """
    def __init__(self, overrides=None):
        super().__init__(overrides=overrides)

    def save_metrics(self, metrics):
        """
        Save the metrics and emit a signal with the metrics.

        Args:
            metrics (dict): Dictionary of metrics.
        """
        
        keys, vals = list(metrics.keys()), list(metrics.values())
        n = len(metrics) + 1  # number of cols
        s = '' if self.csv.exists() else (('%23s,' * n % tuple(['epoch'] + keys)).rstrip(',') + '\n')  # header

        #print(f'_start____{self.epoch} :: {vals}_____end_')
        
        # with open(self.csv, 'a') as f:
        #     f.write(s + ('%23.5g,' * n % tuple([self.epoch] + vals)).rstrip(',') + '\n')

         # Emit the update_metrics_signal with the metrics as a string
        metrics_signal_emitter.update_metrics_signal.emit(s + ('%23.5g,' * n % tuple([self.epoch] + vals)).rstrip(',') + '\n')
        super().save_metrics(metrics)

    
# Update TASK_MAP to use custom DetectionTrainer class
TASK_MAP['detect'][1] = CustomDetectionTrainer


class YoloTrainer():
    """
    A class for training YOLO models.

    Args:
        data_path (str): Path to the data.
        output_path (str): Path to the output.
        image_size (int): Size of the image (default: 32).
    """
   
    def __init__(self, data_path, output_path, image_size=32):  

        self.parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        yolo_data_path_root_dir = os.path.join(self.parent_dir,'Data', 'YOLOv8')

        self.data_path = os.path.join(yolo_data_path_root_dir, 'data', data_path)

        self.output_path = os.path.join(yolo_data_path_root_dir, output_path)

        if not os.path.isdir(self.output_path):
            self.output_path = os.makedirs(os.path.join(yolo_data_path_root_dir, output_path), exist_ok=True)
        
        self.image_size = image_size

        self.name_of_run = 'test_yolov8'

        self.model = None 

   
    def train_model(self, *args):

        # Load the model
        self.model = YOLO("yolov8n.pt")

        self.model.trainer = TASK_MAP['detect'][1]

        '''
        In following way the hyperparameters can modified 

        # parser = argparse.ArgumentParser()
        # for arg in args[0]:
        #     name, value = arg.split('=')
        #     parser.add_argument(f'--{name}', type=str, default=value)
        # args_dict = vars(parser.parse_args())  

        #args_dict could be passed to self.trin.model() 
        # Examples are epochs and batch_size

        '''
        # Parse the argument list
        # # Train the model
        self.model.train(data=os.path.join(self.data_path, 'yolov8_custom.yaml'), 
                    task='detect',
                    name=self.name_of_run,
                    epochs=5, 
                    pretrained=True, 
                    imgsz=self.image_size, 
                    batch=16,
                    project=self.output_path)
        


class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)  # Set the text edit as read-only

    def append_text(self, text):
        # Append the text to the current text in the text edit, followed by a newline character
        self.append(text + '\n')

    @QtCore.pyqtSlot(str)
    # Slot function to update the custom text edit widget with new text
    def update_custom_text_edit(self, text):
        self.append_text(text)

