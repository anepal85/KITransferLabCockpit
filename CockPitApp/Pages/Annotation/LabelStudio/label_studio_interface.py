import time
import requests
from PyQt5.QtCore import QUrl, Qt 

from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


from .label_studio_local_server import LabelStudioThread 
from .label_studio_api import LabelStudioAPI 
from .label_studio_base_url import * 
from ...utils.set_center_alignment import set_alignment 
from .QWbEngineViewDownloadHandler import MyWebEngineView 

class LabelStudioInterfaceWidget(QtWidgets.QWidget):
    """
        Widget for interacting with Label Studio.

        This widget provides a graphical user interface for starting and stopping the Label Studio server,
        authenticating with the Label Studio API, and displaying the Label Studio interface.

        """
    def __init__(self)-> None:
        super(LabelStudioInterfaceWidget, self).__init__()
        # Set up the UI
        self.layout = QVBoxLayout(self)

        self.first_row_layout = QHBoxLayout()

        self.login_button = QPushButton('Start')
        self.login_button.setMinimumWidth(200) 
        self.login_button.setMaximumWidth(200) 
        self.login_button.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.login_button.setStyleSheet("background-color: green; font-size: 18px; color: rgba(0,0,0, 100%);")       
        self.login_button.clicked.connect(self.login)
        self.first_row_layout.addWidget(self.login_button)#, alignment=Qt.AlignCenter| Qt.AlignTop)

        self.stop_button = QPushButton('Stop')
        self.stop_button.setMaximumWidth(200) 
        self.stop_button.setMinimumWidth(200) 
        self.stop_button.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self.stop_button.setStyleSheet("background-color: red; font-size: 18px; color: rgba(0, 0, 0, 100%);")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        self.first_row_layout.addWidget(self.stop_button)#, alignment=Qt.AlignCenter| Qt.AlignTop)

        self.layout.addLayout(self.first_row_layout)

        self.webview = MyWebEngineView()
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)


        # Set up the Label Studio thread
        self.label_studio_thread = LabelStudioThread()
            	
        # Set up the Label Studio API
        self.label_studio_api = LabelStudioAPI()
        self.label_studio_api.login_signal.connect(self.on_login)
        self.label_studio_api.authenticated_signal.connect(self.on_authenticate)


    def login(self):
        # Start the Label Studio server and authenticate with the API
        self.label_studio_thread.start()
        self.login_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        time.sleep(5)  # Wait for the server to start up
        
        while True:
            # Check if the server is running and responding
            try:
                response = requests.get(LABEL_STUDIO_BASE_URL)
                if response.status_code == 200:
                    self.label_studio_api.authenticate()
                    break 
                # else:
                #     self.stop()
                #     self.setText('Failed to connect to Label Studio server')
            except requests.exceptions.ConnectionError:
                #self.stop()
                print('Failed to connect to Label Studio server')
            
        print("Out of the endless loop")


    def stop(self):
        # Stop the Label Studio server
        self.label_studio_thread.stop_server()
        self.label_studio_thread.stop()
        self.stop_button.setEnabled(False)
        self.login_button.setEnabled(True)


    def on_login(self, success):
        # Handle the login result
        if success:
            print('Opening Label Studio homepage...')
            self.login_button.setEnabled(False)

            url = QUrl(f'{LABEL_STUDIO_BASE_URL}/user/login')

            self.webview.load(url)
        else:
            print('Failed to authenticate with Label Studio API')

    def on_authenticate(self, success):
        # Handle the login result
        if success:
            print('Opening Label Studio Projects...')
            #self.label_studio_api.export_yolo_annotation()
            self.login_button.setEnabled(False)

            # Load the Label Studio homepage in the QWebEngineView widget

            url = QUrl(f'{LABEL_STUDIO_BASE_URL}/user/login')

            self.webview.load(url)
        else:
            print('Failed to authenticate with Label Studio API')