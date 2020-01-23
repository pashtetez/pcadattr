#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import loads, dumps
from datetime import datetime
import re, os, sys
from io import StringIO
import contextlib

from ui_main import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
# from PyQt5.QtSvg import *
from PyQt5 import uic

from pcadfile import *

# pyinstaller pcadattr.py --add-data "main.ui;." -y --onefile --windowed

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(os.path.realpath(__file__))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        ui_main_window, qt_base_class = uic.loadUiType(os.path.join(base_path, "main.ui"))
        self.ui = ui_main_window()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fdata = []  # read array
        self.ui.listWidget.itemClicked.connect(self.show_comment)
        self.execfuncs()

    @pyqtSlot()
    def on_pushButton_in_clicked(self):
        self.ui.lineEdit_in.setText(
            QFileDialog.getOpenFileName(self, "Open pcad file", QFileInfo(self.ui.lineEdit_in.text()).filePath(),
                                        "PCAD Files (*.pcb *.PCB)")[0])
        if self.ui.lineEdit_in.text() != "":
            self.ui.lineEdit_out.setText(self.ui.lineEdit_in.text())
            finf = QFileInfo(self.ui.lineEdit_out.text())
            self.ui.lineEdit_out.setText(finf.path() + "/" + ''.join(finf.fileName().split(".")[:-1]) + "_SB.pcb")

    @pyqtSlot()
    def on_pushButton_out_clicked(self):
        fileDialog = QFileDialog()
        fileDialog.setDefaultSuffix("pcb")
        self.ui.lineEdit_out.setText(
            fileDialog.getSaveFileName(self, "Save pcad file", QFileInfo(self.ui.lineEdit_out.text()).filePath(),
                                       "PCAD Files (*.pcb)")[0])

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if not self.ui.lineEdit_out.text() or not self.ui.lineEdit_in.text():
            print("empty")
            return
        new_file = QFileInfo(self.ui.lineEdit_out.text())
        if new_file.exists():
            if (QMessageBox.information(self, "Converter",
                                        "Output file already exists. Are you sure you want to continue?",
                                        QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Cancel):
                return
        bad_file = False
        try:
            with open(str(self.ui.lineEdit_in.text()), 'r', encoding="cp1251") as fl:
                if fl.read().find("ACCEL_ASCII") != 0:
                    bad_file = True
        except:
            bad_file = True
        if bad_file:
            if (QMessageBox.warning(self, "Converter",
                                    "Given file is not in ASCII format. Please select another file",
                                    QMessageBox.Ok)):
                return
        with open(str(self.ui.lineEdit_in.text()), 'r', encoding="cp1251") as fl:
            data = fl.read()
            a = PcadFile(data)
            a.process()
            for x in range(self.ui.listWidget.count()):
                fun = self.ui.listWidget.item(x)
                if fun.checkState() == Qt.Checked:
                    pass
            with open(self.ui.lineEdit_out.text(), 'w', encoding="cp1251", errors="surrogateescape") as f:
                f.write(a.export_to_str())

        if (QMessageBox.information(self, "Converter",
                                    "File generated successfully",
                                    QMessageBox.Ok)):
            return

    @pyqtSlot(QListWidgetItem)
    def show_comment(self, item):
        self.ui.plainTextEdit.clear()
        fun = open(item.text() + '.fun', "r", encoding="utf8")
        for line in fun:
            if line.startswith("#"):
                self.ui.plainTextEdit.setPlainText(self.ui.plainTextEdit.toPlainText() + line)
            else:
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
