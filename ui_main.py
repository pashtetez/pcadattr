# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(985, 595)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_out = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_out.setText("")
        self.lineEdit_out.setObjectName("lineEdit_out")
        self.gridLayout_2.addWidget(self.lineEdit_out, 1, 2, 1, 1)
        self.pushButton_out = QtWidgets.QPushButton(self.tab)
        self.pushButton_out.setObjectName("pushButton_out")
        self.gridLayout_2.addWidget(self.pushButton_out, 1, 1, 1, 1)
        self.pushButton_in = QtWidgets.QPushButton(self.tab)
        self.pushButton_in.setObjectName("pushButton_in")
        self.gridLayout_2.addWidget(self.pushButton_in, 0, 1, 1, 1)
        self.lineEdit_in = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_in.setText("")
        self.lineEdit_in.setObjectName("lineEdit_in")
        self.gridLayout_2.addWidget(self.lineEdit_in, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.frame)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_3.addWidget(self.listWidget, 1, 0, 2, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.frame)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_3.addWidget(self.plainTextEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.padDefTable = QtWidgets.QTableWidget(self.tab_2)
        self.padDefTable.setObjectName("padDefTable")
        self.padDefTable.setColumnCount(0)
        self.padDefTable.setRowCount(0)
        self.gridLayout_5.addWidget(self.padDefTable, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tableView = QtWidgets.QTableView(self.tab_3)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.gridLayout_6.addWidget(self.tableView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.compTable = QtWidgets.QTableWidget(self.tab_4)
        self.compTable.setObjectName("compTable")
        self.compTable.setColumnCount(0)
        self.compTable.setRowCount(0)
        self.gridLayout_7.addWidget(self.compTable, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 985, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pushButton_2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_8.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_8.addWidget(self.pushButton_3, 3, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_8.addWidget(self.comboBox, 0, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_6.setMinimumSize(QtCore.QSize(200, 200))
        self.label_6.setMaximumSize(QtCore.QSize(200, 200))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 1, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_7.setObjectName("label_7")
        self.gridLayout_8.addWidget(self.label_7, 4, 0, 1, 2)
        self.compDrawing = QtWidgets.QGraphicsView(self.dockWidgetContents)
        self.compDrawing.setObjectName("compDrawing")
        self.gridLayout_8.addWidget(self.compDrawing, 2, 0, 1, 2)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionShow_tape_samples = QtWidgets.QAction(MainWindow)
        self.actionShow_tape_samples.setObjectName("actionShow_tape_samples")
        self.actionShow_component_image = QtWidgets.QAction(MainWindow)
        self.actionShow_component_image.setObjectName("actionShow_component_image")
        self.actionShow_full_PCB = QtWidgets.QAction(MainWindow)
        self.actionShow_full_PCB.setObjectName("actionShow_full_PCB")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionGeneral_settings = QtWidgets.QAction(MainWindow)
        self.actionGeneral_settings.setObjectName("actionGeneral_settings")
        self.actionPreprocessing = QtWidgets.QAction(MainWindow)
        self.actionPreprocessing.setObjectName("actionPreprocessing")
        self.actionProcessing = QtWidgets.QAction(MainWindow)
        self.actionProcessing.setObjectName("actionProcessing")
        self.actionDrawing = QtWidgets.QAction(MainWindow)
        self.actionDrawing.setObjectName("actionDrawing")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuView.addAction(self.actionShow_tape_samples)
        self.menuView.addAction(self.actionShow_component_image)
        self.menuView.addAction(self.actionShow_full_PCB)
        self.menuSettings.addAction(self.actionGeneral_settings)
        self.menuSettings.addAction(self.actionPreprocessing)
        self.menuSettings.addAction(self.actionProcessing)
        self.menuSettings.addAction(self.actionDrawing)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionVersion)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PcadAttr"))
        self.pushButton_out.setText(_translate("MainWindow", "choose"))
        self.pushButton_in.setText(_translate("MainWindow", "choose"))
        self.label.setText(_translate("MainWindow", "Input file"))
        self.label_2.setText(_translate("MainWindow", "Output file"))
        self.pushButton.setText(_translate("MainWindow", "Generate"))
        self.label_3.setText(_translate("MainWindow", "Description:"))
        self.label_4.setText(_translate("MainWindow", "Availible actions:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Processing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Pad definition"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Component definition"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Components"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Reports"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.pushButton_2.setText(_translate("MainWindow", "Left"))
        self.pushButton_3.setText(_translate("MainWindow", "Right"))
        self.label_7.setText(_translate("MainWindow", "Board Image: WIP"))
        self.actionShow_tape_samples.setText(_translate("MainWindow", "Tape samples"))
        self.actionShow_component_image.setText(_translate("MainWindow", "Component image"))
        self.actionShow_full_PCB.setText(_translate("MainWindow", "Full PCB"))
        self.actionAbout.setText(_translate("MainWindow", "Manual"))
        self.actionVersion.setText(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionGeneral_settings.setText(_translate("MainWindow", "General settings"))
        self.actionPreprocessing.setText(_translate("MainWindow", "Preprocessing"))
        self.actionProcessing.setText(_translate("MainWindow", "Processing"))
        self.actionDrawing.setText(_translate("MainWindow", "Drawing"))
