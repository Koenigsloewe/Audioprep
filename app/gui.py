import os
import time

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, \
    QLineEdit, QPushButton, QProgressBar, QSpacerItem, QFileDialog, QMessageBox

from .convert import Conversion
from .analyze import Analysis
from .segment import Segment
from .stylesheet import load_stylesheet


class AudioProcessingThread(QThread):
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, input_path, output_path, file_name):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.file_name = file_name

    def run(self):
        try:

            convert = Conversion()
            convert.convert_to_audio(self.input_path, self.output_path, self.file_name, "wav")
            output_file_path = convert.get_output_file_path(self.output_path, self.file_name)

            self.progress_updated.emit(33)

            analyse = Analysis(1, -50)
            analyse.analyse_audio(output_file_path)

            self.progress_updated.emit(66)

            segment = Segment()
            segment.segment(output_file_path, self.output_path)
            convert.delete_processing_audio_file(output_file_path)

            self.progress_updated.emit(100)

            self.finished.emit()

        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            self.error_occurred.emit(error_message)


class AudioprepGUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Audioprep")
        self.setFixedSize(720, 720)
        self.setWindowIcon(QIcon("resources/icons/audioprep2.ico"))

        centralwidget = QWidget()
        centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(centralwidget)

        centralwidget_layout = QGridLayout(centralwidget)
        centralwidget_layout.setContentsMargins(30, 30, 30, 60)
        centralwidget_layout.setSpacing(30)

        logo_pixmap = QPixmap("resources/audioprep_logo.png").scaledToWidth(350, 1)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        centralwidget_layout.addWidget(logo_label, 0, 1, 1, 1, alignment=Qt.AlignCenter)

        input_label = QLabel("Input Path")
        centralwidget_layout.addWidget(input_label, 1, 0)

        self.input_line_edit = QLineEdit()
        centralwidget_layout.addWidget(self.input_line_edit, 1, 1)

        self.input_open_dir_btn = QPushButton()
        self.input_open_dir_btn.setFixedSize(30, 30)
        self.input_open_dir_btn.setObjectName("open_folder_btn")
        self.input_open_dir_btn.setIcon(QIcon(QPixmap("resources/svg/folder.svg")))
        centralwidget_layout.addWidget(self.input_open_dir_btn, 1, 2)

        output_label = QLabel("Output Path")
        centralwidget_layout.addWidget(output_label, 2, 0)

        self.output_line_edit = QLineEdit()
        centralwidget_layout.addWidget(self.output_line_edit, 2, 1)

        self.output_open_dir_btn = QPushButton()
        self.output_open_dir_btn.setFixedSize(30, 30)
        self.output_open_dir_btn.setObjectName("open_folder_btn")
        self.output_open_dir_btn.setIcon(QIcon(QPixmap("resources/svg/folder.svg")))
        centralwidget_layout.addWidget(self.output_open_dir_btn, 2, 2)

        centralwidget_layout.addItem(QSpacerItem(60, 60), 3, 1)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedHeight(35)
        centralwidget_layout.addWidget(self.start_btn, 4, 0, 1, 3)

        centralwidget_layout.addItem(QSpacerItem(90, 90), 5, 1)

        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(False)
        centralwidget_layout.addWidget(self.progressbar, 6, 0, 1, 3)

        self.progression_label = QLabel("Waiting...")
        centralwidget_layout.addWidget(self.progression_label, 7, 1, 1, 1, alignment=Qt.AlignCenter)

        centralwidget_layout.addItem(QSpacerItem(60, 60), 8, 1)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setFixedHeight(35)
        centralwidget_layout.addWidget(self.open_folder_btn, 9, 0, 1, 3)

        self.setStyleSheet(load_stylesheet())

        self.start_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)

        self.input_line_edit.textChanged.connect(self.check_filled)
        self.output_line_edit.textChanged.connect(self.check_filled)
        self.input_open_dir_btn.clicked.connect(lambda: self.open_path("mp3", self.input_line_edit))
        self.output_open_dir_btn.clicked.connect(lambda: self.open_path("dir", self.output_line_edit))
        self.start_btn.clicked.connect(lambda: self.start_progress())
        self.open_folder_btn.clicked.connect(lambda: self.open_dir(self.output_line_edit.text().strip()))

    def check_filled(self):
        input_path = self.input_line_edit.text().strip()
        output_path = self.output_line_edit.text().strip()

        if input_path and output_path:
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)

    def open_path(self, file_type, line_edit):
        root_directory = os.path.abspath(os.sep)

        if file_type == "mp3":
            file_dialog = QFileDialog()
            file_dialog.setDirectory(root_directory)
            file_dialog.setNameFilter("MP3 files (*.mp3)")
            file_dialog.selectNameFilter("MP3 files (*.mp3)")

            if file_dialog.exec_():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    selected_file = selected_files[0]
                    line_edit.setText(selected_file)

        elif file_type == "dir":
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder_path:
                line_edit.setText(folder_path)

    def start_progress(self):
        input_path = self.input_line_edit.text().strip()
        output_path = self.output_line_edit.text().strip()
        filename = os.path.basename(input_path)
        filename = os.path.splitext(filename)[0]

        if os.path.isfile(input_path) and os.path.isdir(output_path):
            self.processing_thread = AudioProcessingThread(input_path, output_path, filename)
            self.processing_thread.finished.connect(self.on_processing_finished)
            self.processing_thread.error_occurred.connect(self.raise_error)
            self.processing_thread.progress_updated.connect(self.update_progress)
            self.processing_thread.start()

        elif not os.path.isfile(input_path):
            self.raise_error("Your MP3 file does not exist!")
        elif not os.path.isdir(output_path):
            self.raise_error("Your directory does not exist!")

    def raise_error(self, text):
        self.progressbar.setValue(0)
        self.progression_label.setText("Waiting...")

        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(text)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

    def update_progress(self, value):
        self.progressbar.setValue(value)
        self.progression_label.setText(f"Progress: {value}%")

    def on_processing_finished(self):
        self.open_folder_btn.setEnabled(True)
        self.progression_label.setText("Process finished!")

    def open_dir(self, output_path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(output_path))
