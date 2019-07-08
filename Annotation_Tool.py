# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Annotation_Tool.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMessageBox

import pprint
import os
import webbrowser

from JSONGenerator import JSONGenerator
from Images_Dialog import ImagesDialog, Ui_imagesDialog
from Split_Dialog import SplitDialog, Ui_splitDialog
from Masks_Dialog import MasksDialog, Ui_masksDialog

class ScaledLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self)
        self._pixmap = QPixmap(self.pixmap())

    def resizeEvent(self, event):
        self.setPixmap(self._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.mainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_3.addWidget(self.pushButton_7)
        self.pushButton_9 = QtWidgets.QPushButton(self.tab)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout_3.addWidget(self.pushButton_9)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setEnabled(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setEnabled(False)
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.imageLabel = QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayout_4.addWidget(self.imageLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_3.addWidget(self.pushButton_8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_3, "")
        
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.imagesDialog = ImagesDialog(MainWindow)

        self.json_generator = JSONGenerator()
        self.via_style = False
        self.image_paths = []
        self.mask_paths = []
        self.current_image_path = ''
        self.current_mask_path = ''

        self.splitDialog = SplitDialog(MainWindow)

        self.masksDialog = MasksDialog(MainWindow)

        ##connect signals
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.pushButton_2.clicked.connect(self.pushButton2_clicked)
        self.pushButton_3.clicked.connect(self.pushButton3_clicked)
        self.pushButton_4.clicked.connect(self.pushButton4_clicked)

        self.imagesDialog.openImagesTabSignal.connect(self.collectImageMaskPairs)
        self.imagesDialog.processAllImages.connect(self.processAllImages)

        self.pushButton_5.clicked.connect(self.pushButton5_clicked)
        self.pushButton_6.clicked.connect(self.pushButton6_clicked)
        self.pushButton_8.clicked.connect(self.pushButton8_clicked)

        self.pushButton_7.clicked.connect(self.pushButton7_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Annotation Tool"))
        self.pushButton_2.setText(_translate("MainWindow", "Edit Annotations"))
        self.pushButton_4.setText(_translate("MainWindow", "Generate JSON for VIA"))
        self.pushButton.setText(_translate("MainWindow", "Generate JSON for training"))
        self.pushButton_3.setText(_translate("MainWindow", "Split Dataset"))
        self.pushButton_7.setText(_translate("MainWindow", "Generate Masks"))
        self.pushButton_9.setText(_translate("MainWindow", "Convert/Combine annotation files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "JSON Editor"))
        self.pushButton_6.setText(_translate("MainWindow", "Accept"))
        self.pushButton_5.setText(_translate("MainWindow", "Reject"))
        self.pushButton_8.setText(_translate("MainWindow", "Cancel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Image/Mask"))

    def pushButton2_clicked(self): ##Open VIA and load annotations
        webbrowser.open_new_tab("file://" + os.path.abspath("via-master/via-2.x.y/src/index.html"))

    def pushButton7_clicked(self): ##Generate Masks
        self.masksDialog = MasksDialog(self.mainWindow)
        ui_masksDialog = Ui_masksDialog()
        ui_masksDialog.setupUi(self.masksDialog)
        self.masksDialog.exec_()
        
    def pushButton3_clicked(self): ##Split dataset
        self.splitDialog = SplitDialog(self.mainWindow)
        ui_splitDialog = Ui_splitDialog()
        ui_splitDialog.setupUi(self.splitDialog)
        self.splitDialog.exec_()

    def pushButton_clicked(self): ##Generate JSON for training
        self.textEdit.clear()
        self.via_style = False
        self.json_generator.clear_annotations()

        self.imagesDialog = ImagesDialog(self.mainWindow)
        ui_imagesDialog = Ui_imagesDialog()
        ui_imagesDialog.setupUi(self.imagesDialog)
        self.imagesDialog.exec_()

    def pushButton4_clicked(self): ##Generate JSON for VIA
        self.textEdit.clear()
        self.via_style = True
        self.json_generator.clear_annotations()

        self.imagesDialog = ImagesDialog(self.mainWindow)
        ui_imagesDialog = Ui_imagesDialog()
        ui_imagesDialog.setupUi(self.imagesDialog)
        self.imagesDialog.exec_()

    def pushButton5_clicked(self): ##Reject
        annotations = None
        annotations = self.json_generator.generate_rejected_contour_data(self.current_image_path, self.current_mask_path, self.via_style)
        if annotations is not None:
            self.textEdit.setText(pprint.pformat(annotations, indent=4))
        else:
            self.textEdit.setText('ERROR: No JSON generated!')
        self._displayImageMaskPair()       

    def pushButton6_clicked(self): ##Accept
        self.json_generator.generate_accepted_contour_data(self.current_image_path, self.current_mask_path, self.via_style) 
        self._displayImageMaskPair()

    def pushButton8_clicked(self): ##Cancel
        self.imageLabel.clear()
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setCurrentIndex(0)

        annotations = None
        annotations = self.json_generator.save_annotations(self.via_style)
        if annotations is not None:
            self.textEdit.setText(pprint.pformat(annotations, indent=4))
            os.system("xdg-open '%s'" % self.imagesDialog.images_directory)
        else:
            self.textEdit.setText('ERROR: No JSON generated!')

    def collectImageMaskPairs(self):
        if not self.json_generator.set_directories(self.imagesDialog.images_directory, self.imagesDialog.masks_directory, self.imagesDialog.annotations_file):
            QMessageBox.information(self.mainWindow, "Annotations", "The section '_via_img_metadata' was not found in the annotations file %s."%self.mainWindow.annotations_file)
        
        self.image_paths, self.mask_paths = self.json_generator.load_paths()
        print(len(self.image_paths), len(self.mask_paths))

        if len(self.image_paths) > 0 and len(self.mask_paths) > 0:
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(1, True) ##Tab for displaying images
            self._displayImageMaskPair()
        else:
            if self.imagesDialog.is_ongoing_project():
                QMessageBox.information(self.mainWindow, "Images", "No new images with corresponding masks in %s were found in %s."%(self.imagesDialog.masks_directory, self.imagesDialog.images_directory))
            else:
                QMessageBox.information(self.mainWindow, "Images", "No images with corresponding masks in %s were found in %s."%(self.imagesDialog.masks_directory, self.imagesDialog.images_directory))

    def _displayImageMaskPair(self):
        if len(self.image_paths) > 0 and len(self.mask_paths) > 0:
            self.current_image_path = self.image_paths.pop(0)
            self.current_mask_path = self.mask_paths.pop(0)
            print(self.current_image_path, self.current_mask_path)

            display = self.json_generator.generate_display_image(self.current_image_path, self.current_mask_path)

            if display is not None:
                self.imageLabel.setPixmap(QPixmap(display).scaled(self.imageLabel.width(), self.imageLabel.height(), QtCore.Qt.KeepAspectRatio))
            else:
                QMessageBox.information(self.mainWindow, "Images", "Either image %s or corresponding mask %s was not found."%(self.current_image_path, self.current_mask_path))
                    
        else:
            self.imageLabel.clear()
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setCurrentIndex(0)

            # webbrowser.open_new_tab("file://" + os.path.abspath("via-master/via-2.x.y/src/index.html"))

    def processAllImages(self):
        self.textEdit.setText('Processing all images in %s.....'%self.imagesDialog.images_directory)
        annotations = None

        if not self.json_generator.set_directories(self.imagesDialog.images_directory, self.imagesDialog.masks_directory, self.imagesDialog.annotations_file):
            QMessageBox.information(self.mainWindow, "Annotations", "The section '_via_img_metadata' was not found in the annotations file %s."%self.imagesDialog.annotations_file)

        self.image_paths, self.mask_paths = self.json_generator.load_paths()
 
        annotations = self.json_generator.generate_JSON(self.via_style)
        
        if len(self.image_paths) == 0 or len(self.mask_paths) == 0:
            if self.imagesDialog.is_ongoing_project():
                QMessageBox.information(self.mainWindow, "Images", "No new images with corresponding masks in %s were found in %s."%(self.imagesDialog.masks_directory, self.imagesDialog.images_directory))
            else:
                QMessageBox.information(self.mainWindow, "Images", "No images with corresponding masks in %s were found in %s."%(self.imagesDialog.masks_directory, self.imagesDialog.images_directory))

        if annotations is not None:
            self.textEdit.setText(pprint.pformat(annotations, indent=4))
            os.system("xdg-open '%s'" % self.imagesDialog.images_directory)
        else:
            self.textEdit.setText('ERROR: No JSON generated!')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
