import os 
import yaml
from ..Annotation.LabelStudio.unzip__recent_yolo_dowloaded_folder import unzip_newest_zip_file
from ..Annotation.LabelStudio.create_yolo_folder_structure_with_data import YoloDataSplitter

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
data_path = os.path.join(parent_dir, 'Data', 'YOLOv8', 'data')

class SetupYoloTraining:
    """
    This class is responsible for setting up YOLO training data and configuration.

    It creates the required folder structure, YAML file, and performs other necessary steps.

    Attributes:
        root_data_dir (str): Root data directory path.
        zip_extracted_path (str): Path to the extracted ZIP file.
        images_path (str): Path to the images directory.
        labels_path (str): Path to the labels directory.
        train_path (str): Path to the training images directory.
        val_path (str): Path to the validation images directory.
        test_path (str): Path to the test images directory.
    """

    def __init__(self):
        self.root_data_dir = data_path 

        ### Unzip the latest .zip file in folder
        self.zip_extracted_path = unzip_newest_zip_file(self.root_data_dir)

        #print(f'________{self.zip_extracted_path}______')
        if self.zip_extracted_path is not None:
            self.images_path = os.path.join(self.zip_extracted_path, 'images')
            self.labels_path = os.path.join(self.zip_extracted_path, 'labels')
            self.train_path = os.path.join(self.images_path, 'train')
            self.val_path = os.path.join(self.images_path, 'val')
            self.test_path = os.path.join(self.images_path, 'test')

            self.prepare_folderstructure(self.images_path, self.labels_path, 
                                              self.train_path, self.val_path, self.test_path)
            self.create_yaml(self.zip_extracted_path, self.train_path, 
                             self.val_path, self.zip_extracted_path+'/classes.txt', self.test_path)


    def prepare_folderstructure(self, images_path, labels_path, train_path, val_path, test_path):
        yolo_data_splitter = YoloDataSplitter(images_path, labels_path, train_path, val_path, test_path)
        yolo_data_splitter.split_data(val_size=0.2, test_size=0.2, random_state=42)

    def create_yaml(self, zip_extracted_path, train_path, val_path, classes_path_file, test_path):
        yaml_creater = YOLOYamlCreator(zip_extracted_path, train_path, val_path, 
                                       classes_path_file, test_path) 
        yaml_creater.create_yaml()

        assert os.path.isfile(os.path.join(self.zip_extracted_path, 'yolov8_custom.yaml'))


class YOLOYamlCreator:
    def __init__(self, root_data_dir, train_path, val_path, classes_file_path, test_path):
        self.root_data_dir = root_data_dir
        self.train_path = train_path
        self.val_path = val_path
        self.classes_file_path = classes_file_path
        self.test_path = test_path 

    def create_yaml(self):
        data = {
            "nc": self._count_classes(),
            "train": self.train_path,
            "val": self.val_path,
            "test":self.test_path,
            "names": self.classes
        }
        with open(self.root_data_dir + "/yolov8_custom.yaml", "w") as f:
            yaml.dump(data, f)
            
    def _count_classes(self):
        with open(self.classes_file_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        return len(self.classes)


### this checks whether a given diretory contains two dirs, a .yaml and a .txt  file
def check_yolo_data_directory(path_to_dir):
    # Check if directory exists
    if not os.path.isdir(path_to_dir):
        raise ValueError(f"{path_to_dir} is not a directory.")

    # Check if subdirectories exist
    subdirectories = [d for d in os.listdir(path_to_dir) if os.path.isdir(os.path.join(path_to_dir, d))]
    if len(subdirectories) != 2:
        raise ValueError(f"{path_to_dir} does not contain two subdirectories.")
    if "images" not in subdirectories or "labels" not in subdirectories:
        raise ValueError(f"{path_to_dir} does not contain the required 'images' and 'labels' subdirectories.")

    # Check if yaml and txt files exist
    yaml_file = os.path.join(path_to_dir, "yolov8_custom.yaml")
    if not os.path.isfile(yaml_file):
        raise ValueError(f"{path_to_dir} does not contain the required 'yolov8_custom.yaml' file.")
    txt_file = os.path.join(path_to_dir, "classes.txt")
    if not os.path.isfile(txt_file):
        raise ValueError(f"{path_to_dir} does not contain the required 'classes.txt' file.")
    
    # If all checks pass, return True
    return True

