from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CompDefModel(QAbstractTableModel):
    class Filter(QSortFilterProxyModel):
        def __init__(self, top, parent=None):
            super().__init__(parent)
            self.m_top = top
            self.setSourceModel(self.m_top)
            self.setDynamicSortFilter(True)

        def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):
            return self.m_top.filterAcceptsRow(source_row, source_parent)

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.filter = CompDefModel.Filter(self)
        self.m_item_dict = data
        self.m_header_data = ["type", "original_name", "smd_pads", "dip_pads", "width", "height", "size", "dipsmd", "group"]

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return QVariant()
        elif index.row() >= len(self.m_item_dict):
            return QVariant()
        elif Qt.DisplayRole != role and Qt.EditRole != role:
            return QVariant()
        return self.rawDisplayData(index)

    def rawDisplayData(self, index: QModelIndex):
        return list(self.m_item_dict.items())[index.row()][1].get(self.m_header_data[index.column()])

    def rowCount(self, parent: QModelIndex):
        return len(self.m_item_dict)

    def columnCount(self, parent: QModelIndex):
        return len(self.m_header_data)

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):
        return True

    def index(self, row: int, column: int, parent: QModelIndex):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, list(self.m_item_dict.items())[row][1])

