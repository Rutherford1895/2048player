import numpy as np
import random
import sys
import time

sleepduration = 0.05

class Game:
    def __init__(self):
        self.chessboard = np.zeros(shape = (4,4), dtype = np.int32)
        
    def setBoard(self,board):
        self.chessboard = board
    
    def resetGame(self):
        self.chessboard = np.zeros(shape = (4,4), dtype = np.int32)
        self.max = self.chessboard.max()
        self.lastPosition = None
        self.new()
        self.new()
        self.showplate()
        print('Reset Done.')
        time.sleep(sleepduration)
    
    def randrowcol(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        return (row, col)
    
    def rand24(self):
        if random.randint(1, 8) == 4:
            return 4
        else:
            return 2
     
    def moveleftward(self):
        b = np.empty_like(self.chessboard)
        b[:] = self.chessboard  # copy, for comparing
        for r in range(0, 4):  # by row
            for c in range(0, 3):  # bubble1
                for i in range(0, 3): 
                    if self.chessboard[r][i] == 0:
                        self.chessboard[r][i] = self.chessboard[r][i + 1]
                        self.chessboard[r][i + 1] = 0
            
            for c in range(0, 3):  # add
                if self.chessboard[r][c] == self.chessboard[r][c + 1] and self.chessboard[r][c] != 0:
                    self.chessboard[r][c] *= 2
                    self.chessboard[r][c + 1] = 0
            for c in range(0, 3):
                for i in range(0, 3):  # bubble2
                    if self.chessboard[r][i] == 0:
                        self.chessboard[r][i] = self.chessboard[r][i + 1]
                        self.chessboard[r][i + 1] = 0

        return (b == self.chessboard).all()
    
    def moverightward(self):
        # print a
        temp = np.fliplr(self.chessboard)
        # print temp
        self.chessboard[:] = temp
        # print a
        result = self.moveleftward()
        # print result, 'same?right'
        b = np.fliplr(self.chessboard)
        self.chessboard[:] = b
        return result
    
    def moveupward(self):
        temp = np.rot90(self.chessboard, 1)
        # print temp
        self.chessboard[:] = temp
        # print a
        result = self.moveleftward()
        # print result, 'same?up'
        b = np.rot90(self.chessboard, 3)
        self.chessboard[:] = b
        return result
    
    def movedownward(self):
        temp = np.rot90(self.chessboard, 3)
        # print temp
        self.chessboard[:] = temp
        # print a
        result = self.moveleftward()
        # print result, 'same?up'
        b = np.rot90(self.chessboard, 1)
        self.chessboard[:] = b
        return result
    
    def move(self, mv):
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
            while self.chessboard[newrc[0]][newrc[1]] != 0:
                newrc = self.randrowcol()
            self.chessboard[newrc[0]][newrc[1]] = self.rand24()
        else:
            pass
    
    def if_full(self):
        zero_exist = 0
        for r in range(0, 4):
            for c in range(0, 4):
                if self.chessboard[r][c] == 0:
                    zero_exist += 1  # find 0, +1
        
        if zero_exist == 0:  # no 0, this keeps 0
            # print 'full!'
            return 1
        else:
            # print 'not full yet!'
            return 0
    
    def showplate(self):
        print(self.chessboard)
        sys.stdout.flush()