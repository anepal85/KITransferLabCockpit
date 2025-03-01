import PyQt5
import json, os 


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

json_dir = os.path.join(parent_dir, 'Data', 'training')

class SelectModelPopup(PyQt5.QtWidgets.QDialog):
    """
    A popup window for selecting a pre-trained AI model.

    This class inherits from PyQt5.QtWidgets.QDialog and provides a graphical user interface for selecting 
    pre-trained models to use in AI applications. 
    It includes a file selection button and label, a file list widget for displaying the selected models, 
    and several buttons for adding, removing, and applying the selected models.

    Attributes:
        None

    Methods:
        __init__(self, parent=None): Initializes the SelectModelPopup.
        load_files(self): Loads a list of files from a JSON file and populates the file list widget.
        select_file_button_clicked(self): Opens a file dialog to select a file.
        add_file_button_clicked(self): Adds the selected file to the list widget with a custom name.
        remove_file_button_clicked(self): Removes the selected file from the list widget.
        apply_button_clicked(self): Gets the files from the list widget and saves them to a JSON file.

    Usage:
        Instantiate the SelectModelPopup class to create a popup window for selecting pre-trained AI models.
    """

    def __init__(self, parent=None):
        """Initializes the SelectModelPopup."""
        super(SelectModelPopup, self).__init__(parent)

        # Set the title and size of the pop up window
        self.setWindowTitle('Select AI Model')
        self.resize(600, 400)

        # Create the layout for the pop up window
        self.layout = PyQt5.QtWidgets.QVBoxLayout(self)

        # Create the file selection button and label
        self.select_file_button = PyQt5.QtWidgets.QPushButton('Select Pretrained Model', self)
        self.select_file_button.clicked.connect(self.select_file_button_clicked)
        self.selected_file_label = PyQt5.QtWidgets.QLabel('No .pt file selected', self)

        # Create the file list widget
        self.file_list = PyQt5.QtWidgets.QListWidget(self)

        # Create the add file button
        self.add_file_button = PyQt5.QtWidgets.QPushButton('Add Model to List', self)
        self.add_file_button.clicked.connect(self.add_file_button_clicked)

        # Create the remove file button
        self.remove_file_button = PyQt5.QtWidgets.QPushButton('Remove Model from List', self)
        self.remove_file_button.clicked.connect(self.remove_file_button_clicked)

        # Create the apply button
        self.apply_button = PyQt5.QtWidgets.QPushButton('Use selected model', self)
        self.apply_button.clicked.connect(self.apply_button_clicked)

        # Add the widgets to the layout
        self.layout.addWidget(self.select_file_button)
        self.layout.addWidget(self.selected_file_label)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.add_file_button)
        self.layout.addWidget(self.remove_file_button)
        self.layout.addWidget(self.apply_button)

        # Load files from JSON file
        self.load_files()

    def load_files(self):
        """Loads a list of files from a JSON file and populates the file list widget."""
        try:
            with open(os.path.join(json_dir, 'modelList.json'), 'r') as f:
                files = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return

        if files:
            for file in files:
                name = file.get('name')
                path = file.get('path')
                self.file_list.addItem(name + '|| ' + path)


    def select_file_button_clicked(self):
        """Open a file dialog to select a file."""
        file_path, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, "Select File",None,"Pretrained Models (*.pt)")
        if file_path:
            self.selected_file_label.setText(file_path)

    def add_file_button_clicked(self):
        """Adds the selected file to the list widget with custom name."""
        file_path = self.selected_file_label.text()
        if file_path:
            name, ok = PyQt5.QtWidgets.QInputDialog.getText(self, 'Name Input Dialog', 'Enter custom name for Model:')
            if ok and name:
                self.file_list.addItem(name + '|| ' + file_path)
                self.selected_file_label.setText('No file selected')

    def remove_file_button_clicked(self):
        """Removes the selected file from the list widget."""
        item = self.file_list.currentItem()
        if item:
            self.file_list.takeItem(self.file_list.row(item))

    def apply_button_clicked(self):
        """Gets the files from the list widget and saves them to a JSON file."""
        files = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            name, path = item.text().split('|| ')
            files.append({'name': name, 'path': path})
        if files:
            with open(os.path.join(json_dir, 'modelList.json'), 'w') as f:
                json.dump(files, f)
            self.accept()
        else:
            PyQt5.QtWidgets.QMessageBox.warning(self, 'Warning', 'No files selected!')
