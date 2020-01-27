from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_settings import Ui_Form


class Settings(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.settings_tree.itemClicked.connect(self.settings_tree_clicked)

        self.main_index = 0
        self.tab_widgets = [self.ui.tab_widget0, self.ui.tab_widget1, self.ui.tab_widget2, self.ui.tab_widget3]
        for i in range(len(self.tab_widgets)):
            self.tab_widgets[i].currentChanged.connect(self.tab_index_changed)
        self.ui.settings_tree.expandAll()
        self.settings_tree_clicked(self.ui.settings_tree.topLevelItem(self.main_index), 0)
        self.ui.settings_tree.setCurrentItem(self.ui.settings_tree.topLevelItem(self.main_index))

    @pyqtSlot(int)
    def showPage(self, a):
        self.main_index = a
        self.ui.settings_tree.expandAll()
        self.settings_tree_clicked(self.ui.settings_tree.topLevelItem(self.main_index), 0)
        self.ui.settings_tree.setCurrentItem(self.ui.settings_tree.topLevelItem(self.main_index))
        self.show()

    @pyqtSlot(int)
    def tab_index_changed(self, a):
        self.ui.settings_tree.setCurrentItem(self.ui.settings_tree.topLevelItem(self.main_index).child(a))

    @pyqtSlot(QTreeWidgetItem, int)
    def settings_tree_clicked(self, a, b):
        self.main_index = self.ui.settings_tree.indexOfTopLevelItem(a)
        sub_index = 0
        if self.main_index == -1:
            for i in range(self.ui.settings_tree.topLevelItemCount()):
                if self.ui.settings_tree.topLevelItem(i):
                    if self.ui.settings_tree.topLevelItem(i).indexOfChild(a) != -1:
                        self.main_index = i
                        sub_index = self.ui.settings_tree.topLevelItem(i).indexOfChild(a)
                        break
        self.ui.stackedWidget.setCurrentIndex(self.main_index)
        self.tab_widgets[self.main_index].blockSignals(True)
        self.tab_widgets[self.main_index].setCurrentIndex(sub_index)
        self.tab_widgets[self.main_index].blockSignals(False)
        self.ui.labelCurrentSetting.setText(a.text(0))
        # print(a.text(0))
        # print(main_index)
        # print(sub_index)
