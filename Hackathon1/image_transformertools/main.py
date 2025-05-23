import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from gui import Ui_MainWindow
from logic import ImageProcessor
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.processor = ImageProcessor()

        # Initialize current_transform early to prevent AttributeError
        self.current_transform = self.ui.convertComboBox.currentText()

        # Set initial slider values without triggering slots
        self.ui.brightnesshorizontalSlider.blockSignals(True)
        self.ui.brightnesshorizontalSlider.setValue(50)
        self.ui.brightnesshorizontalSlider.blockSignals(False)

        self.ui.contrasthorizontalSlider.blockSignals(True)
        self.ui.contrasthorizontalSlider.setValue(50)
        self.ui.contrasthorizontalSlider.blockSignals(False)

        # Connect buttons
        self.ui.uploaButton.clicked.connect(self.load_image)
        self.ui.saveButton.clicked.connect(self.save_image)

        # Connect combo box
        self.ui.convertComboBox.currentTextChanged.connect(self.on_transform_change)

        # Connect sliders
        self.ui.brightnesshorizontalSlider.valueChanged.connect(self.on_brightness_change)
        self.ui.contrasthorizontalSlider.valueChanged.connect(self.on_contrast_change)

        # Set slider state based on initial transform
        self.update_slider_states()

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            if self.processor.load_image(path):
                self.display_image()
            else:
                QMessageBox.warning(self, "Error", "Failed to load image")

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg)")
        if path:
            if not self.processor.save_image(path):
                QMessageBox.warning(self, "Error", "Failed to save image")

    def display_image(self):
        img = self.processor.get_display_image()
        if img is not None:
            h, w, ch = img.shape
            bytes_per_line = ch * w
            qt_img = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(qt_img)
            self.ui.lblImage.setPixmap(pix.scaled(self.ui.lblImage.size(), QtCore.Qt.KeepAspectRatio))

    def update_slider_states(self):
        self.ui.brightnesshorizontalSlider.setEnabled(self.current_transform == "Brightness")
        self.ui.contrasthorizontalSlider.setEnabled(self.current_transform == "Contrast")

    def on_transform_change(self, text):
        self.current_transform = text
        self.update_slider_states()

        if text not in ["Brightness", "Contrast"]:
            # Reset sliders to default
            self.ui.brightnesshorizontalSlider.setValue(50)
            self.ui.contrasthorizontalSlider.setValue(50)

            # Apply transformation with default parameter
            self.processor.apply_transformation(text, 5)  # Pass default param like 5
            self.display_image()

    def on_brightness_change(self, val):
        if self.current_transform == "Brightness":
            self.processor.apply_transformation("Brightness", val)
            self.display_image()

    def on_contrast_change(self, val):
        if self.current_transform == "Contrast":
            self.processor.apply_transformation("Contrast", val)
            self.display_image()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
