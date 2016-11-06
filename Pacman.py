from DisplayDriver import DisplayDriver
from DisplayDriver.GuiObjects import *
from DisplayDriver import Colours
from DisplayDriver.Input import *
from DisplayDriver.Intervals import *
import random
import time

class MOVES:
    UP = [0, -1]
    RIGHT = [2, 0]
    DOWN = [0, 1]
    LEFT = [-2, 0]
    MOVES = [UP,
             DOWN,
             LEFT,
             RIGHT
             ]


class World(GuiObjectBase):

    def __init__(self, worldNum = 0, pos = [0,0]):
        self.worldNum = worldNum
        self.allWorldsAttributes = []
        self.loadBackgrounds()
        self.worldAttributes = {}
        self.world = self.worlds[self.worldNum]
        self.worldAttributes = self.allWorldsAttributes[self.worldNum]
        GuiObjectBase.__init__(self,pos[:],self.world)
        self.layer = 0

    def loadBackgrounds(self):
        self.worlds = []
        with open("Worlds.txt") as worldsFile:
            for line in worldsFile.readlines():
                line = line.replace('\n','')
                if 'newLevel' in line:
                    self.allWorldsAttributes.append({})
                    attributes = line.strip().split('newLevel')[1].split(',')
                    
                    self.allWorldsAttributes[-1]['GhostsSpawn'] = [int(attributes[0]), int(attributes[1])]
                    self.allWorldsAttributes[-1]['PlayerSpawn'] = [int(attributes[2]), int(attributes[3])]
                    self.allWorldsAttributes[-1]['LeftSide'] = [int(attributes[4]), int(attributes[5])]
                    self.allWorldsAttributes[-1]['RightSide'] = [int(attributes[6]), int(attributes[7])]

                    self.worlds.append([])
                    continue
                self.worlds[-1].append(list(line))

    def getGhostSpawn(self):
        return self.worldAttributes['GhostsSpawn'][:]

    def getPlayerSpawn(self):
        return self.worldAttributes['PlayerSpawn'][:]
    
    def getTeleports(self):
        return self.worldAttributes['LeftSide'][:],self.worldAttributes['RightSide'][:]

    def getCharFromPos(self, pos):
        if (pos[1]-self.getY())>=len(self.world) or (pos[0]-self.getX())>=len(self.world[0]):
            return None
        return self.world[pos[1]-self.getY()][pos[0]-self.getX()]
    
    def isCollision(self, pos):
        character = self.getCharFromPos(pos)
        if character == '#':
            return True
        else:
            return False

    def isGate(self, pos):
        characters = []
        for i in range(-2, 2): 
            characters.append(self.getCharFromPos([pos[0]+i,pos[1]]))
            
        if '-' in characters:
            return True
        else:
            return False

    def isFood(self, pos):
        character = self.getCharFromPos(pos)
        if character == '.':
            return True
        else:
            return False

    def isSpecial(self, pos):
        character = self.getCharFromPos(pos)
        if character == '*':
            return True
        else:
            return False

    def isFlee(self, pos):
        character = self.getCharFromPos(pos)
        if character == 'O':
            return True
        else:
            return False

    def hasWon(self):
        for line in self.world:
            if '.' in line or '*' in line or 'O' in line:
                return False
        return True

    def eat(self, pos):
        self.world[pos[1]-self.getY()][pos[0]-self.getX()] = ' '

class Entity(GuiObjectBase):
    
    def __init__(self, pos, look):
        self.currentMove = None
        self.tryMove = None
        self.lastPos = pos
        GuiObjectBase.__init__(self, pos, look)

    def queueMove(self, move):
        self.tryMove = move

    def move(self, move):
        if move:
            self.lastPos = self.getPos()
            x = self.getX() + move[0]
            y = self.getY() + move[1]
            self.setPos(x,y)

    def getLastPos(self):
        return self.lastPos

    def resetMoves(self):
        self.queuedMoves = []

    def undoMove(self):
        self.setPos(self.lastPos)

    def tick(self):
        self.move()

class Player(Entity):
    def __init__(self, pos = [0,0]):
        Entity.__init__(self, pos, [['\x01\FOREGROUND_YELLOW\x02\\'+'C']])
        self.frame = 0

    def nextFrame(self):
        self.frame += 1
        if self.frame:
            self.setImage([['\x01\FOREGROUND_YELLOW\x02\\'+'G']])
            self.frame = -1
        else:
            self.setImage([['\x01\FOREGROUND_YELLOW\x02\\'+'C']])
        
        

class Ghost(Entity):
    COLOURS = ['\x01\FOREGROUND_GREEN\x02\\',
               '\x01\FOREGROUND_RED\x02\\',
               '\x01\FOREGROUND_CYAN\x02\\',
               '\x01\FOREGROUND_MAGENTA\x02\\'
               ]
               
    def __init__(self, pos = [0,0], colour = 0):
        self.flee = False
        self.hasAccess = True
        if colour>=len(self.COLOURS):
            colour = random.randint(0,3)
        Entity.__init__(self, pos, [[self.COLOURS[colour]+'A']])
        self.layer=2

    def pickMove(self):
        self.queueMove(random.choice(MOVES.MOVES)) #random Up Down Left Right

    def fleeMode(self):
        self.flee = True

    def attackMode(self):
        self.flee = False

class Game(object):
    numGhosts = 4
    def __init__(self, pos = [0,0], worldNum = 0, engine = None):
        self.engine = engine
        self.pos = pos
        self.worldNum = worldNum
        self.renderer = None
        self.gameOver = False
        self.score = 0
        self.ghosts = []
        self.player = None
        self.world = None
        self.gameSpeed = 1
        self.tickNum = 0
        self.lives = 2
        self.scoreText = OnscreenText(pos = [pos[0]+50 , pos[1]+20], text = 'Score: 0')
        self.generateLevel()
        self.livesText = OnscreenText(pos = [pos[0]+50, pos[1]+19], text = 'Lives: '+str(self.lives))
        self.gameOverText = OnscreenText(text = 'Game over', pos = [self.pos[0]+len(self.world.world[0])/2-len('Game over')/2 ,self.pos[1]+len(self.world.world)/2])

    def resetGhosts(self):
        for ghost in self.ghosts:
            ghost.removeNode()
        self.ghosts = []

    def resetLevel(self):
        self.resetGhosts()
        
        if self.player:
            self.player.removeNode()
        self.player = None

        if self.world:
            self.world.removeNode()
        self.world = None

        self.generateLevel()

    def generateLevel(self):
        self.world = World(self.worldNum, self.pos)
        self.player = Player()
        self.ghosts=[]
        for i in range(self.numGhosts):
            self.ghosts.append(Ghost([0, 0], i))

    def isGhost(self, pos):
        for ghost in self.ghosts:
            if ghost.getPos() == pos:
                return True
        return False

    def isPlayer(self, pos):
        if self.player.getPos() == pos:
            return True
        else:
            return False

    def spawnGhost(self, ghost):
        startCoords = self.world.getGhostSpawn()
        ghost.setPos(self.pos[0]+startCoords[0], self.pos[1]+startCoords[1])
        
    def spawnPlayer(self):
        startCoords = self.world.getPlayerSpawn()
        self.player.setPos(self.pos[0]+startCoords[0], self.pos[1]+startCoords[1])

    def spawnGhosts(self):
        for ghost in self.ghosts:
            self.spawnGhost(ghost)
    
    def restartGame(self):
        for ghost in self.ghosts:
            ghost.attackMode()
        self.spawnGhosts()
        self.spawnPlayer()

    def death(self):
        self.renderer.removeTask(self.taskId)
        self.lives -= 1
        if self.lives<0:
            self.gameOverSequence()
        else:
            deathSequence = Sequence(DisplayDriver.engine)
            for i in range(3):
                p = Parallel()
                p.append(Func(self.player.hide))
                for ghost in self.ghosts:
                    p.append(Func(ghost.show))
                deathSequence.append(p)
                
                deathSequence.append(Wait(0.5))
                
                p = Parallel()
                p.append(Func(self.player.show))
                for ghost in self.ghosts:
                    p.append(Func(ghost.hide))
                deathSequence.append(p)
                deathSequence.append(Wait(0.5))

            p = Parallel()
            p.append(Func(self.player.show))
            for ghost in self.ghosts:
                p.append(Func(ghost.show))
            deathSequence.append(p)

            deathSequence.append(Wait(2))
            deathSequence.append(Func(self.start))
            deathSequence.start()
        

    def isKilled(self):
        for ghost in self.ghosts:
            if ghost.getPos() == self.player.getPos():
                return True
        return False

    def toWorldPos(self, pos):
        return [pos[0]-self.pos[0], pos[1]-self.pos[1]]

    def toScreenPos(self, pos):
        return [pos[0]+self.pos[0], pos[1]+self.pos[1]]

    def checkAndHandleTeleport(self, entity):
        if self.toWorldPos(entity.getPos()) == self.world.getTeleports()[0]:
            entity.setPos(self.toScreenPos([self.world.getTeleports()[1][0]-2,self.world.getTeleports()[1][1]]))
        elif self.toWorldPos(entity.getPos()) == self.world.getTeleports()[1]:
            entity.setPos(self.toScreenPos([self.world.getTeleports()[0][0]+2,self.world.getTeleports()[0][1]]))

    def moveGhost(self, ghost):
        lastPos = ghost.getPos()
        if not ghost.tryMove:
            ghost.pickMove()
        ghost.move(ghost.tryMove)
        
        if self.world.isCollision(ghost.getPos()):
            ghost.setPos(lastPos)
        else:
            if self.world.isGate(ghost.getPos()):
                if ghost.hasAccess:
                    ghost.hasAccess = False
                else:
                    ghost.setPos(lastPos)
                    
            if ghost.getPos() != lastPos:
                ghost.currentMove = ghost.tryMove
                ghost.pickMove()
            
        while True:
            if ghost.getPos() != lastPos:
                break
            else:
                if not ghost.currentMove:
                    ghost.pickMove()
                    ghost.currentMove = ghost.tryMove
                    while True:
                        ghost.pickMove()
                        if ghost.currentMove == MOVES.RIGHT and ghost.tryMove == MOVES.LEFT:
                            continue
                        elif ghost.currentMove == MOVES.LEFT and ghost.tryMove == MOVES.RIGHT:
                            continue
                        elif ghost.currentMove == MOVES.UP and ghost.tryMove == MOVES.DOWN:
                            continue
                        elif ghost.currentMove == MOVES.DOWN and ghost.tryMove == MOVES.UP:
                            continue
                        else:
                            break
                    

                ghost.move(ghost.currentMove)
                if self.world.isCollision(ghost.getPos()):
                    ghost.currentMove = None
                    ghost.setPos(lastPos)
                    
        self.checkAndHandleTeleport(ghost)

    def setGameOver(self):
        self.gameOver=True

    def tick(self):
        self.tickNum += 1
        if self.tickNum<(3/self.gameSpeed):
            pass
            return
        else:
            self.tickNum = 0
        
        lastPos = self.player.getPos()
        
        if self.player.tryMove:
            self.player.move(self.player.tryMove)

            if self.world.isCollision(self.player.getPos()) or self.world.isGate(self.player.getPos()):
                self.player.setPos(lastPos)
                
            else:
                self.player.currentMove = self.player.tryMove
                self.player.tryMove = None
                
        if self.player.currentMove and self.player.getPos() == lastPos:
            self.player.move(self.player.currentMove)
            if self.world.isCollision(self.player.getPos()):
                self.player.setPos(lastPos)
                self.player.currentMove = None
                
            if self.world.isGate(self.player.getPos()):
                self.player.setPos(lastPos)
                self.player.currentMove = None

        if self.world.isSpecial(self.player.getPos()):
            self.score+=2
            self.world.eat(self.player.getPos())
            
        elif self.world.isFood(self.player.getPos()):
            self.world.eat(self.player.getPos())
            self.score+=1

        self.checkAndHandleTeleport(self.player)
        if self.player.getPos() != lastPos:
            self.player.nextFrame()

        if self.isKilled():
            self.death()
            return

        for ghost in self.ghosts:
            self.moveGhost(ghost)

        if self.isKilled():
            self.death()
            return  

        self.scoreText.setText('Score: '+str(self.score))
        
        self.livesText.setText('Lives: '+str(self.lives))

    def gameOverSequence(self):
        FADELENGTH = 1
        self.world.removeNode()
        sequences=[]
        multiplier=1

        for i in range(len(self.world.world)):
            for j in range(len(self.world.world[i])):
                
                pos = [self.pos[0]+j, self.pos[1]+i]
                character = GuiObjectBase(pos = pos, image = self.world.world[i][j])
                character.layer=0
                character.render(DisplayDriver.engine)
                sequences.append(Sequence(DisplayDriver.engine))
                sequences[-1].append(Wait(random.random()*FADELENGTH))
                sequences[-1].append(Func(character.removeNode))

        for ghost in self.ghosts:
            sequences.append(Sequence(DisplayDriver.engine))
            sequences[-1].append(Wait(random.random()*FADELENGTH))
            sequences[-1].append(Func(ghost.removeNode))

        sequences.append(Sequence(DisplayDriver.engine))
        sequences[-1].append(Wait(FADELENGTH)) 
        sequences[-1].append(Func(self.player.removeNode))
        sequences[-1].append(Func(self.gameOverText.render,DisplayDriver.engine))
        sequences[-1].append(Func(self.setGameOver))

        for sequence in sequences:
            sequence.start()
            
    def start(self):
        self.restartGame()
        self.taskId = self.renderer.addTask(self.tick)
        

    def render(self, renderer):
        self.renderer = renderer
        for ghost in self.ghosts:
            ghost.render(renderer)

        if self.player:
            self.player.render(renderer)

        if self.world:
            pass
            self.world.render(renderer)
        self.livesText.render(renderer)
        self.scoreText.render(renderer)

    def destroy(self):
        for ghost in self.ghosts:
            ghost.removeNode()
            
        if self.player:
            self.player.removeNode()

        if self.world:
            self.world.removeNode()

        self.scoreText.removeNode()

        self.livesText.removeNode()

        self.gameOverText.removeNode()

        self.renderer = None
        
            

class Pacman:
    def __init__(self):
        self.game = None
        self.restart()
        Input.bindAll(self.takeInput)
        Input.mainLoop()

    def restart(self):
        if self.game:
            self.game.destroy()
        self.game = Game([0,0],0,DisplayDriver.engine)
        self.game.render(DisplayDriver.engine)
        self.game.start()

    def gameInput(self, move):
        if self.game:
            self.game.player.queueMove(move)

    def menuInput(self, inputKey):
        pass

    def takeInput(self, inputKey):
        
        if inputKey == KeyCode.UPARROW:
            self.gameInput(MOVES.UP)
            self.menuInput(inputKey)
        
        elif inputKey == KeyCode.LEFTARROW:
            self.gameInput(MOVES.LEFT)
        
        elif inputKey == KeyCode.RIGHTARROW:
            self.gameInput(MOVES.RIGHT)
        
        elif inputKey == KeyCode.DOWNARROW:
            self.gameInput(MOVES.DOWN)
            self.menuInput(inputKey)

        elif inputKey == KeyCode.RETURN:
            if self.game:
                if self.game.gameOver:
                    self.restart()
        elif inputKey == KeyCode.D:
            DisplayDriver.debug.toggle()
            
DisplayDriver.init()
DisplayDriver.engine.setFrameRate(12)
DisplayDriver.debug.toggle()
Pacman()
 

