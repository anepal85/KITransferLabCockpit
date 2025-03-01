import subprocess
from PyQt5.QtCore import QThread
import platform 

class LabelStudioThread(QThread):
    """
        Thread for running the Label Studio server.

        This class extends QThread and provides a thread for running the Label Studio server.
        It starts the server using the `label-studio` command and stops it by sending a SIGINT signal.
        The project directory can be optionally provided.

        :param parent: The parent object.
        :param project_dir: The project directory (optional).
        """
    def __init__(self, parent=None, project_dir=None):
        super().__init__(parent)

    def run(self):
        # Start the Label Studio server using the `label-studio` command and pass the project directory as an argument
        command = ["label-studio", "start", "--no-browser"]
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