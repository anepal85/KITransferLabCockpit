import os
import shutil
from sklearn.model_selection import train_test_split

class YoloDataSplitter:
    """
        Utility class for splitting YOLO data into train, validation, and test sets.

        Args:
            images_path (str): Path to the directory containing the image files.
            labels_path (str): Path to the directory containing the label files.
            train_path (str): Path to the directory where the train set will be saved.
            val_path (str): Path to the directory where the validation set will be saved.
            test_path (str): Path to the directory where the test set will be saved.
        """
    def __init__(self, images_path, labels_path, train_path, val_path, test_path):
        self.images_path = images_path
        self.labels_path = labels_path
        
        self.train_path = train_path
        self.val_path = val_path
        self.test_path = test_path

        self.train_path_l = os.path.join(self.labels_path, 'train')
        self.test_path_l = os.path.join(self.labels_path, 'test')
        self.val_path_l = os.path.join(self.labels_path, 'val')


    def _move_files(self, files, dst_path_img, dst_path_label):
        """
        Move files from the source directory to the destination directory.

        Args:
            files (list): List of file names to be moved.
            dst_path_img (str): Destination path for image files.
            dst_path_label (str): Destination path for label files.
        """
        for file in files:
            image_src = os.path.join(self.images_path, file)
            label_src = os.path.join(self.labels_path, os.path.splitext(file)[0] + '.txt')
            shutil.move(image_src, os.path.join(dst_path_img, file))
            shutil.move(label_src, os.path.join(dst_path_label, os.path.splitext(file)[0] + '.txt'))

    def split_data(self, val_size=0.2, test_size=0.2, random_state=42):
        """
        Split the YOLO data into train, validation, and test sets.

        Args:
            val_size (float): The proportion of data to be used for validation (default: 0.2).
            test_size (float): The proportion of data to be used for testing (default: 0.2).
            random_state (int): Random seed for reproducibility (default: 42).
        """
        # Get a list of all the image files in the images directory
        image_files = [f for f in os.listdir(self.images_path) if f.endswith('.jpg')]

        # Split the image files into train, validation, and test sets
        train_files, test_files = train_test_split(image_files, test_size=test_size, random_state=random_state)
        train_files, val_files = train_test_split(train_files, test_size=val_size, random_state=random_state)

        # Create the train, validation, and test directories
        os.makedirs(self.train_path, exist_ok=True)
        os.makedirs(self.val_path, exist_ok=True)
        os.makedirs(self.test_path, exist_ok=True)

         # Create the train, validation, and test directories
        os.makedirs(self.train_path_l, exist_ok=True)
        os.makedirs(self.val_path_l, exist_ok=True)
        os.makedirs(self.test_path_l, exist_ok=True)

        # Move the image and label files to their respective directories
        self._move_files(train_files, self.train_path, self.train_path_l)
        self._move_files(val_files, self.val_path, self.val_path_l)
        self._move_files(test_files, self.test_path, self.test_path_l)

