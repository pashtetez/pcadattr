from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class PnP(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.size: int = 60
        # self.setToolTip("pnp ololo")
        # self.setCursor(Qt.OpenHandCursor)
        # self.setAcceptedMouseButtons(Qt.LeftButton)
        # self.setFlag(QGraphicsItem.ItemIsMovable)
        # # self.setFlag(QGraphicsItem.itemIsSelectable)

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size, self.size)

    def paint(self, painter: QPainter, option, widget):
        painter.setPen(Qt.white)
        painter.setBrush(Qt.white)
        painter.drawLine(-self.size / 6, -self.size / 6, -self.size / 6, self.size / 6)
        painter.drawLine(-self.size / 6, self.size / 6, self.size / 6, self.size / 6)
        painter.drawLine(self.size / 6, self.size / 6, self.size / 6, -self.size / 6)
        painter.drawLine(self.size / 6, -self.size / 6, -self.size / 6, -self.size / 6)
        painter.drawLine(-self.size / 2, 0, self.size / 2, 0)
        painter.drawLine(0, -self.size / 2, 0, self.size / 2)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        self.setPos(self.mapToScene(event.pos()))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))

    # def mousePressEvent(self, QGraphicsSceneMouseEvent):
    #     self.setCursor(Qt.ClosedHandCursor)

    # def mouseMoveEvent(self,event: QGraphicsSceneMouseEvent):
    #     if QLineF(event.screenPos(), event.buttonDownScreenPos(Qt.LeftButton)).length() < QApplication.startDragDistance():
    #         return
    #
    #     drag = QDrag(event.widget())
    #     mime = QMimeData()
    #     drag.setMimeData(mime)
    #     n = 0
    #     if n > 1 and QRandomGenerator.global_().bounded(3) == 0 :
    #         n+=1
    #         image = QImage(":/images/head.png")
    #         mime.setImageData(image)
    #         drag.setPixmap(QPixmap.fromImage(image).scaled(30, 40))
    #         drag.setHotSpot(QPoint(15, 30))
    #     else:
    #         mime.setColorData(QColor(Qt.red))
    #         mime.setText("pnp tetete")
    #
    #         pixmap = QPixmap(34, 34)
    #         pixmap.fill(Qt.white)
    #
    #         painter = QPainter(pixmap)
    #         painter.translate(15, 15)
    #         painter.setRenderHint(QPainter.Antialiasing)
    #         self.paint(painter, 0, 0)
    #         painter.end()
    #
    #         pixmap.setMask(pixmap.createHeuristicMask())
    #
    #         drag.setPixmap(pixmap)
    #         drag.setHotSpot(QPoint(15, 20))
    #
    #         drag.exec()
    #         self.setCursor(Qt.OpenHandCursor)

    # def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
    #     self.setCursor(Qt.OpenHandCursor)
