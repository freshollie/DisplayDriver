'''
Snake by freshollie

Used to demonstrate the use of DisplayDriver
'''

from DisplayDriver import DisplayDriver
import random
from DisplayDriver.Intervals import *
from DisplayDriver.Input import *
from DisplayDriver.GuiObjects import *

foodChar=chr(1)

class SnakeServer(object):

    def __init__(self):
        self.game=SnakeGame([40,20],[19,1])

    def sendHeadPos(self,pos):
        pass

    def receieveHeadPos(self,pos):
        self.game.dummySnake.nextPos(pos)
        

class TailSegment(GuiObjectBase):

    def __init__(self,look='#'):
        GuiObjectBase.__init__(self,pos=[0,0])
        self[0]=[look]

class Head(GuiObjectBase):
    
    def __init__(self,pos,look='@'):
        GuiObjectBase.__init__(self,pos=pos)
        self[0]=[look]

class Tail(object):

    def __init__(self,tail,headPos):
        self.tail=tail
        self.renderer=None

    def addSegment(self,tail):
        self.tail.append(tail)
        self.tail[-1].setPos(self.lastSegmentPos)
        if self.renderer:
            self.tail[-1].render(self.renderer)

    def tick(self,headPos):
        pos=headPos[:]
        if self.tail:
            self.lastSegmentPos=self.tail[-1].getPos()
        for segment in self.tail:
            oldpos=segment.getPos()
            segment.setPos(pos)
            pos=oldpos

    def render(self,renderer):
        for segment in self.tail:
            segment.render(renderer)
        self.renderer=renderer

    def removeNode(self):
        for segment in self.tail:
            segment.removeNode()

    def hide(self):
        for segment in self.tail:
            segment.hide()

    def show(self):
        for segment in self.tail:
            segment.show()

class Food(GuiObjectBase):

    def __init__(self,look='*'):
        GuiObjectBase.__init__(self,pos=[0,0])
        self[0]=[look]

class Snake(object):
    
    def __init__(self,pos):
        self.head=Head(pos)
        self.tail=Tail([],self.head.getPos())

    def setDirection(self,direction):
        self.direction=direction

    def getDirection(self):
        return self.direction

    def nextHeadPos(self):
        if self.direction=='up':
            self.head.setY(self.head.getY()-1)

        elif self.direction=='down':
            self.head.setY(self.head.getY()+1)
            
        elif self.direction=='left':
            self.head.setX(self.head.getX()-1)
            
        else:
            self.head.setX(self.head.getX()+1)
    
    def nextPos(self):
        if not self.tail.tail:
            self.tail.lastSegmentPos=self.head.getPos()
        headPos=self.head.getPos()
        self.nextHeadPos()
        self.tail.tick(headPos)

    def explode(self):
        sequences=[]
        sequences.append(Sequence(DisplayDriver.engine))

        self.midPos=[int((self.head.getPos()[0]+self.tail.tail[-1].getPos()[0])/2),int((self.head.getPos()[1]+self.tail.tail[-1].getPos()[1])/2)]

        direction=[0,0]
        while direction==[0,0]:
            direction=[random.randint(-10,10),random.randint(-10,10)]
        multiplier=1

        for i in range(20):
            sequences[0].append(Func(self.head.setPos,[self.head.getPos()[0]+(i*direction[0]*multiplier),self.head.getPos()[1]+(i*direction[1]*multiplier)]))
        sequences[0].append(Func(self.head.removeNode))

        x=0
        for segment in self.tail.tail:
            direction=[0,0]
            while direction==[0,0]:
                direction=[random.randint(-10,10),random.randint(-10,10)]
            sequences.append(Sequence(DisplayDriver.engine))
            for i in range(20):
                sequences[-1].append(Func(segment.setPos,[segment.getPos()[0]+(i*direction[0]*multiplier),segment.getPos()[1]+(i*direction[1]*multiplier)]))
            sequences[-1].append(Func(segment.removeNode))
            x+=1

        for sequence in sequences:
            sequence.start()
        Explosion(self.midPos,DisplayDriver.engine).loop()

    def render(self,renderer):
        self.head.render(renderer)
        self.tail.render(renderer)

    def removeNode(self):
        self.head.removeNode()
        self.tail.removeNode()

    def hide(self):
        self.head.hide()
        self.tail.hide()

    def show(self):
        self.head.show()
        self.tail.show()

class DummySnake(Snake):

    def nextHeadPos(self,pos):
        self.head.setPos(pos)
    
    def nextPos(self,pos):
        if not self.tail.tail:
            self.tail.lastSegmentPos=self.head.getPos()
        headPos=self.head.getPos()
        self.nextHeadPos(pos)
        self.tail.tick(headPos)
        

class SnakeGame(object):

    def __init__(self,size,pos,inputs=True):
        self.size=size
        self.running=True
        self.tickNum=0
        self.taskId=0
        self.pos=pos
        self.score=0
        self.snake=None
        self.food=None
        self.scoreText=OnscreenText(['Score: 0'],pos=[self.pos[0]+self.size[0]+2,self.pos[1]])
        self.scoreText.render(DisplayDriver.engine)

        self.background=Rectangle(pos,size,char=' ')
        self.background.render(DisplayDriver.engine)
        
        self.border=Border(size,pos=pos)
        self.border.render(DisplayDriver.engine)
        
        self.start()
        if inputs:
            self.setUpKeyInputs()

    def countDown(self):
        minusPos=[-5,-3]
        numbers=[OnscreenText(['   d88 '.replace(' ',DisplayDriver.BACKGROUNDCHAR),  
                               '    88 '.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                               '    88 '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                               '    88 '.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                               '    88 '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                               '   d88P '.replace(' ',DisplayDriver.BACKGROUNDCHAR)],pos=[self.pos[0]+int(self.size[0]/2)+minusPos[0],self.pos[1]+int(self.size[1]/2)+minusPos[1]]),

                      OnscreenText([' .d8888b.  '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    'd88P  Y88b '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    '       888 '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    '     .d88P '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                     '.od888P"  '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    'd88P"      '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    '888"       '.replace(' ',DisplayDriver.BACKGROUNDCHAR),
                                    '888888888  '.replace(' ',DisplayDriver.BACKGROUNDCHAR)],pos=[self.pos[0]+int(self.size[0]/2)+minusPos[0],self.pos[1]+int(self.size[1]/2)+minusPos[1]]),
                     
                                    
                      OnscreenText([' .d8888b. '.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    'd88P  Y88b'.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    '     .d88P'.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    '    8888" '.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    '     "Y8b.'.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    '888    888'.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    'Y88b  d88P'.replace(' ',DisplayDriver.BACKGROUNDCHAR), 
                                    '  "Y8888P"'.replace(' ',DisplayDriver.BACKGROUNDCHAR)],pos=[self.pos[0]+int(self.size[0]/2)+minusPos[0],self.pos[1]+int(self.size[1]/2)+minusPos[1]])]

        for number in numbers:
            number.render(DisplayDriver.engine)
            number.hide()

        seq=Sequence(DisplayDriver.engine)

        seq.append(Func(numbers[2].show))
        for i in range(2,-1,-1):
            seq.append(Wait(1))
            if i!=0:
                seq.append(Parallel(Func(numbers[i].hide),
                                     Func(numbers[i-1].show)))
            else:
                seq.append(Func(numbers[i].hide))

        seq.append(Func(self.startTick))
            
        seq.start()
                                    

    def isColliding(self,headPos):
        try:
            char=self.border[0][headPos[1]-self.pos[1]][headPos[0]-self.pos[0]]
        except:
            return True
        if char!=DisplayDriver.BACKGROUNDCHAR and char!='*':
            return True
        else:
            for segment in self.snake.tail.tail:
                if headPos==segment.getPos() and segment!=self.snake.tail.tail[-1]:
                    return True
        return False

    def isEatingFood(self):
        headPos=self.snake.head.getPos()
        if headPos==self.food.getPos():
            return True
        return False

    def newFood(self):
        self.food=Food()
        while True:
            pos=[random.randint(self.pos[0]+1,self.pos[0]+self.size[0]-2),random.randint(self.pos[1]+1,self.pos[1]+self.size[1]-2)]
            if not self.isColliding(pos):
                 self.food.setPos(pos)
                 break
        self.food.render(DisplayDriver.engine)

    def workOutInput(self,event):
        if event==KeyCode.UPARROW:
            if self.snake.direction!='down':
                self.snake.setDirection('up')
        elif event==KeyCode.DOWNARROW:
            if self.snake.direction!='up':
                self.snake.setDirection('down')
        elif event==KeyCode.RIGHTARROW:
            if self.snake.direction!='left':
                self.snake.setDirection('right')
        elif event==KeyCode.LEFTARROW:
            if self.snake.direction!='right':
                self.snake.setDirection('left')
        elif event==KeyCode.RETURN:
            if not self.running:
                self.start()
        elif event==KeyCode.D:
            DisplayDriver.debug.toggle()
        else:
            pass

    def setUpKeyInputs(self):
        Input.bindAll(self.workOutInput)
        Input.mainLoop()
    
    def tick(self):
        oldHeadPos=self.snake.head.getPos()
        self.snake.nextHeadPos()
        if self.isColliding(self.snake.head.getPos()):
            self.snake.head.setPos(oldHeadPos)
            self.gameOver()
        else:
            self.snake.head.setPos(oldHeadPos)
            self.snake.nextPos()
            if self.isEatingFood():
                self.food.removeNode()
                self.snake.tail.addSegment(TailSegment())
                self.score+=1
                self.newFood()
                self.scoreText.setText(['Score: %s' %self.score])

    def start(self):
        self.running=True
        self.score=0
        self.scoreText.setText(['Score: %s' %self.score])

        if self.snake:
            self.snake.removeNode()

        if self.food:
            self.food.removeNode()
            
        self.snake=Snake([random.randint(self.pos[0]+3,self.pos[0]+self.size[0]-4),random.randint(self.pos[1]+3,self.pos[1]+self.size[1]-4)])
        self.snake.render(DisplayDriver.engine)
        self.snake.setDirection(random.choice(['up','down','left','right']))
        
        if self.snake.direction=='up':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX(),self.snake.head.getY()+1]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX(),self.snake.tail.tail[-1].getY()+1]
            self.snake.tail.addSegment(TailSegment())

        elif self.snake.direction=='down':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX(),self.snake.head.getY()-1]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX(),self.snake.tail.tail[-1].getY()-1]
            self.snake.tail.addSegment(TailSegment())
            
        elif self.snake.direction=='left':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX()+1,self.snake.head.getY()]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX()+1,self.snake.tail.tail[-1].getY()]
            self.snake.tail.addSegment(TailSegment())
            
        else:
            self.snake.tail.lastSegmentPos=[self.snake.head.getX()-1,self.snake.head.getY()]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX()-1,self.snake.tail.tail[-1].getY()]
            self.snake.tail.addSegment(TailSegment())
        
        self.newFood()
        self.countDown()

    def startTick(self):
        self.taskId=DisplayDriver.engine.addTask(self.tick)

    def disableRunning(self):
        self.running=False

    def gameOver(self):
        DisplayDriver.engine.removeTask(self.taskId)
        self.taskId=0
        seq=Sequence(DisplayDriver.engine)
        seq.append(Func(self.snake.explode))
        seq.append(Wait(2))
        seq.append(Func(self.disableRunning))
        seq.start()

    def show(self):
        self.background.show()
        self.border.show()
        self.snake.show()
        self.food.show()
        self.scoreText.show()

    def hide(self):
        self.background.hide()
        self.border.hide()
        self.snake.hide()
        self.food.hide()
        self.scoreText.hide()

    def destroy(self):
        self.background.removeNode()
        self.border.removeNode()
        self.scoreText.removeNode()
        self.snake.removeNode()
        self.food.removeNode()

class AI(object):

    def __init__(self,game):
        self.game=game
        self.taskId=DisplayDriver.engine.addTask(self.tick)
        self.deep=0
        self.directions=['up','down','left','right']
        #DisplayDriver.debug.toggle()

    def leftOrRight(self):
        if self.game.food.getX()>self.game.snake.head.getX():
            return False
        else:
            return True

    def upOrDown(self):
        if self.game.food.getY()>self.game.snake.head.getY():
            return False
        else:
            return True

    def isFoodInRow(self):
        if self.game.food.getY()==self.game.snake.head.getY():
            return True
        return False

    def isFoodInColumn(self):
        if self.game.food.getX()==self.game.snake.head.getX():
            return True
        return False

    def checkDirection(self,direction):
        self.deep+=1
        returnVal=True
        self.game.snake.setDirection(direction)
        oldSnake=[]
        oldSnakeHead=self.game.snake.head.getPos()[:]
        lastSegmentPos=self.game.snake.tail.lastSegmentPos[:]
        
        #Gets the orig snake pos
        for segment in self.game.snake.tail.tail:
            oldSnake.append(segment.getPos()[:])
        
        for i in range(30):    
            self.game.snake.nextPos()
            
            if self.game.isEatingFood():
                returnVal=True
                break
                
            elif self.game.isColliding(self.game.snake.head.getPos()):
                #print('collide')
                returnVal=False
                break
            elif self.workOutMove():
                returnVal=True
                break
            
        self.game.snake.head.setPos(oldSnakeHead)

        #puts snake back to normal
        for i in range(len(self.game.snake.tail.tail)):
            self.game.snake.tail.tail[i].setPos(oldSnake[i])

        self.game.snake.tail.lastSegmentPos=lastSegmentPos

      #  print(returnVal)
        self.deep-=1
        return returnVal

        

        

    def workOutMove(self,newMove=False):
        self.deep+=1
        if self.deep<=10:
            bestMove=False
            #print(self.deep)
            
            if self.isFoodInRow():
                #print('in Row')
                if self.leftOrRight():
                    directionChosen='left'
                    if self.game.snake.getDirection()!='right':
                       # print(directionChosen)
                        bestMove=self.checkDirection(directionChosen)
                    else:
                        bestMove=False
                else:
                    directionChosen='right'
                    if self.game.snake.getDirection()!='left':
                        #print(directionChosen)
                        bestMove=self.checkDirection(directionChosen)
                    else:
                        bestMove=False
            elif self.isFoodInColumn():
                if self.upOrDown():
                    directionChosen='up'
                    if self.game.snake.getDirection()!='down':
                        #print(directionChosen)
                        bestMove=self.checkDirection(directionChosen)
                    else:
                        bestMove=False
                    
                else:
                    directionChosen='down'
                    if self.game.snake.getDirection()!='up':
                      #  print(directionChosen)
                        bestMove=self.checkDirection(directionChosen)
                    else:
                        bestMove=False
                        '''
            else:
                bestMove=False
                for i in range(2):
                    if not i:
                        #print('wtf')
                        if self.leftOrRight():
                            directionChosen='left'
                            if self.game.snake.getDirection()!='right':
                               # print(directionChosen)
                                bestMove=self.checkDirection(directionChosen)
                            else:
                                bestMove=False
                        else:
                            directionChosen='right'
                            if self.game.snake.getDirection()!='left':
                                #print(directionChosen)
                                bestMove=self.checkDirection(directionChosen)
                            else:
                                bestMove=False
                    if bestMove==False and i:
                        #print('wtf2')
                        if self.upOrDown():
                            directionChosen='up'
                            if self.game.snake.getDirection()!='down':
                                #print(directionChosen)
                                bestMove=self.checkDirection(directionChosen)
                            else:
                                bestMove=False
                            
                        else:
                            directionChosen='down'
                            if self.game.snake.getDirection()!='up':
                              #  print(directionChosen)
                                bestMove=self.checkDirection(directionChosen)
                            else:
                                bestMove=False
                '''
                            
                        

            if bestMove==True:
                self.game.snake.setDirection(directionChosen)
                self.deep-=1
                return True
                   
            elif self.checkDirection(self.game.snake.getDirection())==True:
                self.deep-=1
                return True

            else:
                for direction in self.directions:
                    #print(direction)
                    move=self.checkDirection(direction)

                    if move==True:
                        self.game.snake.setDirection(direction)
                        self.deep-=1
                        return True
                '''
                #print('gotHere')
                for direction in self.directions:
                    #print(direction)
                    if direction == directionChosen:
                        continue
                    move=self.checkDirection(direction)

                    if move==True:
                        self.game.snake.setDirection(direction)
                        self.deep-=1
                        return True
                '''
                
                self.deep-=1
                return False
        else:
            self.deep-=1
            return False
            

    def tick(self):
        if self.game.taskId:
            self.deep=0
            if not self.workOutMove(): #Start looking for a solution
                for direction in self.directions:
                    worked=self.workOutMove()
                    if worked:
                        return
        else:
            if not self.game.running:
                self.game.start()
            
            
            


class FruitGame(SnakeGame):
    def __init__(self,size,pos,inputs=True):
        SnakeGame.__init__(self,size,pos,inputs)

    def start(self):
        self.running=True
        self.score=0
        self.scoreText.setText(['Score: %s' %self.score])

        if self.snake:
            self.snake.removeNode()

        if self.food:
            self.food.removeNode()
            
        self.snake=Snake([random.randint(self.pos[0]+3,self.pos[0]+self.size[0]-4),random.randint(self.pos[1]+3,self.pos[1]+self.size[1]-4)])
        self.snake.render(DisplayDriver.engine)
        self.snake.setDirection(random.choice(['up','down','left','right']))
        
        if self.snake.direction=='up':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX(),self.snake.head.getY()+1]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX(),self.snake.tail.tail[-1].getY()+1]
            self.snake.tail.addSegment(TailSegment())

        elif self.snake.direction=='down':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX(),self.snake.head.getY()-1]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX(),self.snake.tail.tail[-1].getY()-1]
            self.snake.tail.addSegment(TailSegment())
            
        elif self.snake.direction=='left':
            self.snake.tail.lastSegmentPos=[self.snake.head.getX()+1,self.snake.head.getY()]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX()+1,self.snake.tail.tail[-1].getY()]
            self.snake.tail.addSegment(TailSegment())
            
        else:
            self.snake.tail.lastSegmentPos=[self.snake.head.getX()-1,self.snake.head.getY()]
            self.snake.tail.addSegment(TailSegment())
            self.snake.tail.lastSegmentPos=[self.snake.tail.tail[-1].getX()-1,self.snake.tail.tail[-1].getY()]
            self.snake.tail.addSegment(TailSegment())
        
        self.newFood()
        self.countDown()
            
                
DisplayDriver.init()
DisplayDriver.engine.setFrameRate(12)
SnakeGame([40,20],[19,1])
#AI(SnakeGame([40,20],[19,1],inputs=False))
