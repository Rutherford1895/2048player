import numpy as np
import random
import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, qRgb, QTextOption
from PyQt5.QtCore import Qt, QRectF, QThread, pyqtSignal

class Game(QThread):
    _signal1 = pyqtSignal(str)
    def __init__(self):
        super(Game, self).__init__()
        self.moveName = {0:'up',1:'down',2:'left',3:'right'}
        self.moveActions = {0:self.moveupward,1:self.movedownward,2:self.moveleftward,3:self.moverightward}
        self.a = np.zeros(shape = (4,4), dtype = np.int32)
        print('Initialized!')
        
    def run(self):
        print('Auto running...')
        self.resetGame()
        same = 0
        step = 0
        while not self.if_full():
            m = random.randint(0,3)
            same = self.move(self.moveName[m])
            #print("Same? "+str(same))
            while same:
                #print("Solving Same...")
                m = random.randint(0,3)
                #print(m)
                same = self.move(self.moveName[m])
            step += 1
            print(str(step)+" steps")
            self.new()
            self.showplate()
            self._signal1.emit('Moved.')
            time.sleep(0.05)
            if self.if_full() == 1:
                print("Game Over.")
                break;
            print("\nNext move:")
            
    
    def resetGame(self):
        global a
        self.a = np.zeros(shape = (4,4), dtype = np.int32)
        self.max = self.a.max()
        self.lastPosition=None
        self.new()
        self.new()
        self.showplate()
        self._signal1.emit('Reset Done.')
        time.sleep(0.2)
    
    def randrowcol(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        return (row, col)
    
    def rand24(self):
        if random.randint(1,8) == 4:
            return 4
        else:
            return 2
     
    def moveleftward(self):
        b = np.empty_like(self.a)
        b[:] = self.a #copy, for comparing
        for r in range(0,4): #by row
            for c in range(0,3): #bubble1
                for i in range(0,3): 
                    if self.a[r][i] == 0:
                        self.a[r][i] = self.a[r][i+1]
                        self.a[r][i+1] = 0
            
            for c in range(0,3):#add
                if self.a[r][c] == self.a[r][c+1] and self.a[r][c]!=0:
                    self.a[r][c]*=2
                    self.a[r][c+1] = 0
            for c in range(0,3):
                for i in range(0,3): #bubble2
                    if self.a[r][i] == 0:
                        self.a[r][i] = self.a[r][i+1]
                        self.a[r][i+1] = 0

        return (b==self.a).all()
    
    def moverightward(self):
        #print a
        temp = np.fliplr(self.a)
        #print temp
        self.a[:] = temp
        #print a
        result = self.moveleftward()
        #print result, 'same?right'
        b = np.fliplr(self.a)
        self.a[:] = b
        return result
    
    def moveupward(self):
        temp = np.rot90(self.a, 1)
        #print temp
        self.a[:] = temp
        #print a
        result = self.moveleftward()
        #print result, 'same?up'
        b = np.rot90(self.a, 3)
        self.a[:] = b
        return result
    
    def movedownward(self):
        temp = np.rot90(self.a, 3)
        #print temp
        self.a[:] = temp
        #print a
        result = self.moveleftward()
        #print result, 'same?up'
        b = np.rot90(self.a, 1)
        self.a[:] = b
        return result
        pass
    
    def move(self,mv):
        print(mv)   
        if mv == Qt.Key_A or mv == Qt.Key_Left or mv == 'left':
            get = self.moveleftward()            
        if mv == Qt.Key_D or mv == Qt.Key_Right or mv == 'right':
            get = self.moverightward()          
        if mv == Qt.Key_W or mv == Qt.Key_Up or mv == 'up':
            get = self.moveupward()          
        if mv == Qt.Key_S or mv == Qt.Key_Down or mv == 'down':
            get = self.movedownward()      
        return get
                
    def new(self):
        if self.if_full() == 0:
            newrc = self.randrowcol()
            while self.a[newrc[0]][newrc[1]] != 0:
                newrc = self.randrowcol()
            self.a[newrc[0]][newrc[1]] = self.rand24()
        else:
            pass
    
    def if_full(self):
        zero_exist = 0
        for r in range(0,4):
            for c in range(0,4):
                if self.a[r][c] == 0:
                    zero_exist += 1 #find 0, +1
        
        if zero_exist == 0:#no 0, this keeps 0
            #print 'full!'
            return 1

        else:
            #print 'not full yet!'
            return 0
    
    def showplate(self):
        print(self.a)
        sys.stdout.flush()

class Window(QWidget): 
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(300,300,400,500)
        self.setWindowTitle("2048 PyQt")
        self.brushes={
            0:QBrush(QColor(0xcdc1b4)),
            1:QBrush(QColor(0x999999)),
            2:QBrush(QColor(0xeee4da)),
            4:QBrush(QColor(0xede0c8)),
            8:QBrush(QColor(0xf2b179)),
            16:QBrush(QColor(0xf59563)),
            32:QBrush(QColor(0xf67c5f)),
            64:QBrush(QColor(0xf65e3b)),
            128:QBrush(QColor(0xedcf72)),
            256:QBrush(QColor(0xedcc61)),
            512:QBrush(QColor(0xedc850)),
            1024:QBrush(QColor(0xedc53f)),
            2048:QBrush(QColor(0xedc22e)),
        }    
        self.backgroundBrush=QBrush(QColor(0xbbada0))
        self.resetRect=QRectF(290,30,100,40)
        self.descriptionRect=QRectF(10,30,270,40)
        
        self.player1 = Game()
        self.player1._signal1.connect(self.update)
        self.player1._signal1.connect(self.showInfo)           
        self.player1.start()
    
    def showInfo(self, info):
        print(info)
    
    def mousePressEvent(self,e):
        self.player1.lastPoint=e.pos()

    def mouseReleaseEvent(self,e):
        if self.resetRect.contains(self.player1.lastPoint.x(),self.player1.lastPoint.y()) and self.resetRect.contains(e.pos().x(),e.pos().y()):
            if QMessageBox.question(self,'','Restart?', QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                self.player1.resetGame()
    
    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_A,Qt.Key_W,Qt.Key_D,Qt.Key_S,Qt.Key_Up,Qt.Key_Down,Qt.Key_Left,Qt.Key_Right]:
            same = self.player1.move(e.key())
            if not same:
                self.player1.new()
                self.player1.showplate()
                self.update()
                print("\nNext move:")
            else:
                if self.player1.if_full() == 1:
                    print("Game Over.")
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.NoPen)
        qp.setBrush(self.brushes[1024])
        qp.drawRoundedRect(self.resetRect,5,5)
        qp.setPen(QColor(0xf9f6f2))
        qp.setFont(QFont("Thoma",26))
        qp.drawText(self.resetRect, "Reset", QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))
        qp.setPen(QColor(0x776e65))
        qp.setFont(QFont("Thoma",13))
        qp.drawText(self.descriptionRect,"Join the numbers og get to the 2048 title!", QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))
        for i in range(4):
            for j in range(4):
                rect=QRectF(10+j*100, 110+i*100, 80, 80)
                qp.setPen(Qt.NoPen)
                #qp.setBrush(QColor(255,80,0,160))
                qp.setBrush(self.brushes[self.player1.a[i,j]])
                qp.drawRoundedRect(rect, 5, 5)
                
                if self.player1.a[i,j] < 16:
                    qp.setPen(QColor(0x776e65))
                else:
                    qp.setPen(QColor(0xf9f6f2))
                if self.player1.a[i,j] > 512:
                	qp.setFont(QFont("Tahoma",30))
                elif self.player1.a[i,j] > 64:
                	qp.setFont(QFont("Tahoma",40))
                else:
	                qp.setFont(QFont("Tahoma",50))
                if self.player1.a[i,j] != 0:
                	qp.drawText(rect, str(self.player1.a[i,j]), QTextOption(Qt.AlignHCenter|Qt.AlignVCenter))           
        qp.end()
    

app = QApplication(sys.argv)
window1 = Window()
window1.show()
sys.exit(app.exec_())

    