from DisplayDriver.Input import *
from DisplayDriver import DisplayDriver
from DisplayDriver.Intervals import *
from DisplayDriver.GuiObjects import *
import random
import math
import string
import time

FRAMERATE = 25.0

XCONSTANT = 2.0

class World(Border):
    SIZE = [80,40]
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
    
    def __init__(self,pos = [0,0]):
        Border.__init__(self, [World.SIZE[0],World.SIZE[1]], pos)
        

class Ball(GuiObjectBase):

    def __init__(self, paddles = None, pos=[World.SIZE[0]/2,World.SIZE[1]/2]):
        self.velocity = 25.0
        self.colourlist = [[['\x01\BACKGROUND_GREEN\x02\\O']],
                  [['\x01\BACKGROUND_BLUE\x02\\O']],
                  [['\x01\BACKGROUND_RED\x02\\O']],
                  [['\x01\BACKGROUND_YELLOW\x02\\O']],
                  [['\x01\BACKGROUND_CYAN\x02\\O']],
                  [['O']]
                  ]
        self.newRandomBearing()
        self.colourId = 1
        self.hit = False
        GuiObjectBase.__init__(self,pos,image=[['O']])
        self.paddles = paddles
        self.reset()

    def newRandomBearing(self):
        #self.setBearing(90)
        self.setBearing(random.choice([40,220])+random.random()*100)

    def setBearing(self, bearing):
        while bearing>=360:
            bearing -= 360
        self.bearing = bearing

    def newColour(self):
        image = self.colourlist.pop(0)
        self.setImage(image)
        self.colourlist.append(image)
            
    def calcTrigPos(self, distance):
        
        if self.bearing == 0:
            yPlus = -distance
            xPlus = 0
        elif self.bearing == 90:
            xPlus = distance
            yPlus = 0
        elif self.bearing == 180:
            yPlus = distance
            xPlus = 0
        elif self.bearing == 270:
            xPlus = -distance
            yPlus = 0
        else:
            if self.bearing<90:
                yPlus = -(math.cos(math.radians(self.bearing))*distance)
                xPlus = math.sin(math.radians(self.bearing))*distance
            elif self.bearing<180:
                bearing = math.radians(self.bearing - 90)
                xPlus = math.cos(bearing)*distance
                yPlus = math.sin(bearing)*distance
            elif self.bearing<270:
                bearing = math.radians(self.bearing - 180)
                xPlus = -math.sin(bearing)*distance
                yPlus = math.cos(bearing)*distance
            elif self.bearing<360:
                bearing = math.radians(self.bearing - 270)
                xPlus = - math.cos(bearing)*distance
                yPlus = - math.sin(bearing)*distance

        return self.getX()+xPlus, self.getY()+yPlus

    def reset(self):
        self.setPos([World.SIZE[0]/2,World.SIZE[1]/2])
        self.newRandomBearing()

    def getDistanceFromY(self, y):
        
        if self.bearing%90 == 0:
            return y
        else:
            if self.bearing<90:
                bearing = math.radians(self.bearing)
                return y/math.cos(bearing)
            elif self.bearing<180:
                bearing = math.radians(self.bearing - 90)
                return y/math.sin(bearing)
            elif self.bearing<270:
                bearing = math.radians(self.bearing - 180)
                return y/math.cos(bearing)
            elif self.bearing<360:
                bearing = math.radians(self.bearing - 270)
                return y/math.sin(bearing)

    def getDistanceFromX(self, x):
        if self.bearing%90 == 0:
            return x
        else:
            if self.bearing<90:
                bearing = math.radians(self.bearing)
                return x/math.sin(bearing)
            elif self.bearing<180:
                bearing = math.radians(self.bearing - 90)
                return x/math.cos(bearing)
            elif self.bearing<270:
                bearing = math.radians(self.bearing - 180)
                return x/math.sin(bearing)
            elif self.bearing<360:
                bearing = math.radians(self.bearing - 270)
                return x/math.cos(bearing)

    def getBounceBearing(self, side):
        if side == World.TOP:
            if self.bearing>270:
                return 270-(self.bearing-270)
            else:
                return 90+(90-self.bearing)
            
        elif side == World.RIGHT:
            if self.bearing>90:
                return 270-(self.bearing-90)
            else:
                return 360-self.bearing

        elif side == World.BOTTOM:
            if self.bearing>180:
                return 270+(270-self.bearing)
            else:
                #time.sleep(1)
                return 90-(self.bearing-90)
    
        elif side == World.LEFT:
            if self.bearing>270:
                return 360-self.bearing
            else:
                return 180-(self.bearing-180)

    def checkBounces(self, newX, newY, withPaddles = True):
        if self.paddles and withPaddles:
            rightSide = 3
            leftSide = 2
            
        else:
            rightSide = 2
            leftSide = 1
        
        if newX<=leftSide and newY>1 and newY<World.SIZE[1]-1: # LEFT hit
            distance = self.getDistanceFromX(self.getX()-leftSide)
            newBearing = self.getBounceBearing(World.LEFT)
            side = World.LEFT
            
        elif newY<=1 and newX>1 and newX<World.SIZE[0]-1: # TOP hit
            distance = self.getDistanceFromY(self.getY()-1)
            newBearing = self.getBounceBearing(World.TOP)
            side = World.TOP
            
        elif newX>=World.SIZE[0]-rightSide and newY>1 and newY<World.SIZE[1]-1: # RIGHT hit
            distance = self.getDistanceFromX(World.SIZE[0]-rightSide-self.getX())
            newBearing = self.getBounceBearing(World.RIGHT)
            side = World.RIGHT

        elif newY>=World.SIZE[1]-2 and newX>1 and newX<World.SIZE[0]-1: # BOTTOM hit
            distance = self.getDistanceFromY(World.SIZE[1]-2-self.getY())
            newBearing = self.getBounceBearing(World.BOTTOM)
            side = World.BOTTOM
            
            '''
        elif newY<=1 and newX<=1:
            yDistance = self.getY()-1
            xDistance = self.getX()-1

            if yDistance>xDistance:
                distance = self.getDistanceFromX(xDistance)
                newBearing = self.getBounceBearing(World.LEFT)
            else:
                distance = self.getDistanceFromY(yDistance)
                newBearing = self.getBounceBearing(World.TOP)

        elif newY<=1 and newX>=World.SIZE[0]-2:
            yDistance = self.getY()-1
            xDistance = World.SIZE[0]-2-self.getX()
            
            if yDistance>xDistance:
                distance = self.getDistanceFromX(xDistance)
                newBearing = self.getBounceBearing(World.RIGHT)
            else:
                distance = self.getDistanceFromY(yDistance)
                newBearing = self.getBounceBearing(World.TOP)

        elif newY>=World.SIZE[1]-2 and newX>=World.SIZE[0]-2:
            yDistance = World.SIZE[1]-2-self.getY()
            xDistance = World.SIZE[0]-2-self.getX()
            
            if yDistance>xDistance:
                distance = self.getDistanceFromX(xDistance)
                newBearing = self.getBounceBearing(World.RIGHT)
            else:
                distance = self.getDistanceFromY(yDistance)
                newBearing = self.getBounceBearing(World.BOTTOM)

        elif newY>=World.SIZE[1]-2 and newX<=1:
            yDistance = World.SIZE[1]-2-self.getY()
            xDistance = self.getX()-1
            
            if yDistance>xDistance:
                distance = self.getDistanceFromX(xDistance)
                newBearing = self.getBounceBearing(World.LEFT)
            else:
                distance = self.getDistanceFromY(yDistance)
                newBearing = self.getBounceBearing(World.BOTTOM)
                '''
        else:
            return False, False, False

        return distance, newBearing, side
        
    def nextPos(self):
        newBearing = self.bearing
        distance = self.velocity/FRAMERATE
        oldDistance = distance
        
        while True:
            
            newX, newY = self.calcTrigPos(distance)
            newDistance, newBearing, side = self.checkBounces(newX, newY)
            
            if not newDistance:
                self.setPos(newX, newY)
                return
            
            else:
                distance = distance - newDistance
                #self.newColour()
                newX, newY = self.calcTrigPos(distance)
                if side in [World.LEFT, World.RIGHT] and self.paddles:
                    if ((newY<=self.paddles[0].getY() or newY>=self.paddles[0].getY()+Paddle.SIZE) and side == World.LEFT):
                        distance = self.getDistanceFromX(self.getX()-1)
                        self.setPos(self.calcTrigPos(distance))
                        self.hit = side
                        return False

                    elif ((newY<=self.paddles[1].getY() or newY>=self.paddles[1].getY()+Paddle.SIZE) and side == World.RIGHT):
                        distance = self.getDistanceFromX(World.SIZE[0]-2-self.getX())
                        self.setPos(self.calcTrigPos(distance))
                        self.hit = side
                        return False
                    self.velocity*=1.05
                        
                self.setPos(newX, newY)
                self.setBearing(newBearing)
                distance = oldDistance - distance

    def getHit(self):
        return self.hit

    def tick(self):
        self.nextPos()

    def destroy(self):
        self.removeNode()

class Paddle(GuiObjectBase):
    SIZE = 5
    LOOK = [['#']]*SIZE
    SPEED = 1
    def __init__(self, side):
        if side == World.RIGHT:
            pos = [World.SIZE[0]-2,int(World.SIZE[1]/2)-int(Paddle.SIZE/2)]
        else:
            pos = [1,int(World.SIZE[1]/2)-int(Paddle.SIZE/2)]

        self.score = 0
        
        GuiObjectBase.__init__(self, image=Paddle.LOOK, pos = pos)

    def moveUp(self):
        newY = self.getY() - Paddle.SPEED
        if newY<1:
            return
        else:
            self.setY(newY)

    def moveDown(self):
        newY = self.getY() + Paddle.SPEED
        if (newY+Paddle.SIZE)>World.SIZE[1]-1:
            return
        else:
            self.setY(newY)

    def incrementScore(self):
        self.score += 1

    def getScore(self):
        return self.score

class Pong(object):

    def __init__(self):
        
        self.restartSequence = Sequence(DisplayDriver.engine,
                                        Wait(2),
                                        Func(self.newBall),
                                        Func(self.startTask),
                                        Wait(2),
                                        Func(self.restart))
        
        self.player1 = Paddle(World.LEFT)
        self.player1.render(DisplayDriver.engine)
        self.player2 = Paddle(World.RIGHT)
        self.player2.render(DisplayDriver.engine)

        self.player1Score = OnscreenText(text = '0', pos = [1+(World.SIZE[0]-2)*0.25,1])
        self.player1Score.render(DisplayDriver.engine)
        self.player2Score = OnscreenText(text = '0', pos = [1+(World.SIZE[0]-2)*0.75,1])
        self.player2Score.render(DisplayDriver.engine)
        
        self.world = World()
        self.world.render(DisplayDriver.engine)

        self.ball = None
        self.roundRunning = False
        
        self.p1Up = False
        self.p1Down = False
        self.p2Up = False
        self.p2Down = False
        
        Input.bindAll(self.handleKeyDown)
        Input.bindAllRelease(self.handleKeyUp)

        self.newBall()
        
        Sequence(DisplayDriver.engine,
                 Wait(2),
                 Func(self.restart)
                 ).start()

        self.startTask()
        
        Input.mainLoop()

    def newBall(self):
        if self.ball:
            self.ball.destroy()
        self.ball = Ball([self.player1, self.player2])
        self.ball.render(DisplayDriver.engine)
        

    def handleKeyDown(self, key):
        if key == KeyCode.W:
            self.p1Up = True
        elif key == KeyCode.S:
            self.p1Down = True
        elif key == KeyCode.UPARROW:
            self.p2Up = True
        elif key == KeyCode.DOWNARROW:
            self.p2Down = True

    def handleKeyUp(self, key):
        if key == KeyCode.W:
            self.p1Up = False
        elif key == KeyCode.S:
            self.p1Down = False
        elif key == KeyCode.UPARROW:
            self.p2Up = False
        elif key == KeyCode.DOWNARROW:
            self.p2Down = False

    def handleMovement(self):
        if self.p1Up:
            self.player1.moveUp()

        if self.p1Down:
            self.player1.moveDown()

        if self.p2Up:
            self.player2.moveUp()

        if self.p2Down:
            self.player2.moveDown()

    def startTask(self):
        self.taskId = DisplayDriver.engine.addTask(self.tick)

    def restart(self):
        self.roundRunning = True

    def roundOver(self):
        sideHit = self.ball.getHit()
        self.roundRunning = False
        DisplayDriver.engine.removeTask(self.taskId)
        
        if sideHit == World.RIGHT:
            self.player1.incrementScore()
            self.player1Score.setText(str(self.player1.getScore()))
        else:
            self.player2.incrementScore()
            self.player2Score.setText(str(self.player2.getScore()))

        self.restartSequence.start()

    def tick(self):
        self.handleMovement()
        if self.ball:
            
            if self.roundRunning:
                self.ball.tick()
                
            if self.ball.getHit() != False:
                self.roundOver()

DisplayDriver.engine.graphics.setRes(World.SIZE)
DisplayDriver.engine.setFrameRate(FRAMERATE)
DisplayDriver.init()

p = Pong()


