# pyqt_test/pyqt6_test.py 

import os
import sys
from image_filters import applyAndShowFilter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, 
    QComboBox,
    QFileDialog, 
    QGridLayout,
    QLabel,
    QMainWindow,
    QWidget
    )

selected_files = []

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.filtered_buf = None
        self.setWindowTitle("Image Filter Application")
        self._createMenu()
        self._createWindow()
        self.showMaximized()

    def _createMenu(self):
        file = self.menuBar().addMenu("File")
        open_action = file.addAction("Open", lambda: openFileDialog(self))
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        save_action = file.addAction("Save", lambda: saveFileDialog(self))
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        exit_action = file.addAction("Exit", self.close)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        edit = self.menuBar().addMenu("Edit")
        edit.addAction("Undo", lambda: print("Undo Action"))
        edit.addAction("Redo", lambda: print("Redo Action")) 

    def _createWindow(self):
        self.central_widget = QWidget()
        self.layout = QGridLayout()
        self.image_label = QLabel("Open an image by clicking 'File -> Open'")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label, 0, 0, 1, 3)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def _createFilterCombo(self, selected_files):
        filter_types = [
            "none", 
            "grayscale", 
            "sepia", 
            "invert", 
            "blur", 
            "sharpen",
            "cartoon",
            "emboss",
            "edge_enhance",
            ]
        filter_label = QLabel("Select Filter:")
        filter_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(filter_label, 1, 0, 1, 1)
        filter_combo = QComboBox()
        filter_combo.addItems([ft.capitalize() for ft in filter_types])
        self.layout.addWidget(filter_combo, 1, 1, 1, 2)
        
        def on_filter_selected(index):
            filter_type = filter_types[index]
            storeFilteredBuf(self, filter_type, selected_files[0])

        filter_combo.currentIndexChanged.connect(on_filter_selected)

def showSelectedFiles(self,selected_files):
    if selected_files:
        pixmap = QPixmap(selected_files[0])
        self.image_label.setPixmap(pixmap)
        self._createFilterCombo(selected_files)

def openFileDialog(self):
    dialog = QFileDialog(self)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dialog.setDirectory(os.path.expanduser("~"))
    dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
    if dialog.exec():
        selected_files = dialog.selectedFiles()
        print("Selected files:", selected_files)
        showSelectedFiles(self, selected_files)

def saveFileDialog(self):
    dialog = QFileDialog(self)
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
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
    if filter_type == "none":
        self.filtered_buf = None
        self.image_label.setPixmap(QPixmap(image_path))
        return
    from image_filters import applyAndShowFilter
    self.filtered_buf = applyAndShowFilter(self, filter_type, image_path)

if __name__ == "__main__":
    app = QApplication([])      
    window = Window()
    window.show()
    sys.exit(app.exec())