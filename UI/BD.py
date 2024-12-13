# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BD.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 569)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setMinimumSize(QtCore.QSize(512, 512))
        self.image_label.setMaximumSize(QtCore.QSize(512, 512))
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.verticalLayout_2.addWidget(self.image_label)
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filename_label.setObjectName("filename_label")
        self.verticalLayout_2.addWidget(self.filename_label)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.memory_label = QtWidgets.QLabel(self.centralwidget)
        self.memory_label.setObjectName("memory_label")
        self.verticalLayout.addWidget(self.memory_label)
        self.filter_input = QtWidgets.QLineEdit(self.centralwidget)
        self.filter_input.setObjectName("filter_input")
        self.verticalLayout.addWidget(self.filter_input)
        self.offsets_table = QtWidgets.QTableWidget(self.centralwidget)
        self.offsets_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.offsets_table.setObjectName("offsets_table")
        self.offsets_table.setColumnCount(0)
        self.offsets_table.setRowCount(0)
        self.offsets_table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.offsets_table)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.open_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_button.setObjectName("open_button")
        self.horizontalLayout_3.addWidget(self.open_button)
        self.offsets_button = QtWidgets.QPushButton(self.centralwidget)
        self.offsets_button.setEnabled(False)
        self.offsets_button.setObjectName("offsets_button")
        self.horizontalLayout_3.addWidget(self.offsets_button)
        self.memory_button = QtWidgets.QPushButton(self.centralwidget)
        self.memory_button.setObjectName("memory_button")
        self.horizontalLayout_3.addWidget(self.memory_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.export_button = QtWidgets.QPushButton(self.centralwidget)
        self.export_button.setEnabled(False)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout_4.addWidget(self.export_button)
        self.section_button = QtWidgets.QPushButton(self.centralwidget)
        self.section_button.setEnabled(False)
        self.section_button.setObjectName("section_button")
        self.horizontalLayout_4.addWidget(self.section_button)
        self.patchImage_button = QtWidgets.QPushButton(self.centralwidget)
        self.patchImage_button.setEnabled(False)
        self.patchImage_button.setObjectName("patchImage_button")
        self.horizontalLayout_4.addWidget(self.patchImage_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.special_button = QtWidgets.QPushButton(self.centralwidget)
        self.special_button.setObjectName("special_button")
        self.horizontalLayout_2.addWidget(self.special_button)
        self.folder_button = QtWidgets.QPushButton(self.centralwidget)
        self.folder_button.setObjectName("folder_button")
        self.horizontalLayout_2.addWidget(self.folder_button)
        self.patchSection_button = QtWidgets.QPushButton(self.centralwidget)
        self.patchSection_button.setEnabled(False)
        self.patchSection_button.setObjectName("patchSection_button")
        self.horizontalLayout_2.addWidget(self.patchSection_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.export_list = QtWidgets.QPushButton(self.centralwidget)
        self.export_list.setObjectName("export_list")
        self.verticalLayout.addWidget(self.export_list)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.image_label.setText(_translate("MainWindow", "Pick an offset..."))
        self.filename_label.setText(_translate("MainWindow", "Pick an offset..."))
        self.memory_label.setText(_translate("MainWindow", "Memory Usage: 0MB"))
        self.open_button.setText(_translate("MainWindow", "Open .XAV"))
        self.offsets_button.setText(_translate("MainWindow", "Load Offsets"))
        self.memory_button.setText(_translate("MainWindow", "Refresh Memory"))
        self.export_button.setText(_translate("MainWindow", "Export .PNG"))
        self.section_button.setText(_translate("MainWindow", "Export Section"))
        self.patchImage_button.setText(_translate("MainWindow", "Patch Image"))
        self.special_button.setText(_translate("MainWindow", "Special Extraction"))
        self.folder_button.setText(_translate("MainWindow", "Filter From Folder"))
        self.patchSection_button.setText(_translate("MainWindow", "Patch Section"))
        self.export_list.setText(_translate("MainWindow", "Export List"))
