import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from app.gui import AudioprepGUI

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Roboto", 12))
    window = AudioprepGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


"""
    Audioprep/
|-- app/
|   |-- __init__.py
|   |-- convert.py
|   |-- analyze.py
|   |-- segment.py
|   |-- gui.py
|-- main.py
|-- requirements.txt

    :return:
"""


