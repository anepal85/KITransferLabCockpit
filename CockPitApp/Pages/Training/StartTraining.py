import PyQt5

from Pages.Training.HyperList import HyperParamList


class StartTrainingPopup(PyQt5.QtWidgets.QDialog):
    """
    A popup window to select a dataset for the training of the AI and to enter hyperparameters for the training.

    This class represents a dialog window that allows the user to select a dataset for the training of an AI and
    to enter hyperparameters for the training.
    It inherits from PyQt5.QtWidgets.QDialog and contains several widgets 

    Attributes:
        dataset_path: A string representing the path to the selected dataset.
        HyperParam: An instance of the HyperParamList class containing the hyperparameters for the training.

    Args:
        selected_file_path: A string representing the path of the selected file.
        parent: An optional QWidget representing the parent widget.

    Methods:
        __init__(self, selected_file_path: str, parent: QWidget = None): Initializes the class by setting the attributes, creating the interface, and defining the custom functions.

        edit_default_value(self, name: str): Edits the default value for a hyperparameter with the given name.

        remove_from_list(self, name: str): Removes a widget from the scroll layout and updates HyperParam.
    """
    def __init__(self, selected_file_path, parent=None):
        super(StartTrainingPopup, self).__init__(parent)
        self.dataset_path = None
        self.HyperParam = HyperParamList()

        self.file_path_model = selected_file_path

        # Set the title and size of the pop up window
        self.setWindowTitle('Select Data Set')
        self.resize(600, 400)

        # Create the layout for the pop up window
        self.layout = PyQt5.QtWidgets.QVBoxLayout(self)

        # Create the file selection button and label
        self.select_folder_button = PyQt5.QtWidgets.QPushButton('Select Data Set', self)
        self.select_folder_button.clicked.connect(self.select_dataSet_button_clicked)
        self.selected_folder_label = PyQt5.QtWidgets.QLabel('No DataSet (folder) selected', self)
        
        self.layout.addWidget(self.select_folder_button)
        self.layout.addWidget(self.selected_folder_label)

        # Create a scroll area to hold the hyperparameters section
        self.scroll_area = PyQt5.QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Create a container widget to hold the hyperparameter widgets
        self.scroll_content = PyQt5.QtWidgets.QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = PyQt5.QtWidgets.QVBoxLayout(self.scroll_content)

        # Define a custom function for editing the default value of a hyperparameter
        def edit_default_value(name):
            """
            Edit the default value for a hyperparameter with the given name.

            Args:
                name (str): The name of the hyperparameter.

            Returns:
                None.
            """
            current_name = ""
            # loop over all items in the scroll layout
            for i in range(self.scroll_layout.count()):
                # every item in the scroll layout is a PyQt5.QtWidgets.QGroupBox
                widget = self.scroll_layout.itemAt(i).widget()
                # every PyQt5.QtWidgets.QGroupBox contains 3 things 1) the meatballs menu, 2) the label, 3) the input
                for j in range(1,widget.layout().count()): # since we are not interested in the meatballs menu we skip it
                    current_widget = widget.layout().itemAt(j).widget() 
                    if isinstance(current_widget,PyQt5.QtWidgets.QLabel):
                        current_name = current_widget.text().lower().replace(":","")
                    elif isinstance(current_widget, PyQt5.QtWidgets.QLineEdit) and current_name == name:
                        default_value=current_widget.text()
                        self.HyperParam.edit_default_value(name,str(default_value))
                        return
                    elif isinstance(current_widget, PyQt5.QtWidgets.QCheckBox) and current_name == name:
                        if current_widget.isChecked():
                            self.HyperParam.edit_default_value(name,True)
                        else:
                            self.HyperParam.edit_default_value(name,False)
                        return
                    


        # Define a custom function for removing a hyperparameter from the list
        def remove_from_list(name):
            """
            Remove a widget from the scroll layout and update HyperParam.

            Args:
                name (str): The name of the widget to remove.

            Returns:
                None
            """
            current_name = ""
            # loop over all items in the scroll layout
            for i in range(self.scroll_layout.count()):
                # every item in the scroll layout is a PyQt5.QtWidgets.QGroupBox
                widget = self.scroll_layout.itemAt(i).widget()
                # every PyQt5.QtWidgets.QGroupBox contains 3 things 1) the meatballs menu, 2) the label, 3) the input
                for j in range(1,widget.layout().count()): # since we are not interested in the meatballs menu we skip it
                    current_widget = widget.layout().itemAt(j).widget() 
                    if isinstance(current_widget,PyQt5.QtWidgets.QLabel):
                        current_name = current_widget.text().lower().replace(":","")
                        if current_name == name:
                            widget.deleteLater()
                            try:
                                self.scroll_layout.removeWidget(widget)
                            except:
                                pass
                            self.HyperParam.remove(name)
                            return
  
        # Create the hyperparameters section dynamically from hyper_param_list
        for name, default_value, tooltip in self.HyperParam.get():
            group_box = PyQt5.QtWidgets.QGroupBox(self.scroll_content)
            layout = PyQt5.QtWidgets.QVBoxLayout(group_box)

            # Add the meatballs button to the top right corner of the group box
            meatballs_btn = PyQt5.QtWidgets.QToolButton(group_box)
            meatballs_btn.setPopupMode(PyQt5.QtWidgets.QToolButton.InstantPopup)
            meatballs_menu = PyQt5.QtWidgets.QMenu(meatballs_btn)

            # Add actions to the menu
            edit_action = PyQt5.QtWidgets.QAction("Current Value to Default Value", meatballs_menu)
            meatballs_menu.addAction(edit_action)

            remove_action = PyQt5.QtWidgets.QAction("Remove from List", meatballs_menu)
            meatballs_menu.addAction(remove_action)

            # Connect the actions to custom functions for editing/removing
            edit_action.triggered.connect(lambda checked, name=name, : edit_default_value(name))
            remove_action.triggered.connect(lambda checked, name=name: remove_from_list(name))

            # Set the menu for the button
            meatballs_btn.setMenu(meatballs_menu)
            meatballs_btn.setFixedWidth(16)
            layout.addWidget(meatballs_btn, alignment=PyQt5.QtCore.Qt.AlignTop | PyQt5.QtCore.Qt.AlignRight)

            label = PyQt5.QtWidgets.QLabel(name.capitalize() + ':', group_box)
            layout.addWidget(label)

            if isinstance(default_value,bool):
                input_widget = PyQt5.QtWidgets.QCheckBox(group_box)
                input_widget.setChecked(default_value)
            else:
                input_widget = PyQt5.QtWidgets.QLineEdit(group_box)
                input_widget.setText(str(default_value))

            input_widget.setToolTip(tooltip)
            layout.addWidget(input_widget)

            self.scroll_layout.addWidget(group_box)

        # Create the add and remove parameter buttons
        self.add_parameter_button = PyQt5.QtWidgets.QPushButton('Add Parameter', self)
        self.add_parameter_button.clicked.connect(self.add_parameter_button_clicked)
        self.layout.addWidget(self.add_parameter_button)

        # Create the apply button
        self.apply_button = PyQt5.QtWidgets.QPushButton('Start Training', self)
        self.apply_button.clicked.connect(self.apply_button_clicked)
        self.layout.addWidget(self.apply_button)
    


    def select_dataSet_button_clicked(self):
        """
        Handler for the select dataset button click event.

        Opens a file dialog to allow the user to select a folder containing a .yaml file.
        Updates the selected folder label with the chosen folder path.
        """
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.ShowDirsOnly
        folder_path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, "Select DataSet", options=options)
        if folder_path:
            # Check if there is a .yaml file in the selected folder
            import os
            if not any(fname.endswith('.yaml') for fname in os.listdir(folder_path)):
                PyQt5.QtWidgets.QMessageBox.warning(self, "Warning", "No .yaml file found in the selected folder.")
                return
            self.selected_folder_label.setText("Selected folder: " + folder_path)
            self.dataset_path = folder_path

    def add_parameter_button_clicked(self):
        """Handles the button click event to add a new hyperparameter."""
        name, ok = PyQt5.QtWidgets.QInputDialog.getText(self, 'Name Input Dialog', 'Enter parameter name:')
        if ok and name:
            # Check if the parameter name already exists in the hyperparams list
            hyperparams = self.HyperParam.get()
            for param in hyperparams:
                if name.lower().strip() == param[0].lower():
                    PyQt5.QtWidgets.QMessageBox.warning(self, "Warning", f"The parameter '{name}' already exists.")
                    return

            value, ok = PyQt5.QtWidgets.QInputDialog.getText(self, 'Value Input Dialog', 'Enter parameters default value:')
            if ok and value:
                try:
                    value = float(value)
                except ValueError:
                    try:
                        value = value.strip().lower()
                        if value != "true" or value != "false":
                            raise ValueError
                        value = bool(value)
                    except ValueError:
                        pass

                tooltip, ok = PyQt5.QtWidgets.QInputDialog.getText(self, 'Value Tool Tip Dialog', 'Enter parameters Tool Tip:')
                if ok and tooltip:
                    self.HyperParam.add(name,value,tooltip)

                    PyQt5.QtWidgets.QMessageBox.information(self, "", "The parameter was added and will be visable after restart")

    def apply_button_clicked(self):
        """Handle click event for Apply button."""
        # Check if a dataset has been selected
        if not self.dataset_path:
            PyQt5.QtWidgets.QMessageBox.warning(self, "Warning", "No dataset has been selected.")
            return
        
        #loop over all widgets in the scroll area (the hyperparameters)
        j=-1
        self.hyperparams = []
        hyper_param_list = self.HyperParam.get()
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()

            for j in range(1,widget.layout().count()): # since we are not interested in the meatballs menu we skip it
                current_widget = widget.layout().itemAt(j).widget() 
                if isinstance(current_widget,PyQt5.QtWidgets.QLabel):
                    current_name = current_widget.text().lower().replace(":","")
                elif isinstance(current_widget, PyQt5.QtWidgets.QLineEdit):
                    current_value=str(current_widget.text())   
                elif isinstance(current_widget, PyQt5.QtWidgets.QCheckBox):
                    current_value = str(current_widget.isChecked())
                            
            
            print(current_name,current_value)

            self.hyperparams.append(f"{current_name}={current_value}")
                        
        self.accept()
