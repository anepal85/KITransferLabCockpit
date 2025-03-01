from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CustomYOLOWidget(QWidget):
    """
        A custom widget for displaying a table and images related to YOLO data.

        Args:
            csv_file (str): The path to the CSV file containing data for the table.
            image_files (list): A list of image file paths to be displayed.

        """
    def __init__(self, csv_file, image_files):
        super().__init__()
        self.csv_file = csv_file
        self.image_files = image_files

        self.init_ui()

    def init_ui(self):
        # Initialize the layout
        layout = QVBoxLayout(self)

        # Create the first row containing the table
        row1 = QHBoxLayout()
        layout.addLayout(row1)

        # Create and fill the table
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.fill_table()
        row1.addWidget(self.table)

        # Create the second row containing the images
        row2 = QHBoxLayout()
        layout.addLayout(row2)

        # Create the first image label and add it to the second row
        self.image1_label = QLabel()
        row2.addWidget(self.image1_label)

        # Create the second image label and add it to the second row
        self.image2_label = QLabel()
        row2.addWidget(self.image2_label)

        # Set the widget properties
        self.setLayout(layout)
        self.setMinimumSize(500, 500)
        self.setWindowTitle("Custom Widget")

        # Plot the images
        self.plot_images()

    def fill_table(self):
        try:
            # Read the CSV file and fill the table
            with open(self.csv_file) as f:
                lines = f.readlines()
                headers = lines[0].strip().split(",")
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                for i, line in enumerate(lines[1:]):
                    row = line.strip().split(",")
                    self.table.setRowCount(i + 1)
                    for j, item in enumerate(row):
                        table_item = QTableWidgetItem(item)
                        table_item.setFlags(Qt.ItemIsEnabled)
                        self.table.setItem(i, j, table_item)
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file}' not found.")

    def plot_images(self):
    # Set the images in the image labels and resize them
        if len(self.image_files) > 0:
            image1 = QPixmap(self.image_files[0]).scaled(2*600, 2*300, Qt.KeepAspectRatio)
            self.image1_label.setPixmap(image1)
        if len(self.image_files) > 1:
            image2 = QPixmap(self.image_files[1]).scaled(2*600, 2*300, Qt.KeepAspectRatio)
            self.image2_label.setPixmap(image2)
