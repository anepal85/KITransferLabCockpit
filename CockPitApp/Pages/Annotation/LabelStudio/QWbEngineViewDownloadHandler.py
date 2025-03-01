from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QUrl, QFileInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class MyWebEngineView(QWebEngineView):
    """
        Customized web engine view with download handling.

        This class extends QWebEngineView and provides a customized view that handles download requests.
        When a download is requested, it sets the download path and file name and handles different MIME types.

        """
    def __init__(self):
        super().__init__()
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handleDownload)
    
    @QtCore.pyqtSlot("QWebEngineDownloadItem*") 
    def handleDownload(self, downloadItem):
        """
        Handle the download request.

        This method is called when a download is requested. It sets the download path and file name
        based on the suggested file name and extension. It also checks the MIME type of the download
        and accepts or rejects the download accordingly.

        :param downloadItem: The download item.
        :return: None
        """
        # Get the suggested file name and extension
        fileName = QUrl(downloadItem.url()).fileName()
        fileInfo = QFileInfo(fileName)
        suggestedFileName = fileInfo.baseName()

        # Set the download path and file name
        downloadPath = r'./Data/YOLOv8/data' + '/' + suggestedFileName + '.zip' 
        
        downloadItem.setPath(downloadPath)


        # Check the MIME type of the download
        mimeType = downloadItem.mimeType()

        print(f'YoloV8 Format data including images and texts file are downloaded in {downloadPath}')
        
        if mimeType == 'application/zip':
            downloadItem.accept()
            return
        # Accept the download item to start the download
        else:
            # Call the parent implementation
            super().handleDownload(downloadItem)
        #downloadItem.accept()
