from PyQt5.QtCore import pyqtSignal, QObject, QThread, QUrl
from .label_studio_base_url import * 
import requests 


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
    
    def export_yolo_annotation(self):
        if self.authenticated_signal:
        # Make API call to export annotations in zip format
            project_id = 13
            auth_token = token
            export_type = "JSON"
            export_url = f"https://localhost:8080/api/projects/{project_id}/export?exportType={export_type}"
            headers = {
                "Authorization": f"Token {auth_token}"
            }

            response = requests.get(export_url, headers=headers)

            print(response)



