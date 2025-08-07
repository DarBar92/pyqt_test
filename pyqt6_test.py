# pyqt_test/pyqt6_test.py 

import os
import sys
from image_filters import applyAndShowFilter
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget
    )

selected_files = []

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.filtered_buf = None
        self.setWindowTitle("PyQt6 Test")
        self._createMenu()
        self._createWindow()
        self.showMaximized()

    def _createMenu(self):
        file = self.menuBar().addMenu("File")
        file.addAction("Open", lambda: openFileDialog(self))
        file.addAction("Save", lambda: saveFileDialog(self))
        file.addAction("Exit", self.close)
        edit = self.menuBar().addMenu("Edit")
        edit.addAction("Undo", lambda: print("Undo Action"))
        edit.addAction("Redo", lambda: print("Redo Action")) 

    def _createWindow(self):
        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.image_label = QLabel("No image selected")
        self.layout.addWidget(self.image_label, 0, 0, 1, 3)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def _createButtons(self, selected_files):
        grayscale_button = QPushButton("Grayscale")
        grayscale_button.clicked.connect(lambda: storeFilteredBuf(self, "grayscale", selected_files[0]))
        self.layout.addWidget(grayscale_button, 1, 0)
        sepia_button = QPushButton("Sepia")
        sepia_button.clicked.connect(lambda: storeFilteredBuf(self, "sepia", selected_files[0]))
        self.layout.addWidget(sepia_button, 1, 1)
        invert_button = QPushButton("Invert")
        invert_button.clicked.connect(lambda: storeFilteredBuf(self, "invert", selected_files[0]))
        self.layout.addWidget(invert_button, 1, 2)


def showSelectedFiles(self,selected_files):
    if selected_files:
        pixmap = QPixmap(selected_files[0])
        self.image_label.setPixmap(pixmap)
        self._createButtons(selected_files)

def openFileDialog(self):
    dialog = QFileDialog(self)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dialog.setDirectory(os.path.expanduser("~"))
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilter("JPEG Files (*.jpg *.jpeg)")
    if dialog.exec():
        selected_files = dialog.selectedFiles()
        print("Selected files:", selected_files)
        showSelectedFiles(self, selected_files)

def saveFileDialog(self):
    dialog = QFileDialog(self)
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dialog.setNameFilter("JPEG Files (*.jpg *.jpeg)")
    if dialog.exec():
        selected_files = dialog.selectedFiles()
        print("Selected files for saving:", selected_files)
        if self.filtered_buf:
            with open(selected_files[0], 'wb') as f:
                f.write(self.filtered_buf.getvalue())
            print(f"Filtered image saved to {selected_files[0]}")
        else:
            print("No filtered image to save.")

def storeFilteredBuf(self, filter_type, image_path):
    from image_filters import applyAndShowFilter
    self.filtered_buf = applyAndShowFilter(self, filter_type, image_path)

if __name__ == "__main__":
    app = QApplication([])      
    window = Window()
    window.show()
    sys.exit(app.exec())