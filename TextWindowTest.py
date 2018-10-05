import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.Qt import qRgb

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.text = '2'
        self.setGeometry(300,300,400,400)
        self.setWindowTitle("Test")
        self.show()
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
    
    def drawText(self, event, qp):
        qp.setPen(QColor(168,34,3))
        qp.setFont(QFont("Decorative",80))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())