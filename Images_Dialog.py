# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Images_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLineEdit, QFileDialog, QMessageBox

import os

class ImagesDialog(QDialog):
    openImagesTabSignal = pyqtSignal()
    processAllImages = pyqtSignal()

    def __init__(self, parent):
        super(ImagesDialog, self).__init__(parent)
        self.pick_images = False
        self.resume_project = False

        self.images_directory = ''
        self.masks_directory = ''
        self.annotations_file = ''
        self.last_directory = os.path.expanduser("~")

    def accept(self):
        if len(self.images_directory) == 0 or len(self.masks_directory) == 0:
            if len(self.images_directory) == 0:
                QMessageBox.information(self, "Images", "Set Images Folder!")
            elif len(self.masks_directory) == 0:
                QMessageBox.information(self, "Masks", "Set Masks Folder!")

        elif self.resume_project and len(self.annotations_file) == 0:
            QMessageBox.information(self, "Annotations", "Set Annotations File!")

        else:
            if self.pick_images:
                self.openImagesTabSignal.emit()
            else:
                self.processAllImages.emit()

            super(ImagesDialog, self).accept()

    def set_pick_images(self, value):
        self.pick_images = value

    def is_ongoing_project(self):
        return self.resume_project

class Ui_imagesDialog(object):
    def setupUi(self, imagesDialog):
        imagesDialog.setObjectName("imagesDialog")
        imagesDialog.setWindowModality(QtCore.Qt.WindowModal)
        imagesDialog.resize(423, 337)
        self.dialogBox = imagesDialog
        self.buttonBox = QtWidgets.QDialogButtonBox(imagesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(imagesDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 10, 140, 54))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setChecked(True)
        self.verticalLayout.addWidget(self.radioButton_2)
        self.layoutWidget1 = QtWidgets.QWidget(imagesDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(80, 80, 242, 62))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.checkBox = QtWidgets.QCheckBox(imagesDialog)
        self.checkBox.setGeometry(QtCore.QRect(100, 150, 201, 23))
        self.checkBox.setObjectName("checkBox")
        self.groupBox = QtWidgets.QGroupBox(imagesDialog)
        self.groupBox.setGeometry(QtCore.QRect(60, 170, 286, 71))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(13, 33, 112, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(131, 33, 142, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.groupBox.hide()

        self.retranslateUi(imagesDialog)
        self.buttonBox.accepted.connect(imagesDialog.accept)
        self.buttonBox.rejected.connect(imagesDialog.reject)
        self.radioButton.toggled.connect(self.radioButton_toggled)
        self.radioButton_2.toggled.connect(self.radioButton2_toggled)
        self.checkBox.stateChanged.connect(self.checkBox_clicked)
        QtCore.QMetaObject.connectSlotsByName(imagesDialog)

        self.lineEdit.mouseReleaseEvent = self.lineEdit_clicked
        self.lineEdit_2.mouseReleaseEvent = self.lineEdit2_clicked
        self.lineEdit_3.mouseReleaseEvent = self.lineEdit3_clicked

        self.checkBox.setChecked(False)

    def retranslateUi(self, imagesDialog):
        _translate = QtCore.QCoreApplication.translate
        imagesDialog.setWindowTitle(_translate("imagesDialog", "Images Dialog"))
        self.radioButton.setText(_translate("imagesDialog", "Pick images"))
        self.radioButton_2.setText(_translate("imagesDialog", "Select all images"))
        self.label.setText(_translate("imagesDialog", "Image Folder"))
        self.lineEdit.setToolTip(_translate("imagesDialog", "Enter the path of the folder that contains the images"))
        self.label_2.setText(_translate("imagesDialog", "Mask Folder"))
        self.lineEdit_2.setToolTip(_translate("imagesDialog", "Enter the folder that contains the masks. The masks should contain the corresponding images name in their names."))
        self.checkBox.setText(_translate("imagesDialog", "Resume previous project?"))
        self.label_3.setText(_translate("imagesDialog", "Annotations File"))
        self.lineEdit_3.setToolTip(_translate("imagesDialog", "Set the path to the annotation file. The annotation file must be in VIA format, i.e., contain [\'_via_img_metadata\'] and details about all the files in the images folder. "))

    def radioButton_toggled(self):
        if self.radioButton.isChecked():
            self.dialogBox.set_pick_images(True)

    def radioButton2_toggled(self):
        if self.radioButton_2.isChecked():
            self.dialogBox.set_pick_images(False)

    def checkBox_clicked(self):
        if self.checkBox.isChecked():
            self.dialogBox.resume_project = True
            self.groupBox.show()
        else:
            self.dialogBox.resume_project = False
            self.groupBox.hide()

    def lineEdit_clicked(self, event):
        input_dir = QFileDialog.getExistingDirectory(self.dialogBox, 'Select a folder:', self.dialogBox.last_directory)
        if len(input_dir) > 0:
            if os.path.isdir(input_dir):
                self.dialogBox.images_directory = input_dir
                self.dialogBox.last_directory = input_dir
        self.lineEdit.setText(self.dialogBox.images_directory)

    def lineEdit2_clicked(self, event):
        input_dir = QFileDialog.getExistingDirectory(self.dialogBox, 'Select a folder:', self.dialogBox.last_directory)
        if len(input_dir) > 0:
            if os.path.isdir(input_dir):
                self.dialogBox.masks_directory = input_dir
                self.dialogBox.last_directory = input_dir
        self.lineEdit_2.setText(self.dialogBox.masks_directory)

    def lineEdit3_clicked(self, event):
        input_file, _ = QFileDialog.getOpenFileName(self.dialogBox, 'Select JSON file:', self.dialogBox.last_directory, "JSON files (*.json)")
        if len(input_file) > 0:
            path = os.path.abspath(input_file)
            if os.path.isfile(path):
                self.dialogBox.annotations_file = path
                self.dialogBox.last_directory = path[:path.rfind(os.path.sep)]
        self.lineEdit_3.setText(self.dialogBox.annotations_file)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    imagesDialog = QtWidgets.QDialog()
    ui = Ui_imagesDialog()
    ui.setupUi(imagesDialog)
    imagesDialog.show()
    sys.exit(app.exec_())
