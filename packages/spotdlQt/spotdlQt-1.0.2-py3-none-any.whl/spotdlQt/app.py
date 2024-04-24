#!/usr/bin/env python3

import os
import sys
import subprocess
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QFileDialog,
)
from PyQt6.QtCore import QThread, pyqtSignal


class SpotDLWrapper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.downloader_thread = None  # Keep track of the downloader thread
        self.download_folder = None

        self.setWindowTitle("SpotDL Wrapper")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.setWindowIcon(QIcon("icon.svg"))
        self.input_label = QLabel("Enter Spotify URL or Song Name:")
        self.layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.download_song)
        self.layout.addWidget(self.input_field)

        self.download_folder_button = QPushButton("Choose Download Folder")
        self.download_folder_button.clicked.connect(self.choose_download_folder)
        self.layout.addWidget(self.download_folder_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_song)
        self.layout.addWidget(self.download_button)

        self.output_textbox = QPlainTextEdit()
        self.output_textbox.setReadOnly(True)
        self.layout.addWidget(self.output_textbox)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def download_song(self):
        if len(self.input_field.text()) == 0:
            return  # dont start if no string provided
        if self.downloader_thread and self.downloader_thread.isRunning():
            return  # Don't start a new thread if one is already running
        self.download_button.setDisabled(True)
        self.download_button.setText("Downloading...")
        user_input = self.input_field.text()
        self.downloader_thread = SpotDLDownloader(
            self, user_input, self.download_folder
        )
        self.downloader_thread.output_signal.connect(self.update_output)
        self.downloader_thread.finished.connect(
            self.downloader_finished
        )  # Connect the finished signal
        self.downloader_thread.start()

    def update_output(self, output):
        self.output_textbox.appendPlainText(output)

    def downloader_finished(self):
        self.downloader_thread.deleteLater()  # Clean up the thread object
        self.download_button.setText("Download")
        self.download_button.setDisabled(False)
        self.downloader_thread = None

    def choose_download_folder(self):
        options = QFileDialog().options().ShowDirsOnly
        new_download_folder = QFileDialog().getExistingDirectory(
            self, "Choose Download Folder", options=options
        )
        if new_download_folder:
            self.update_output(f"Download folder selected: {new_download_folder}")
            self.download_folder = new_download_folder

    def closeEvent(self, event):
        self.download_button.setDisabled(True)
        self.setWindowTitle("Closing...")
        if self.downloader_thread:
            if self.downloader_thread.isRunning():
                self.setWindowTitle("Waiting for subprocess to finish...")
                # Stop the download and subprocess if running
                self.downloader_thread.stop_download()
                self.downloader_thread.wait()  # Wait for the thread to finish before closing
            self.downloader_thread.deleteLater()
        event.accept()


class SpotDLDownloader(QThread):
    output_signal = pyqtSignal(str)
    custom_message = pyqtSignal(str)

    def __init__(self, spotdl_app, user_input, download_folder):
        super().__init__()
        self.user_input = user_input
        self.download_folder = download_folder
        self.process = None  # Store a reference to the subprocess
        self.custom_message.connect(spotdl_app.update_output)

    def run(self):
        self.custom_message.emit("Starting download...")
        try:
            if self.download_folder:
                os.chdir(self.download_folder)
            self.process = subprocess.Popen(
                ["spotdl", self.user_input],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            for line in self.process.stdout:
                self.output_signal.emit(line)
                if self.isInterruptionRequested():
                    self.stop_download()
                    break
            self.process.wait()
            self.custom_message.emit("Done.")
        except subprocess.CalledProcessError as e:
            self.output_signal.emit(f"Error: {e.output}")

    def stop_download(self):
        if self.process:
            self.custom_message.emit("Closing...")
            self.process.terminate()


def main():
    app = QApplication(sys.argv)
    spotdl_app = SpotDLWrapper()
    spotdl_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
