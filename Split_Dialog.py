# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Split_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QFileDialog, QMessageBox

import os

from DatasetSplitter import DatasetSplitter

class SplitDialog(QDialog):
    def __init__(self, parent):
        super(SplitDialog, self).__init__(parent)
        self.images_directory = ''
        self.annotations_file = ''
        self.last_directory = os.path.expanduser("~")
        self.current_directory = ''

        self.train_validation_split = 0.5
        self.splitter = DatasetSplitter()

    def accept(self):
        if len(self.images_directory) == 0 or len(self.annotations_file) == 0:
            if len(self.images_directory) == 0:
                QMessageBox.warning(self, "Images", "Set Images Folder!")
            elif len(self.annotations_file) == 0:
                QMessageBox.warning(self, "Annotations", "Set Annotations File!")

        else:
            self.splitter.reset()
            
            if os.path.isdir(self.images_directory) and os.path.isfile(self.annotations_file):
                split = -2
                split, self.current_directory = self.splitter.split_dataset(self.images_directory, self.annotations_file, self.train_validation_split)

                if split == 0:
                    generated = False
                    generated = self.splitter.generate_annotations(self.annotations_file)

                    if not generated:
                       QMessageBox.information(self, "Annotations", "Annotation files were not generated for train and validation folders. Original annotaion file does not contain the section '_via_img_metadata'."%image_path)
                        
                elif split == -1:
                    QMessageBox.information(self, "Mask", "Image files corresponding to annotations were not found in %s."%self.images_directory)
                elif split == 1:
                    QMessageBox.information(self, "Annotations", "The section '_via_img_metadata' was not found in the annotations file %s."%self.annotations_file)

                os.system("xdg-open '%s'" % self.current_directory)

            else:
                if not os.path.isdir(self.images_directory):
                    QMessageBox.information(self, "Images", "Images Folder %s was not found."%self.images_directory)
                elif not os.path.isfile(self.annotations_file):
                    QMessageBox.information(self, "Annotations", "Annotations file %s was not found."%self.annotations_file)

        super(SplitDialog, self).accept()

class Ui_splitDialog(object):
    def setupUi(self, splitDialog):
        splitDialog.setObjectName("splitDialog")
        splitDialog.setWindowModality(QtCore.Qt.WindowModal)
        splitDialog.resize(400, 300)
        self.dialogBox = splitDialog
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(splitDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(splitDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(splitDialog)
        self.spinBox.setMinimum(50)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(splitDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit = QLineEdit(splitDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(splitDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_3 = QLineEdit(splitDialog)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(splitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(splitDialog)
        self.buttonBox.accepted.connect(splitDialog.accept)
        self.buttonBox.rejected.connect(splitDialog.reject)
        self.spinBox.valueChanged.connect(self.spinBox_valueChanged)
        QtCore.QMetaObject.connectSlotsByName(splitDialog)

        self.lineEdit.mouseReleaseEvent = self.lineEdit_clicked
        self.lineEdit_3.mouseReleaseEvent = self.lineEdit3_clicked

    def retranslateUi(self, splitDialog):
        _translate = QtCore.QCoreApplication.translate
        splitDialog.setWindowTitle(_translate("splitDialog", "Split"))
        self.label.setText(_translate("splitDialog", "Split"))
        self.spinBox.setToolTip(_translate("splitDialog", "E.g. If you set 60, 60% of the dataset images will go into the train folder and the rest into the val folder."))
        self.label_2.setText(_translate("splitDialog", "Images Folder"))
        self.lineEdit.setToolTip(_translate("splitDialog", "Set the path to the folder containing the image files that have to be split."))
        self.label_4.setText(_translate("splitDialog", "Annotation File"))
        self.lineEdit_3.setToolTip(_translate("splitDialog", "Set the path to the annotation file. The annotation file must be in VIA format, i.e., contain [\'_via_img_metadata\'] and details about all the files in the images folder. "))


    def lineEdit_clicked(self, event):
        input_dir = QFileDialog.getExistingDirectory(self.dialogBox, 'Select a folder:', self.dialogBox.last_directory)
        if len(input_dir) > 0:
            if os.path.isdir(input_dir):
                self.dialogBox.images_directory = input_dir
                self.dialogBox.last_directory = input_dir
        self.lineEdit.setText(self.dialogBox.images_directory)

    def lineEdit3_clicked(self, event):
        input_file, _ = QFileDialog.getOpenFileName(self.dialogBox, 'Select JSON file:', self.dialogBox.last_directory, "JSON files (*.json)")
        if len(input_file) > 0:
            path = os.path.abspath(input_file)
            if os.path.isfile(path):
                self.dialogBox.annotations_file = path
                self.dialogBox.last_directory = path[:path.rfind(os.path.sep)]
        self.lineEdit_3.setText(self.dialogBox.annotations_file)

    def spinBox_valueChanged(self):
        self.dialogBox.train_validation_split = self.spinBox.value() / 100

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    splitDialog = QtWidgets.QDialog()
    ui = Ui_splitDialog()
    ui.setupUi(splitDialog)
    splitDialog.show()
    sys.exit(app.exec_())
