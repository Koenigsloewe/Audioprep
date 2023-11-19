import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout, \
    QLineEdit, QPushButton, QProgressBar, QSpacerItem, QFileDialog, QMessageBox

from convert import Conversion

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

        self.progression_label = QLabel("bla bla")
        centralwidget_layout.addWidget(self.progression_label, 7, 1, 1, 1, alignment=Qt.AlignCenter)

        centralwidget_layout.addItem(QSpacerItem(60, 60), 8, 1)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setFixedHeight(35)
        centralwidget_layout.addWidget(self.open_folder_btn, 9, 0, 1, 3)

        with open("resources/styles.qss", "r") as qss_file:
            style_sheet = qss_file.read()
            self.setStyleSheet(style_sheet)

        self.start_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)

        self.input_line_edit.textChanged.connect(self.check_filled)
        self.output_line_edit.textChanged.connect(self.check_filled)
        self.input_open_dir_btn.clicked.connect(lambda: self.open_path("mp3", self.input_line_edit))
        self.output_open_dir_btn.clicked.connect(lambda: self.open_path("dir", self.output_line_edit))
        self.start_btn.clicked.connect(lambda: self.start_progress())

    def check_filled(self):
        input_path = self.input_line_edit.text().strip()
        output_path = self.output_line_edit.text().strip()

        if input_path and output_path:
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)

    def open_path(self, file_type, line_edit):
        if file_type == "mp3":
            file_dialog = QFileDialog()
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

        if os.path.isfile(input_path) and os.path.isdir(output_path):
            print("")
        elif not os.path.isfile(input_path):
            self.raise_error("Your MP3 file does not exist!")
        elif not os.path.isdir(output_path):
            self.raise_error("Your directory does not exist!")

    def raise_error(self, text):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(text)
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()