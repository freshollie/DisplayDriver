from DisplayDriver import DisplayDriver
from DisplayDriver.Intervals import *
from DisplayDriver.GuiObjects import *
import random

'''
Small sorting animator
'''

HIEGHT = 30.0
WIDTH = 60.0


class Bar(GuiObjectBase):
    def __init__(self, value, look = '#'):
        self.value = value
        GuiObjectBase.__init__(self, image=[['#']]*int(round(value/WIDTH*HIEGHT)))

    def updatePos(self, i):
        self.setPos([i, 0])

    def __value__(self):
        return self.value

    def selectRed(self):
        #self.setImage([['\x01\BACKGROUND_RED\x02\\'+'#']]*int(round(self.value/WIDTH*HIEGHT)))
        self.setImage([['O']]*int(round(self.value/WIDTH*HIEGHT)))

    def selectGreen(self):
        self.setImage([['-']]*int(round(self.value/WIDTH*HIEGHT)))

    def deselect(self):
        self.setImage([['#']]*int(round(self.value/WIDTH*HIEGHT)))

class SortingRepresentation(object):
    def __init__(self, speed=10):
        self.speed = speed
        self.sortIndex=0
        self.selectedBars = []
        self.bars = []
        self.newList()
        self.updateBars()
        self.changedThisPass = False
        Sequence(DisplayDriver.engine,Wait(2),Func(self.randomise),Wait(2),Func(self.start)).start()
        

    def start(self):
        self.taskId = DisplayDriver.engine.addTask(self.tick)

    def newList(self):
        for bar in self.bars:
            bar.removeNode()

        self.bars = []

        for i in reversed(range(int(WIDTH))):
            self.bars.append(Bar(i))
            

        for bar in self.bars:
            bar.render(DisplayDriver.engine)
            
    def randomise(self):
        random.shuffle(self.bars)
        self.updateBars()

    def deselectBars(self):
        for bar in self.selectedBars:
            bar.deselect()
        self.selectedBars = []

    def updateBars(self):
        for i in range(len(self.bars)):
            self.bars[i].updatePos(i)

    def sortTick(self):
        self.deselectBars()
        
        if self.bars[self.sortIndex].value<self.bars[self.sortIndex+1].value:
            self.bars[self.sortIndex],self.bars[self.sortIndex+1] = self.bars[self.sortIndex+1],self.bars[self.sortIndex]
            self.bars[self.sortIndex].selectRed()
            self.bars[self.sortIndex+1].selectRed()
            self.selectedBars.append(self.bars[self.sortIndex])
            self.selectedBars.append(self.bars[self.sortIndex+1])
            self.changedThisPass = True
        else:
            self.bars[self.sortIndex].selectGreen()
            self.bars[self.sortIndex+1].selectGreen()
            self.selectedBars.append(self.bars[self.sortIndex])
            self.selectedBars.append(self.bars[self.sortIndex+1])
            
        self.sortIndex+=1
        newStart = False

        if self.sortIndex+1>=len(self.bars):
            self.sortIndex=0
            newStart = True

        self.updateBars()

        return newStart
    
    def tick(self):
        newStart = False
        for i in range(self.speed):
            newStartOld = self.sortTick()
            if newStartOld:
                newStart = True
    
        if newStart:
            if not self.changedThisPass:
                DisplayDriver.engine.removeTask(self.taskId)
                self.updateBars()
            else:
                self.changedThisPass = False
                
            
DisplayDriver.engine.graphics.setRes([80,40])
DisplayDriver.engine.setFrameRate(50)
#DisplayDriver.debug.toggle()
SortingRepresentation()
DisplayDriver.init()
