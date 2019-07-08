# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Masks_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QFileDialog, QMessageBox

import os
import cv2

from MaskGenerator import MaskGenerator

class MasksDialog(QDialog):

    showProgressBar = pyqtSignal()
    hideProgressBar = pyqtSignal()
    updateProgressBar = pyqtSignal(int, int)

    def __init__(self, parent):
        super(MasksDialog, self).__init__(parent)
        self.images_directory = ''
        self.weights_file = ''
        self.last_directory = os.path.expanduser("~")

        self.masks_directory = 'masks/'
        self.generator = MaskGenerator()

    def accept(self):
        if len(self.images_directory) == 0 or len(self.weights_file) == 0:
            if len(self.images_directory) == 0:
                QMessageBox.information(self, "Images", "Set Images Folder!")
            elif len(self.weights_file) == 0:
                QMessageBox.information(self, "Weights", "Set Weights File!")

        else:
            self.generator.reset()
            self.showProgressBar.emit()
            
            self.masks_directory = self.generator.set_masks_directory(self.images_directory)

            if os.path.isfile(self.weights_file):
                self.generator.load_weights(self.weights_file)
            else:
                QMessageBox.information(self, "Weights", "Weights file %s was not found."%self.weights_file)

            if os.path.isdir(self.images_directory):
                mask_instances = 0
                images_processed = 0

                images = os.listdir(self.images_directory)
                total_images = len(images)

                for filename in images:
                    image_path = os.path.join(self.images_directory, filename)
                    if os.path.isfile(image_path):
                        mask_generated = False
                        image = cv2.imread(image_path)
                        if image is not None:
                            mask_generated = self.generator.generate_mask(image, filename)

                        images_processed += 1
                        self.updateProgressBar.emit(images_processed, total_images)

                        if mask_generated:
                            mask_instances += 1
                        else:
                            QMessageBox.information(self, "Mask", "Mask was not generated for %s. The file could not be opened."%image_path)
            else:
                QMessageBox.information(self, "Images", "Images Folder %s was not found."%self.images_directory)

            if mask_instances > 0:
                os.system("xdg-open '%s'" % self.masks_directory)

            self.hideProgressBar.emit()

            super(MasksDialog, self).accept()

class Ui_masksDialog(object):
    def setupUi(self, masksDialog):
        masksDialog.setObjectName("masksDialog")
        masksDialog.setWindowModality(QtCore.Qt.WindowModal)
        masksDialog.resize(400, 300)
        self.dialogBox = masksDialog
        self.buttonBox = QtWidgets.QDialogButtonBox(masksDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(masksDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 40, 264, 62))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.progressBar = QtWidgets.QProgressBar(masksDialog)
        self.progressBar.setGeometry(QtCore.QRect(27, 130, 341, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()

        self.retranslateUi(masksDialog)
        self.buttonBox.accepted.connect(masksDialog.accept)
        self.buttonBox.rejected.connect(masksDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(masksDialog)

        self.lineEdit.mouseReleaseEvent = self.lineEdit_clicked
        self.lineEdit_2.mouseReleaseEvent = self.lineEdit2_clicked

        self.dialogBox.showProgressBar.connect(self.progressBar.show)
        self.dialogBox.hideProgressBar.connect(self.progressBar.hide)
        self.dialogBox.updateProgressBar.connect(self.progressBar_update)

    def retranslateUi(self, masksDialog):
        _translate = QtCore.QCoreApplication.translate
        masksDialog.setWindowTitle(_translate("masksDialog", "Dialog"))
        self.label.setText(_translate("masksDialog", "Images Folder"))
        self.label_2.setText(_translate("masksDialog", "Weights File"))
        self.lineEdit.setToolTip(_translate("imagesDialog", "Enter the path of the folder that contains the images"))
        self.lineEdit_2.setToolTip(_translate("imagesDialog", "Set the path to the weights file for Mask-RCNN."))

    def lineEdit_clicked(self, event):
        input_dir = QFileDialog.getExistingDirectory(self.dialogBox, 'Select a folder:', self.dialogBox.last_directory)
        if len(input_dir) > 0:
            if os.path.isdir(input_dir):
                self.dialogBox.images_directory = input_dir
                self.dialogBox.last_directory = input_dir
        self.lineEdit.setText(self.dialogBox.images_directory)

    def lineEdit2_clicked(self, event):
        input_file, _ = QFileDialog.getOpenFileName(self.dialogBox, 'Select weights file:', self.dialogBox.last_directory)
        if len(input_file) > 0:
            path = os.path.abspath(input_file)
            if os.path.isfile(path):
                self.dialogBox.weights_file = path
                self.dialogBox.last_directory = path[:path.rfind(os.path.sep)]
        self.lineEdit_2.setText(self.dialogBox.weights_file)

    def progressBar_update(self, current_value, maximum_value):
        self.progressBar.setValue(current_value // maximum_value)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    masksDialog = QtWidgets.QDialog()
    ui = Ui_masksDialog()
    ui.setupUi(masksDialog)
    masksDialog.show()
    sys.exit(app.exec_())
