import os
import sys
import platform
import time
import requests
import psutil
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QUrl
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Constants
LABEL_STUDIO_PORT = 8080
LABEL_STUDIO_USERNAME = 'anepal857@gmail.com'
LABEL_STUDIO_PASSWORD = '7Anjita2aa*'
LABEL_STUDIO_BASE_URL = f'http://localhost:{LABEL_STUDIO_PORT}'

token = '52297494adebaf4e6826df8e743b072fb508a2e1'


import subprocess

class LabelStudioThread(QThread):
    def __init__(self, parent=None, project_dir=None):
        super().__init__(parent)

    def run(self):
        # Start the Label Studio server using the `label-studio` command and pass the project directory as an argument
        command = ["label-studio", "start"]
        if platform.system() == "Windows":
            command.insert(0, "cmd.exe")
            command.insert(1, "/c")
        subprocess.call(command)


    def stop_server(self):
        # Stop the server by sending a SIGINT signal to the `label-studio` process
        if platform.system() == "Windows":
            subprocess.call(["taskkill", "/f", "/im", "label-studio.exe"])
        # else:
        #     os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
        self.wait()

    def stop(self):
        self.terminate()



class LabelStudioAPI(QObject):
    login_signal = pyqtSignal(bool)
    authenticated_signal = pyqtSignal(bool)


    def __init__(self):
        super().__init__()

    def login(self):
        # Login with the Label Studio API
        url = f'{LABEL_STUDIO_BASE_URL}/user/login'
        data = {
            'username': LABEL_STUDIO_USERNAME,
            'password': LABEL_STUDIO_PASSWORD
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('Successfully Login with Label Studio API')
            self.login_signal.emit(True)
        else:
            print('Failed to Login with Label Studio API')
            self.login_signal.emit(False)


    def authenticate(self):
        # Authenticate with the Label Studio API
        url = f'{LABEL_STUDIO_BASE_URL}/api/projects'

        headers = {"Authorization": f"Token {token}"}

        response = requests.get(url, headers=headers, timeout=1)

        if response.status_code == 200:
            print('Successfully authenticated with Label Studio API')
            self.authenticated_signal.emit(True)
        else:
            print('Failed to authenticate with Label Studio API')
            self.authenticated_signal.emit(False)
    


class MainWindow(QLabel):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle('Label Studio Authentication Example')
        self.layout = QVBoxLayout()
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)
        self.webview = QWebEngineView()
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
        
        # Check if the server is running and responding
        try:
            response = requests.get(LABEL_STUDIO_BASE_URL)
            if response.status_code == 200:
                self.label_studio_api.login()
            else:
                self.stop()
                self.setText('Failed to connect to Label Studio server')
        except requests.exceptions.ConnectionError:
            self.stop()
            self.setText('Failed to connect to Label Studio server')


    def stop(self):
        # Stop the Label Studio server
        self.label_studio_thread.stop_server()
        self.label_studio_thread.stop()
        self.stop_button.setEnabled(False)
        self.login_button.setEnabled(True)
        self.webview.setUrl(QUrl(''))

    def on_login(self, success):
        # Handle the login result
        if success:
            print('Opening Label Studio homepage...')
            self.login_button.setEnabled(False)

            # Load the Label Studio homepage in the QWebEngineView widget
            url = QUrl(f'{LABEL_STUDIO_BASE_URL}/')
            self.webview.setUrl(url)
        else:
            self.setText('Failed to authenticate with Label Studio API')

    def on_authenticate(self, success):
        # Handle the login result
        if success:
            print('Opening Label Studio Projects...')
            #self.login_button.setEnabled(False)

            # Load the Label Studio homepage in the QWebEngineView widget

            url = QUrl(f'{LABEL_STUDIO_BASE_URL}/api/projects')

            self.webview.load(url)
        else:
            self.setText('Failed to authenticate with Label Studio API')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())