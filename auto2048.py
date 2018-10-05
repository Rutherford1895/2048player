import numpy as np
import random
import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QTextOption, QPen
from PyQt5.QtCore import Qt, QRectF, QThread, pyqtSignal, QObject

moveName = {0:'up', 1:'down', 2:'left', 3:'right'}
'''
### Control Panel ###
'''
sleepduration = 0
runtimesOneStep = 500
proposalThreshold = 2
initialCodelets = 100

'''
class Node:
    def __init__(self, conceptName = '', conceptActivity = 0):
        self.concept = conceptName
        self.activity = conceptActivity
        self.checkActivity()
        self.connectionList=[]
        self.connectionActivity = {}
    
    def checkActivity(self):
        if self.activity <0:
            print("Concept's activity lower than 0.")
            self.activity = 0
            print("Concept's activity higher than 0.")
        if self.activity >100:
            self.activity = 100
'''

def selectRandom(var):
    if len(var) == 0:   # Empty iterable cannot be randomed
        print(len(var))
        print(var)
        time.sleep(2)
    return var[random.randint(0,len(var)-1)]

class conceptWeb(QObject):
    _signal3 = pyqtSignal(list)
    def __init__(self):
        super(conceptWeb, self).__init__()
        self.concepts = []
        self.activities = {}
        # Add pre-set concepts
        self.addConcept('same')
        self.addConcept('next')
        for i in [2,4,8,16,32,64,128,256,512,1024,2048,4096]: 
            self.addConcept(i)
        print('Concept web initialized.')
    
    def addConcept(self, cpt):
        #self.concepts.append(Node(name,0))
        #print("Concept added: "+self.concepts[-1].concept)
        self.concepts.append(cpt)
        self.activities[cpt]=0
        #print('Concept {} added.'.format(cpt))
        self._signal3.emit(self.conceptCollect())
    
    def activityUp(self, name):
        if self.activities[name] <10:
            self.activities[name]+=1
            #print('Concept {} up to {}.'.format(str(name),str(self.activities[name])))
            self._signal3.emit(self.conceptCollect())
        
    def activityDown(self, name):
        if self.activities[name] >0:
            self.activities[name]-=1
            print('Concept {} down to {}.'.format(str(name),str(self.activities[name])))
            self._signal3.emit(self.conceptCollect())
        
    def conceptCollect(self):
        #print('Collecting')
        collect = []
        for i in self.concepts:
            collect.append((i,self.activities[i]))
        return collect
    
    def cleanUp(self):
        for key in self.activities:
            self.activities[key] = 0
        #print("Concept web cooled down.")

class Structure:
    def __init__(self, ele=None, asgnCpt=None):
        self.cord = ele
        #self.elements = self.convertSpace(ele)
        #print('elements = ')
        #print(self.elements)
        self.assignedConcept = asgnCpt
        #print('concept = ' +str(asgnCpt))
        #self.activity = 1
    def convertSpace(self,el):
        '''
        print('length of element = 2')
        print(el)
        print(el[0])
        print(el[1])
        time.sleep(0.2)
        '''
        if type(el[0]) == int and type(el[1]) == int:
            spc = np.zeros(shape=(4,4), dtype = np.int32)
            spc[el[0]][el[1]] = 1
            return spc
        elif type(el[0]) != int and type(el[1]) != int: # assume only 2 types: int and not int.
            spc = el[0].elements + el[1].elements
            #print(spc)
            return spc
        else:
            print('unknown type. {} and {}..'.format(str(type(el[0])),str(type(el[1]))))
        
        
    
class workSpace(QObject):
    _signal2 = pyqtSignal(list)
    _signal6 = pyqtSignal(list)
    def __init__(self):
        super(workSpace, self).__init__()
        self.perceptionSpace = np.zeros(shape = (4,4), dtype = np.int32)
        self.structureList = []
        self.structuresActivity = {}
        self.depictList = []
        print('Work space initialized.')
    
    def addStructure(self, subjective, predictive):
        #print("addStructure called.")
        #print(predictive)
        #print(type(predictive))
        if type(predictive) == int: # Structure of titles
            self.addStructure_is(subjective, predictive)
        else:   # Structure of relationship (TODO: May be more, later)
            if predictive == 'next':
                self.addStructure_next(subjective, predictive)
            if predictive == 'same':
                self.addStructure_same(subjective, predictive)
        self.structureDepict()
            
    def addStructure_is(self, sub, pre):
        ###
        #print("addStructure_is called.")
        #print(self.perceptionSpace)
        #print(sub)
        ###
        if self.perceptionSpace[sub[0],sub[1]] == 0:  #This point on perception space is still empty
            s = Structure(sub, pre)
            self.structureList.append(s)
            self.structuresActivity[s]=1
            self.perceptionSpace[sub[0],sub[1]] = 1
            self._signal2.emit([s.cord,s.assignedConcept]) # Emit a signal to print and refesh GUI
            return s
            ### TEST ####
            #im = raw_input('press to go #1')
            time.sleep(sleepduration)
        else:   # the place on perception space is not empty. Something's there
            # TODO: a risk, the one already there is not identical to this new one.
            '''
            # TEST
            print('Going to look up...')
            print(sub)
            print(pre)
            print(len(self.structureList))
            for i in self.structureList:
                print('start for...')
                print(i.cord)
                print(i.assignedConcept)
                print(self.structuresActivity[i])
            '''
            self.structuresActivity[self.lookUp(sub, pre)] += 1 #find the structure and add its activity
            return self.lookUp(sub,pre)
    
    def addStructure_same(self, sub, pre):
        if not self.ifConsist(sub, pre):
            s = Structure(sub, pre)
            self.structureList.append(s)
            self.structuresActivity[s]=1    # Should be higher
            self._signal2.emit([s.cord,s.assignedConcept]) # Emit a signal to print and refresh GUI
            ### TEST ####
            #im = raw_input('press to go #1')
            time.sleep(sleepduration)
        else:
            print('The identical "same" structure is already there.')
    
    def addStructure_next(self, sub, pre):
        if not self.ifConsist(sub, pre):
            s = Structure(sub, pre)
            self.structureList.append(s)
            self.structuresActivity[s]=1
            self._signal2.emit([s.cord,s.assignedConcept]) # Emit a signal to print and refresh GUI
            ### TEST ####
            #im = raw_input('press to go #1')
            time.sleep(sleepduration)
        else:
            print('The identical "next" structure is already there.')
    
    def ifConsist(self,sub,pre): # if the structure workspace already in workspace?
        consist = 0
        for structure in self.structureList:
            if structure.cord == sub and structure.assignedConcept == pre: #same elements and same concept
                consist = 1
        return consist
    
    def lookUp(self,sub,pre): # find the same structure in this workspace
        for structure in self.structureList:
            if structure.cord == sub and structure.assignedConcept == pre:
                #print('Found!')
                return structure
            else:
                #print('notFound!')
                pass
    
    def structureDepict(self):
        '''
        Generate easy-used structure visualization
        '''
        for strc in self.structureList:
            if strc.assignedConcept in ['same','next']:    # get all 'same' structure, get 4 cords of 2 elements, translate into x y
                cords = [strc.cord[0].cord[1], strc.cord[0].cord[0], strc.cord[1].cord[1], strc.cord[1].cord[0]]
                # TEST
                #print('TEST')
                #print(strc.cord[0])
                #print(strc.cord[0].cord[1])
                #print(cords)
                xys = (401+50+cords[0]*100, 100+50+cords[1]*100, 401+50+cords[2]*100, 100+50+cords[3]*100, strc.assignedConcept)
                self.depictList.append(xys)
                #print(xys)
        self._signal6.emit(self.depictList)
        time.sleep(sleepduration)
                
        
    
    def cleanUp(self):
        self.perceptionSpace = np.zeros(shape = (4,4), dtype = np.int32)
        self.structureList = []
        self.structuresActivity = {}
        self.depictList = []
        #print('Work space cleaned up.')

class Codelet:
    def __init__(self, md = 0):
        self.mode = md

class codeRack(QObject):
    _signal4 = pyqtSignal(list)
    def __init__(self):
        super(codeRack,self).__init__()
        self.codeletList = []
        print('Code rack initialized.')
        self._signal4.emit(self.statistic())
    
    def addCodelet(self, mode):
        self.codeletList.append(Codelet(mode))
        self._signal4.emit(self.statistic())
        #print('Codelet added.')
    
    def removeCodelet(self, d):
        self.codeletList.remove(d)
        self._signal4.emit(self.statistic())
        #print('Codelet removed.')
    
    def cleanUp(self):
        self.codeletList = []
        
    def statistic(self):
        stat = {}
        tp = []
        for codelet in self.codeletList:
            if codelet.mode in stat:
                if codelet.mode not in tp: # collect types
                    tp.append(codelet.mode) 
                stat[codelet.mode]+=1 # collect frequency
            else:
                stat[codelet.mode]=0 # add this new type
        return [tp,stat]

class Controller(QObject):
    _signal5 = pyqtSignal(dict)
    def __init__(self):
        super(Controller,self).__init__()
        self.conceptweb1 = conceptWeb()
        self.workspace1 = workSpace()
        self.coderack1 = codeRack()
        self.proposals = []
        self.proposalsActivity = {}
        self.currentState = None
        self.lastState = np.zeros(shape =(4,4), dtype = np.int32)
        self.runtimes = 1
        
        self.codeletFunction = {0:self.shallWe, 1:self.areTheyNext, 2:self.areTheySame, 3:self.isNeighbourSame, 4:self.isNextSame}
        print('Controller initialized.')
    
    def recognizeAllTitles(self):
        #print('Recognizing...')
        for i in range(4):
            for j in range(4):
                if self.currentState[i,j] != 0:
                    self.workspace1.addStructure((i,j), int(self.currentState[i,j]))
    
    def isNeighbourSame(self, item): # item here is a single structure
        #print('Is any neighbour of {} mergable?'.format(str(item.cord)))
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                newCord = (item.cord[0]+i,item.cord[1]+j)
                # boundary & self check
                if newCord == item.cord:    # exclude self
                    pass
                elif not ( (newCord[0]>=0 and newCord[0]<=3) and (newCord[1]>=0 and newCord[1]<=3)):
                    pass    # exclude out of boundary
                else:
                    if self.currentState[newCord[0],newCord[1]] == item.assignedConcept: # A same neighbor found
                        #print('A same neighbour found')
                        self.conceptweb1.activityUp('same')
                        self.workspace1.addStructure((item,self.workspace1.addStructure_is(newCord,item.assignedConcept)), 'same')
                        self.coderack1.addCodelet(random.randint(1,4))
                        # propose for move direction
                        if newCord[0] == item.cord[0]:
                            p = random.randint(0,1)
                            self.shallWe(p)
                        if newCord[1] == item.cord[1]:
                            p = random.randint(2,3)
                            self.shallWe(p)   
    
    def isNextSame(self, item): # item here is a 'next' structure
        print('Here, is Next same?')
        if type(item.cord[0].assignedConcept) == int and item.cord[0].assignedConcept == item.cord[1].assignedConcept:
            print('a next structure is found same')
            self.conceptweb1.activityUp('same')
            self.workspace1.addStructure((item.cord[0],item.cord[1]), 'same')
            self.coderack1.addCodelet(random.randint(1,4))
            # propose for move direction
            if item.cord[0].cord[0] == item[1].cord[0]:
                p = random.randint(0,1)
                self.shallWe(p)
            if item[0].cord[1] == item[1].cord[1]:
                p = random.randint(2,)
                self.shallWe(p)
            
                    
    def areTheyNext(self, item):
        #print('Are they next...')
        #print(item[0])
        #print(item[0].cord)
        if type(item[0].cord[0])==int and type(item[1].cord[0])==int: #They are two titles
            if pow(pow(item[0].cord[0]-item[1].cord[0],2)+pow(item[0].cord[1]-item[1].cord[1],2),0.5) == 1: # distance = 1
                print('They are 2 titles next to each other')
                self.conceptweb1.activityUp('next')
                self.workspace1.addStructure(item, 'next')
                self.coderack1.addCodelet(random.randint(1,4))
                # propose for move direction                
                if item[0].cord[0] == item[1].cord[0]:
                    p = random.randint(0,1)
                    self.shallWe(p)
                if item[0].cord[1] == item[1].cord[1]:
                    p = random.randint(2,3)
                    self.shallWe(p)
            else:
                #print('They are 2 titles but not next to each other')
                self.coderack1.addCodelet(random.randint(1,2))
        else:
            #print('They are not 2 titles.')
            self.coderack1.addCodelet(random.randint(1,4))
    
    def areTheySame(self, item):
        #print('Are they same...')
        if len(self.workspace1.structureList)<2:
            self.coderack1.addCodelet(random.randint(1,4))
            #print('StructureList < 2')
        else: 
            # same type of structure concept in different positions
            if not item[0].cord == item[1].cord and item[0].assignedConcept == item[1].assignedConcept:
                if type(item[0].cord[0]) == int:
                    #print('Same title in different positions')
                    ##print(item[0].elements, item[0].assignedConcept)
                    ##print(item[1].elements, item[1].assignedConcept)
                    self.conceptweb1.activityUp('same')
                    self.workspace1.addStructure(item, 'same')
                    self.coderack1.addCodelet(random.randint(1,4))
                    # propose for move direction
                    if item[0].cord[0] == item[1].cord[0]:
                        p = random.randint(0,1)
                        self.shallWe(p)
                    if item[0].cord[1] == item[1].cord[1]:
                        p = random.randint(2,3)
                        self.shallWe(p)
                else:
                    print('The element of SAME structure must be titles.')
            # otherwise
            else:
                #print('No they are not same type of structure in different positions')
                self.coderack1.addCodelet(random.randint(1,3))
                      
    def shallWe(self, move): #put forward a proposal for move
        print('Shall we {} ?'.format(moveName[move]))
        if move in self.proposals: # if the proposal is already there
            if self.proposalsActivity[move] < 100: # control the range
                self.proposalsActivity[move]+=1
            elif self.proposalsActivity[move] < 1: #if the proposal has activity < 1
                self.proposals.remove(move) #delete this proposal
                self.proposalsActivity.pop(move)                
        else: # if the proposal is not there
            self.proposals.append(move) # add it and assign an activity
            self.proposalsActivity[move] = 1
        self._signal5.emit(self.proposalsActivity)
    
    def proposalPick(self):
        #print('Picking proposal...')
        if len(self.proposals) > 0: # if there is at least 1 proposal
            #print('Proposals:')
            #print(self.proposals)
            # get the one with highest activity
            chosen = self.proposals[0]
            for proposal in self.proposalsActivity.keys():
                if self.proposalsActivity[proposal]>self.proposalsActivity[chosen]:
                    chosen = proposal
            
            if self.proposalsActivity[chosen] > proposalThreshold: #only proposal with activity > 3 can be taken
                print('=== === === {} is picked === === ==='.format(moveName[chosen]))
                print('=== === === in {} times === === ==='.format(self.runtimes))
                return chosen   
            else:
                #print("No proposal active > {}".format(proposalThreshold))
                return 4 # 4 for not chosen
        else: # there haven't been any proposal so far
            return 4 # no move
        
    def randomMove(self):
        return random.randint(0,3)
        print('Random Move called :(')
    
    def randrowcol(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        return (row, col)
    
    def postRun(self): #clean up proposals, activities, save current state to last, clean current
        
        
        ### TEST ###
        #print('TESTING...')
        #print(self.workspace1.perceptionSpace)
        # for refresing GUI
        self.workspace1._signal2.emit([])
        #aaa = raw_input('press to go #2')
        time.sleep(sleepduration)
        
        self.proposals = []
        self.proposalsActivity = {}
        self.lastState = self.currentState.copy()
        self.currentState = np.zeros_like(self.currentState)
        self.runtimes = 1
    
    def nextStep(self, cs): # input a state and get a decision, main loop of this class
        print('nextStep() is called')
        
        m = 4 #preset the outcome move to be 4, an invalid move
        self.currentState = cs.copy() # Get current state
        self.recognizeAllTitles()
        if not (self.lastState == self.currentState).all(): # current is not same as last
            #print("current is different")
            for i in range(initialCodelets): # put some codelets for scout
                self.coderack1.addCodelet(random.randint(1,3))
            
            while self.runtimes < runtimesOneStep: # How many tries should the Multi-agent system try?
                #print('---Runetime: {} ---'.format(self.runtimes))
                cl = selectRandom(self.coderack1.codeletList) # Get a codelet from coderack randomly
                self.coderack1.removeCodelet(cl) # remove the codelet from coderack.
                
                if cl.mode == 0:    # shallWe? 
                    print("mode 0, shall we?")
                    
                
                if cl.mode == 1:    # areTheyNext?
                    #print("mode 1, are They Next")
                    if len(self.workspace1.structureList) > 1:
                        self.areTheyNext((selectRandom(self.workspace1.structureList),selectRandom(self.workspace1.structureList)))
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                    else:
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                        print('Structures still less than 2.')
                
                if cl.mode == 2:    # areTheySame?   
                    #print("mode 2, are They Same?") 
                    if len(self.workspace1.structureList) > 1:   
                        self.areTheySame((selectRandom(self.workspace1.structureList),selectRandom(self.workspace1.structureList))) 
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                    else:
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                        print('Structures still less than 2.')
                
                if cl.mode == 3:    # isNeighborSame?
                    #print("mode 3, is Neighbour same?")
                    #print self.workspace1.structureList
                    if len(self.workspace1.structureList) > 1:
                        itm = selectRandom(self.workspace1.structureList)
                        while type(itm.assignedConcept) != int:
                            itm = selectRandom(self.workspace1.structureList)
                        ##
                        self.isNeighbourSame(itm)
                        self.coderack1.addCodelet(random.randint(1,4))
                    else:
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                        print('Structures still less than 2.')
                
                if cl.mode == 4:    # is next same?
                    print('mode 4, is next same?')
                    if len(self.workspace1.structureList) > 1:
                        itm = selectRandom(self.workspace1.structureList)
                        while itm.assignedConcept != 'next':
                            itm = selectRandom(self.workspace1.structureList)
                        ##
                        self.isNextSame(itm)
                        self.coderack1.addCodelet(random.randint(1,4))
                    else:
                        self.coderack1.addCodelet(random.randint(1,4)) # put a codelet back to coderack
                        print('Structures still less than 2.')
                    
                m = self.proposalPick() # try to get a proposal
                
                #print('Codelet number: {}'.format(len(self.coderack1.codeletList)))
                self.runtimes += 1 # one more loop run
                if self.runtimes == runtimesOneStep: # This run fails, need report
                    print(self.runtimes)
                if m != 4:  # a proposal has been taken
                    #print('A')
                    self.postRun() #clean up proposals, activities, save current state to last, clean current
                    return m
                else:   # no proposal was taken, run again
                    pass
        else: #current is same as last, use random
            #print('B')
            #print('current state is same to last state, use random')
            m = self.randomMove() # use random function to get an m 0-3
            self.postRun() #clean up proposals, activities, save current state to last, clean current
            return m
        
        if m == 4: # m is still unchanged as 4, after all runs, cuz no proposal was taken
            #print('C')
            m = self.randomMove() # use random function to get an m 0-3
            self.postRun() #clean up proposals, activities, save current state to last, clean current
            return m
        

class randomController:
    def __init__(self):
        pass
    
    def nextStep(self, cs):
        return random.randint(0, 3)
    

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


class gamePlay(QThread):
    _signal1 = pyqtSignal(str)

    def __init__(self):
        super(gamePlay, self).__init__()
        self.game1 = Game() # Initialize a game
        
        self.controller1 = Controller() #Initialize a controller
        #self.controller1 = randomController()
        
        self.moveActions = {0:self.game1.moveupward, 1:self.game1.movedownward, 2:self.game1.moveleftward, 3:self.game1.moverightward}
        print('Initialized!')
        
    def run(self):
        self._signal1.emit('Auto running...')
        self.game1.resetGame()
        same = 0
        step = 0
        while not self.game1.if_full():
            m = self.controller1.nextStep(self.game1.chessboard)
            self.controller1.workspace1.cleanUp() # after every move generated, the picture will change, previous workspace can be Cleaned up. TODO : can be better!
            self.controller1.coderack1.cleanUp()
            self.controller1.conceptweb1.cleanUp()
            # Testing point
            #aa = raw_input('press enter to continue...')
            same = self.game1.move(moveName[m])
            # print("Same? "+str(same))
            while same:
                # print("Solving Same...")
                m = self.controller1.nextStep(self.game1.chessboard)
                self.controller1.workspace1.cleanUp() # clean up. as above.
                self.controller1.coderack1.cleanUp()
                # print(m)
                same = self.game1.move(moveName[m])
            step += 1
            print(str(step) + " steps")
            self.game1.new()
            self.game1.showplate()
            self._signal1.emit('Moved.')
            #time.sleep(sleepduration)
            if self.game1.if_full() == 1:
                print('full, let us see...') # TODO: can be better.
                if self.game1.move('up'):
                    if self.game1.move('down'):
                        if self.game1.move('left'):
                            if self.game1.move('right'):
                                print("Game Over.")
                                break
            print("\nNext move:")


class Window(QWidget): 

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(350, 250, 920, 500)
        self.setWindowTitle("2048 Cat")
        self.brushes = {
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
        self.backgroundBrush = QBrush(QColor(0xbbada0))
        
        self.resetRect = QRectF(290, 30, 100, 40)
        self.descriptionRect = QRectF(10, 30, 270, 40)
        self.infoFromSignal = []
        self.conceptFromSignal = []
        self.codeRackStatFromSignal = []
        self.proposalsActivityFromSignal = {}
        self.structureDepictList = []
        
        self.player1 = gamePlay()
        
        self.player1._signal1.connect(self.showInfo)
        self.player1._signal1.connect(self.update)
        
        self.player1.controller1.workspace1._signal2.connect(self.catchInfo)
        self.player1.controller1.workspace1._signal2.connect(self.update)
        
        self.player1.controller1.conceptweb1._signal3.connect(self.catchConcepts)
        self.player1.controller1.conceptweb1._signal3.connect(self.update)
        
        self.player1.controller1.coderack1._signal4.connect(self.catchCodeRackStat)
        self.player1.controller1.coderack1._signal4.connect(self.update)
        
        self.player1.controller1._signal5.connect(self.catchProposalsActivity)
        self.player1.controller1._signal5.connect(self.update)
        
        self.player1.controller1.workspace1._signal6.connect(self.catchDepictList)
        self.player1.controller1.workspace1._signal6.connect(self.update)
        
        self.player1.start()
        
    def catchDepictList(self, info):
        self.structureDepictList = info
    
    def showInfo(self, info):
        #print('Showing info from signal1...')
        #print(info)
        pass
    
    def catchInfo(self, info):
        #print('Info got from signal2, new structure')
        #print(info)
        self.infoFromSignal = info
    
    def catchConcepts(self, info):
        #print('Concept web from signal3')
        #print(info)
        self.conceptFromSignal = info
        
    def catchCodeRackStat(self,info):
        info.sort()
        self.codeRackStatFromSignal = info
        #print('Statistics get!')
        #print info
    
    def catchProposalsActivity(self,info):
        self.proposalsActivityFromSignal = info
    
    def mousePressEvent(self, e):
        self.player1.lastPoint = e.pos()

    def mouseReleaseEvent(self, e):
        if self.resetRect.contains(self.player1.lastPoint.x(), self.player1.lastPoint.y()) and self.resetRect.contains(e.pos().x(), e.pos().y()):
            # if QMessageBox.question(self,'','Restart?', QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
            self.update()
            self.player1.game1.resetGame()
            self.player1.start()
    
    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_A, Qt.Key_W, Qt.Key_D, Qt.Key_S, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            same = self.player1.game1.move(e.key())
            if not same:
                self.player1.game1.new()
                self.player1.game1.showplate()
                self.update()
                print("\nNext move:")
            else:
                if self.player1.game1.if_full() == 1:
                    print("Game Over.")
    
    def len2Font(self, toShow):
        if len(str(toShow))>5:
            ln = 5
        else:
            ln = len(str(toShow))
        len2font={5:QFont("Tahoma", 20),4:QFont("Tahoma", 30),3:QFont("Tahoma", 40),2:QFont("Tahoma", 50),1:QFont("Tahoma", 50)}
        return len2font[ln]
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        
        # Reset box
        qp.setPen(Qt.NoPen)
        qp.setBrush(self.brushes[1024])
        qp.drawRoundedRect(self.resetRect, 5, 5)
        qp.setPen(QColor(0xf9f6f2))
        qp.setFont(QFont("Tahoma", 25))
        qp.drawText(self.resetRect, "Reset", QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
        
        # Description
        qp.setPen(QColor(0x776e65))
        qp.setFont(QFont("Tahoma", 12))
        qp.drawText(self.descriptionRect, "2048 auto player\nwith Parallel Terraced Scan applied", QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
        
        # Titles left (game)
        for i in range(4):
            for j in range(4):
                rect = QRectF(j * 100, 100 + i * 100, 100, 100)
                qp.setPen(Qt.NoPen)
                # qp.setBrush(QColor(255,80,0,160))
                qp.setBrush(self.brushes[self.player1.game1.chessboard[i, j]])
                qp.drawRect(rect)
                
                if self.player1.game1.chessboard[i, j] < 10:
                    qp.setPen(QColor(0x776e65))
                else:
                    qp.setPen(QColor(0xf9f6f2))
                if self.player1.game1.chessboard[i, j] > 999:
                    qp.setFont(QFont("Tahoma", 30))
                elif self.player1.game1.chessboard[i, j] > 99:
                    qp.setFont(QFont("Tahoma", 40))
                else: # 1 or 2 digits
                    qp.setFont(QFont("Tahoma", 50))
                if self.player1.game1.chessboard[i, j] != 0:
                    qp.drawText(rect, str(self.player1.game1.chessboard[i, j]), QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))           
                
        # Titles right (perception space)
        borderRect =QRectF(400,100,400,400)
        qp.setPen(QColor(0xffffff)) # the black border
        qp.setBrush(QColor(0xffffff)) # the white background
        qp.drawRect(borderRect)
        
        # Draw perception space
        for i in range(4):
            for j in range(4):
                rect = QRectF(400 + j * 100, 100 + i * 100, 100, 100)
                
                if self.player1.controller1.workspace1.perceptionSpace[i,j] != 0:
                    qp.setPen(QColor(0x000000))
                    qp.setBrush(QColor(128,128,128,30))
                    qp.drawRect(rect)
                
                qp.setPen(QColor(0x000000))
                if self.player1.controller1.workspace1.perceptionSpace[i, j] > 999:
                    qp.setFont(QFont("Tahoma", 30))
                elif self.player1.controller1.workspace1.perceptionSpace[i, j] > 99:
                    qp.setFont(QFont("Tahoma", 40))
                elif self.player1.controller1.workspace1.perceptionSpace[i, j] > 9:
                    qp.setFont(QFont("Tahoma", 50))

        # Draw newly added structure
        # Draw titles
        if self.infoFromSignal != [] and type(self.infoFromSignal[0][1])==int:
            cordinate = self.infoFromSignal[0]
            structureRect = QRectF(400 + cordinate[1]*100, 100 + cordinate[0]*100, 100,100)
            qp.setFont(self.len2Font(str(self.infoFromSignal[1])))
            qp.setPen(QColor(0x999999))
            text = str(self.infoFromSignal[1])
            #print("This is the TEXT!  "+text)
            qp.drawText(structureRect,text,QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
        # TODO: Draw relation
        
        # Draw concepts
        for i in range(len(self.conceptFromSignal)):
            #print('Drawing Concepts')
            conceptRect = QRectF(801,100+20*i,120,20)
            qp.setPen(QColor(0x999999))
            qp.setBrush(QColor(0xffffff))
            qp.drawRect(conceptRect)
            conceptActivityRect = QRectF(801,100+20*i,self.conceptFromSignal[i][1]*10,20)
            qp.setPen(Qt.NoPen)
            qp.setBrush(QColor(0xf2b179))
            qp.drawRect(conceptActivityRect)
            qp.setPen(QColor(0x000000))
            qp.setFont(QFont("Tahoma",15))
            qp.drawText(conceptRect,str(self.conceptFromSignal[i][0]),QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
        
        # Draw coderack stat
        if len(self.codeRackStatFromSignal) > 0:
            statRect = QRectF(401,15,400,40)
            qp.setPen(QColor(0x555555))
            qp.setFont(QFont("Tahoma",20))
            statText=''
            if len(self.codeRackStatFromSignal[1]) > 0:
                for i in self.codeRackStatFromSignal[1]:
                    statText += str(i)+': '+str(self.codeRackStatFromSignal[0][i])+'  '
                    qp.drawText(statRect,statText)
        
        # Draw proposal activities
        upRect = QRectF(800,15,20,20)
        downRect = QRectF(800,35,20,20)
        leftRect = QRectF(780,35,20,20)
        rightRect = QRectF(820,35,20,20)
        dirRect = {0:upRect,1:downRect,2:leftRect,3:rightRect}
        if len(self.proposalsActivityFromSignal) > 0:
            for proposal in range(4):
                qp.setBrush(QColor(0xffffff))
                qp.drawRect(dirRect[proposal])
                if proposal in self.proposalsActivityFromSignal:
                    qp.setPen(QColor(0x000000))
                    qp.drawText(dirRect[proposal],str(self.proposalsActivityFromSignal[proposal]),QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
        
        # Draw stuctures
        strcTypeColor = {'same':Qt.gray, 'next':Qt.yellow}
        if len(self.structureDepictList) > 0:
            for strc in self.structureDepictList:
                pen = QPen(strcTypeColor[strc[4]], 2, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawLine(strc[0],strc[1],strc[2],strc[3])
                            
        
        qp.end()
  
  
app = QApplication(sys.argv)
window1 = Window()
window1.show()
sys.exit(app.exec_())