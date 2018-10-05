import numpy as np
import random
import sys
import time
import cPickle as pickle

class game():
    
    def __init__(self):
        self.a = np.zeros(shape = (4,4), dtype = np.int32)
        self.max = self.a.max()
    
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
        #print "left!"
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
            #print 'row ', r, ' over'
        #print (b==self.a).all() ,'same?nei'
        return (b==self.a).all()
    
    def moverightward(self):
        #print "right!"
        #print self.a
        temp = np.fliplr(self.a)
        #print temp
        self.a[:] = temp
        #print self.a
        result = self.moveleftward()
        #print result, 'same?right'
        b = np.fliplr(self.a)
        self.a[:] = b
        return result
    
    def moveupward(self):
        temp = np.rot90(self.a, 1)
        #print temp
        self.a[:] = temp
        #print self.a
        result = self.moveleftward()
        #print result, 'same?up'
        b = np.rot90(self.a, 3)
        self.a[:] = b
        return result
        pass
    
    def movedownward(self):
        temp = np.rot90(self.a, 3)
        #print temp
        self.a[:] = temp
        #print self.a
        result = self.moveleftward()
        #print result, 'same?up'
        b = np.rot90(self.a, 1)
        self.a[:] = b
        return result
        pass
    
    def move(self,mv):
        
        while mv not in ['a','w','d','s']:
            print "invalid key, try again:\n"
            sys.stdout.flush()
            mv = sys.stdin.readline()[:-1]
        
        if mv == 'a':
            get = self.moveleftward()
            
        if mv == 'd':
            get = self.moverightward()
            
        if mv == 'w':
            get = self.moveupward()
            
        if mv == 's':
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
        print self.a
        sys.stdout.flush()

def gameplay():
    #load board
    global board
    board = {}
    global playerlist
    global timelist
    
    try:
        f1 = open('board.txt','r')
    except IOError:
        pass
    else:
        board = pickle.load(f1)
        f1.close()
    
    try:
        f4 = open('timelist.txt','r')
    except IOError:
        pass
    else:
        timelist = pickle.load(f4)
        f4.close()    
    timelist.append(t)

    #init        
    game1 = game()
    game1.new()
    game1.new()
    game1.showplate()
    while game1.if_full() == 0:
        print "next move\n"
        sys.stdout.flush()
        operate = sys.stdin.readline()[:-1]
        if operate == 'b':
            break
        same = game1.move(operate)
        #Write into file!
        np.savetxt('./2048users/'+str(t)+'.txt', game1.a, delimiter = ',')
        board[t]=game1.a.max()
        f2 = open('board.txt','w')
        pickle.dump(board, f2)
        f2.close()
        f3 = open('timelist.txt','w')
        pickle.dump(timelist, f3)
        f3.close()
        
        while same:
            print "same, next move\n"
            sys.stdout.flush()
            operate = sys.stdin.readline()[:-1]
            same = game1.move(operate)
        game1.new()
        game1.showplate()
    print "Game Over\n\n\n"
    sys.stdout.flush()
    tmax = sorted(board, key=lambda x:board[x])[-1]
    print 'At', time.strftime("%a %b %d %H:%M:%S %Y",(time.localtime(tmax))), ',player ',tmax, ' achieved ', game1.a.max()
    sys.stdout.flush()
    if tmax == t:
        print "Congratulations!\n\n"
        sys.stdout.flush()
    else:
        print "You are just one step from the top.\nWant to beat that one? Reload to play again!\n\n"
        sys.stdout.flush()
    
    #print board
    #print sorted(board, key=lambda x:board[x])[(min(len(board),15))*(-1)]
    #sys.stdout.flush()
    
    
def main():
    global playerlist
    playerlist = {}
    global timelist
    timelist = []
    global t
    t = time.time()
    global tformat
    tformat = time.strftime("%a %b %d %H:%M:%S %Y",(time.localtime(t)))
    print "\n\nWelcome to 2048 online.\nClick button to control.\nYour ID is: ", t#,"\nWould like to have a nickname? Or you can just skip buy click 'submit'.\n"
    sys.stdout.flush()
    gameplay()
    
if __name__ == "__main__":
    main()