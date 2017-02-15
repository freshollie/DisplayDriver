from DisplayDriver import DisplayDriver
from DisplayDriver.Intervals import *
from DisplayDriver.Input import *
import random
import winsound
from DisplayDriver.GuiObjects import *

BLOCKCHAR = chr(178)

try:
    xrange
except NameError:
    xrange = range


class Block(GuiObjectBase):
    '''
    Base of what goes to make a block.
    This Class will be a parent to any
    block that is created
    '''

    def __init__(self):
        GuiObjectBase.__init__(self)
        self[0] = self.images[0]
        self.imageIndex = 0

    def rotateRight(self):
        if self.imageIndex < 3:
            self.imageIndex += 1
        else:
            self.imageIndex = 0
        self[0] = self.images[self.imageIndex][:]

    def rotateLeft(self):
        if self.imageIndex > 0:
            self.imageIndex -= 1
        else:
            self.imageIndex = 3
        self[0] = self.images[self.imageIndex][:]

    def moveDown(self):
        self.setY(self.getY() + 1)

    def moveLeft(self):
        self.setX(self.getX() - 1)

    def moveRight(self):
        self.setX(self.getX() + 1)

    def getRightPos(self):
        return self.getX() + len(self[0][0])

    def getLowestPos(self):
        return self.getY() + len(self[0])


class LBlock(Block):
    '''
    L Block class with the shape:

    #
    #
    ##
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR,
                         DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, DisplayDriver.BACKGROUNDCHAR,
                         '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_GREY\x02\\' + BLOCKCHAR]
                        ]
                       ]
        Block.__init__(self)


class LBlockReflected(Block):
    '''
    L Block Reflected with the shape:

     #
     #
    ##
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR,
                         DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [['\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, DisplayDriver.BACKGROUNDCHAR,
                         '\x01\BACKGROUND_INTENSITY\BACKGROUND_BLUE\x02\\' + BLOCKCHAR]
                        ]
                       ]
        Block.__init__(self)


class SquareBlock(Block):
    '''
    Square block with insidentally doesn't
    have any differnt rotations but they
    need to be definined in order to not
    have to change the functions for rotation
    inherited from Block.

    The shape of this is:

    ##
    ##
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_GREEN\x02\\' + BLOCKCHAR]
                        ]
                       ]
        Block.__init__(self)


class LineBlock(Block):
    '''
    Line Block class which only has 2
    states for rotation but just like
    the square block 4 are defined
    anyway.

    The shape is:

    ####
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_RED\x02\\' + BLOCKCHAR]
                        ]
                       ]
        Block.__init__(self)


class SBlock(Block):
    '''
    S Block with the shape:

     ##
    ##
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_MAGENTA\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR]
                        ]
                       ]
        Block.__init__(self)


class SBlockReflected(Block):
    '''
    S Block Reflected with the shape:

    ##
     ##
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR, ],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [['\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR, ],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_CYAN\x02\\' + BLOCKCHAR]
                        ]
                       ]
        Block.__init__(self)


class CrossBlock(Block):
    '''
    Cross Block with the shape:

    #
    ##
    #
    '''

    def __init__(self, initPos):
        self.initPos = initPos[:]
        self.images = [[['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, DisplayDriver.BACKGROUNDCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR],
                        ['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR]
                        ],

                       [[DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR],
                        ['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR]
                        ],

                       [['\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR,
                         '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR],
                        [DisplayDriver.BACKGROUNDCHAR, '\x01\BACKGROUND_YELLOW\x02\\' + BLOCKCHAR,
                         DisplayDriver.BACKGROUNDCHAR]
                        ]
                       ]
        Block.__init__(self)


class Stack(GuiObjectBase):
    '''
    This object is used to represent the stacked
    blocks. It also controls weather a block is
    allowed to perform a move.
    '''

    def __init__(self, pos=[0, 0], size=[20, 20]):
        GuiObjectBase.__init__(self, pos)
        self.size = size[:]

        self.emptyBoard()

    def emptyBoard(self):
        self[0] = []
        for y in range(self.size[1] - 2):
            self[0].append([])
            for x in range(self.size[0] - 2):
                self[0][-1].append(DisplayDriver.BACKGROUNDCHAR)
        for i in range(4):
            self[0][i] = [DisplayDriver.BACKGROUNDCHAR] * (self.size[0] - 2)

    def addToStack(self, blockObject):
        for y in range(len(blockObject[0])):
            for x in range(len(blockObject[0][y])):
                stackPos = self.getStackCoordFromObject(blockObject, x, y)
                if blockObject[0][y][x] != DisplayDriver.BACKGROUNDCHAR:
                    self[0][stackPos[1]][stackPos[0]] = blockObject[0][y][x]

    def getStackCoordFromObject(self, object, x, y):
        return [object.getX() - self.getX() + x, object.getY() - self.getY() + y]

    def isColliding(self, object):
        for y in range(len(object[0])):
            for x in range(len(object[0][y])):
                realPos = self.getStackCoordFromObject(object, x, y)
                if object[0][y][x] != DisplayDriver.BACKGROUNDCHAR and realPos[1] + 1 >= len(self[0]):
                    return True
                elif object[0][y][x] != DisplayDriver.BACKGROUNDCHAR and self[0][realPos[1] + 1][
                    realPos[0]] != DisplayDriver.BACKGROUNDCHAR:
                    return True

        return False

    def canMove(self, direction, object):
        for y in range(len(object[0])):
            for x in range(len(object[0][y])):
                objectX = object.getX() + x + direction
                maxRight = self.getX() + len(self[0][0])
                realPos = self.getStackCoordFromObject(object, x, y)
                if object.getX() + direction < self.getX() or objectX >= maxRight:
                    return False
                elif realPos[1] > len(self[0]) - 1:
                    return False
                elif realPos[0] + direction > len(self[0][realPos[1]]) - 1:
                    return False
                elif object[0][y][x] != DisplayDriver.BACKGROUNDCHAR and self[0][realPos[1]][
                            realPos[0] + direction] != DisplayDriver.BACKGROUNDCHAR:
                    return False
        return True

    def isGameOver(self):
        returnValue = False
        for pixel in self[0][0]:
            if pixel != DisplayDriver.BACKGROUNDCHAR:
                returnValue = True
        return returnValue

    def removeLine(self, lineNum):
        del self[0][lineNum]
        self[0].insert(0, [DisplayDriver.BACKGROUNDCHAR] * (self.size[1] - 5))

    def produceLineAnimation(self, lineNum, score):
        linePos = [self.getX() + int(self.size[0] / 2), self.getY() + lineNum]
        text = OnscreenText([str(score)], linePos)

        scoreSequence = Sequence(DisplayDriver.engine,
                                 Func(text.render, DisplayDriver.engine))

        for i in range(1, 10):
            scoreSequence.append(Parallel(Func(text.setX, linePos[0] + i),
                                          Func(text.setY, linePos[1] - i)
                                          ))
        scoreSequence.append(Func(text.removeNode))
        scoreSequence.start()

    def checkLines(self):
        score = 0
        lines = 0
        for i in range(2):
            for lineNum in range(len(self[0])):
                if DisplayDriver.BACKGROUNDCHAR not in self[0][lineNum]:
                    self.produceLineAnimation(lineNum, score + 100)
                    self.removeLine(lineNum)
                    score += score + 100
                    lines += 1
        return score, lines


class ScoreBoard(TextBox):
    def __init__(self, pos):
        TextBox.__init__(self, pos, [9, 6],
                         background=DisplayDriver.BACKGROUNDCHAR)  # ,chars=[DisplayDriver.BACKGROUNDCHAR,'|','-','_'])
        self.setLine(0, 'Score:')
        self.setLine(1, '0')
        self.setLine(3, 'Lines:')
        self.setLine(4, '0')
        self.score = 0
        self.lines = 0
        self.rendered = None

    def add(self, score, lines):
        self.score += score
        self.lines += lines
        self.update()

    def update(self):
        self.setLine(1, str(self.score))
        self.setLine(4, str(self.lines))

    def reset(self):
        self.score = 0
        self.lines = 0
        self.update()


class TetrisMenuBackground(object):
    BLOCK_TYPES = (LBlock,
                   LBlockReflected,
                   SquareBlock,
                   LineBlock,
                   SBlock,
                   SBlockReflected,
                   CrossBlock
                   )

    def __init__(self):
        self.blocks = []
        self.taskId = None

    def genRandomBlock(self):
        self.blocks.append(random.choice(TetrisMenuBackground.BLOCK_TYPES)([random.randint(0, 80), -4]))
        self.blocks[-1].setPos([random.randint(0, 80), -4])
        self.blocks[-1].layer = 0  # Background layer
        self.blocks[-1].render(DisplayDriver.engine)

    def tick(self):
        self.genRandomBlock()

        for block in self.blocks:
            block.setY(block.getY() + 1)
            if block.getY() > 24:
                block.removeNode()
                self.blocks.remove(block)

    def start(self):
        if not self.taskId:
            self.taskId = DisplayDriver.engine.addTask(self.tick)

    def stop(self):
        DisplayDriver.engine.removeTask(self.taskId)
        self.taskId = None
        for block in self.blocks:
            block.removeNode()
        self.blocks = []


class HelpScreen(object):
    def __init__(self):
        self.title = OnscreenText(
            [
                '#__##__##########___##############'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                '/\\ \\/\\ \\########/\\_ \\#############'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                '\\ \\ \\_\\ \\#####__\\//\\ \\####_____###'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                "#\\ \\  _  \\##/'__`\\\\ \\ \\##/\\ '__`\\#".replace('#', DisplayDriver.BACKGROUNDCHAR),
                "##\\ \\ \\ \\ \\/\\  __/#\\_\\ \\_\\ \\ \\L\\ \\".replace('#', DisplayDriver.BACKGROUNDCHAR),
                '###\\ \\_\\ \\_\\ \\____\\/\\____\\\\ \\ ,__/'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                '####\\/_/\\/_/\\/____/\\/____/#\\ \\ \\/#'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                '############################\\ \\_\\#'.replace('#', DisplayDriver.BACKGROUNDCHAR),
                '#############################\\/_/#'.replace('#', DisplayDriver.BACKGROUNDCHAR)
             ],
            [14, 0])
        self.title.setPos([21, 0, ])

        self.text = []
        self.text.append(OnscreenText(['Up Arrow: Rotate block right'], [40, 10]))
        self.text[0].setPos([25, 14])
        self.text.append(OnscreenText(['Down Arrow: Move Block Down'], [40, 11]))
        self.text[1].setPos([25, 15])
        self.text.append(OnscreenText(['Left Arrow: Move Block Left'], [40, 12]))
        self.text[2].setPos([25, 16])
        self.text.append(OnscreenText(['Right Arrow: Move Block Right'], [40, 13]))
        self.text[3].setPos([25, 17])
        self.text.append(OnscreenText(['Escape: Back to main menu'], [40, 14]))
        self.text[4].setPos([25, 18])

    def render(self, renderer):
        self.title.render(renderer)
        for text in self.text:
            text.render(renderer)

    def removeNode(self):
        self.title.removeNode()
        for text in self.text:
            text.removeNode()

    def show(self):
        self.title.show()
        for text in self.text:
            text.show()

    def hide(self):
        self.title.hide()
        for text in self.text:
            text.hide()


class Tetris(object):
    '''
    Main game object
    '''

    blockTypes = (LBlock, LBlockReflected, SquareBlock, LineBlock, SBlock, SBlockReflected, CrossBlock)

    def __init__(self, size=[20, 20], pos=[0, 0]):
        DisplayDriver.engine.setTitle('Tetris')
        self.stage = None

        self.border = Border(size,
                             pos=pos[:],
                             chars=['<!', '!>', '-V', '_'],
                             corners=[DisplayDriver.BACKGROUNDCHAR,
                                      DisplayDriver.BACKGROUNDCHAR,
                                      DisplayDriver.BACKGROUNDCHAR,
                                      DisplayDriver.BACKGROUNDCHAR
                                      ]
                             )
        self.border.render(DisplayDriver.engine)

        self.border2 = Border([14, 8],
                              pos=[pos[0] - 14,
                                   pos[1]
                                   ]
                              )
        self.border2.render(DisplayDriver.engine)

        self.score = ScoreBoard([pos[0] + size[0],
                                 pos[1]])
        self.score.render(DisplayDriver.engine)

        self.stack = Stack([pos[0] + 1, 1], size)
        self.stack.render(DisplayDriver.engine)

        self.helpPage = HelpScreen()
        self.helpPage.render(DisplayDriver.engine)

        self.gameOverText = OnscreenText([
            ' _______  _______  _______  _______    _______           _______  _______',
            '(  ____ \(  ___  )(       )(  ____ \  (  ___  )|\     /|(  ____ \(  ____ )',
            '| (    \/| (   ) || () () || (    \/  | (   ) || )   ( || (    \/| (    )|',
            '| |      | (___) || || || || (__      | |   | || |   | || (__    | (____)|',
            '| | ____ |  ___  || |(_)| ||  __)     | |   | |( (   ) )|  __)   |     __)',
            '| | \_  )| (   ) || |   | || (        | |   | | \ \_/ / | (      | (\ (   ',
            '| (___) || )   ( || )   ( || (____/\  | (___) |  \   /  | (____/\| ) \ \__',
            '(_______)|/     \||/     \|(_______/  (_______)   \_/   (_______/|/   \__/',
            '                                                                          ',
            '                          Press Enter To Continue                         '
        ]
            , pos=[3, 6]
        )

        self.gameOverText.render(DisplayDriver.engine)
        self.gameOverText.hide()

        self.nextBlockText = OnscreenText(['Next Block'], pos=[pos[0] - 12, pos[1] + 1])
        self.nextBlockText.render(DisplayDriver.engine)

        self.menu = ChoiceMenu([Choice('Start', self.start),
                                Choice('About', self.showAbout),
                                Choice('Help', self.showHelp)],
                               ['>', '<'],
                               [38, 15])
        self.menu.render(DisplayDriver.engine)

        self.animatedBackground = TetrisMenuBackground()

        self.titleText = OnscreenText([
            '#_______##_______##_______##______####___###_______#'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '|       ||       ||       ||    _ |##|   |#|       |'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '|_     _||    ___||_     _||   |#||##|   |#|  _____|'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '##|   |##|   |___###|   |##|   |_||_#|   |#| |_____#'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '##|   |##|    ___|##|   |##|    __  ||   |#|_____  |'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '##|   |##|   |___###|   |##|   |##| ||   |##_____| |'.replace('#', DisplayDriver.BACKGROUNDCHAR),
            '##|___|##|_______|##|___|##|___|##|_||___|#|_______|'.replace('#', DisplayDriver.BACKGROUNDCHAR)
        ]
            , pos=[14, 5]
        )
        self.titleText.render(DisplayDriver.engine)

        try:
            # winsound.PlaySound('Tetris Remix.wav',winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
            pass
        except:  # Sound hasn't been downloaded
            pass

        self.nextBlock = None
        self.size = size[:]
        self.pos = pos[:]
        self.block = None
        self.running = False
        self.down = False
        self.left = False
        self.right = False
        self.rotate = False
        self.enterKey = False
        self.oldBlock = None
        self.newBlock()

        self.hide()
        self.loadMenu()

        self.setUpKeyInputs()

    def workOutInput(self, event):
        if event == KeyCode.DOWNARROW:
            if self.stage == 1:
                self.down = True
            elif self.stage == 0:
                self.menu.nextChoice()

        elif event == KeyCode.UPARROW:
            if self.stage == 1:
                self.rotate = True
            elif self.stage == 0:
                self.menu.previousChoice()

        elif event == KeyCode.LEFTARROW:
            self.left = True

        elif event == KeyCode.RIGHTARROW:
            self.right = True

        elif event == KeyCode.ESCAPE:
            self.exit()

        elif event == KeyCode.RETURN:
            if self.stage == 2:
                self.loadMenu()
            elif self.stage == 0:
                self.menu.selectChoice()
            else:
                self.enterKey = True

        elif event == KeyCode.D:
            if not DisplayDriver.debug.running:
                DisplayDriver.debug.start()
            else:
                DisplayDriver.debug.stop()

        else:
            pass

    def releaseInput(self, event):
        if event == KeyCode.DOWNARROW:
            self.down = False
        elif event == KeyCode.LEFTARROW:
            self.left = False
        elif event == KeyCode.RIGHTARROW:
            self.right = False
        elif event == KeyCode.RETURN:
            self.enterKey = False

    def showAbout(self):
        pass

    def showHelp(self):
        self.helpPage.show()
        self.stage = 4
        self.menu.hide()
        self.titleText.hide()

    def exit(self):
        if self.stage != 0:
            if self.stage == 1:
                self.gameOver()
            self.loadMenu()

    def checkKeys(self):
        if self.down:
            self.moveBlockDown()
        elif self.left:
            self.moveBlockLeft()
        elif self.right:
            self.moveBlockRight()
        elif self.rotate:
            self.rotate = False
            self.rotateBlock()
        elif self.enterKey:
            self.moveBlockToBottem()

    def setUpKeyInputs(self):
        Input.bindAll(self.workOutInput)
        Input.bindAllRelease(self.releaseInput)
        Input.mainLoop()

    def loadMenu(self):
        self.gameOverText.hide()
        if self.stage not in (0, 4, 5):
            self.animatedBackground.start()
        elif self.stage == 4:
            self.helpPage.hide()
        elif self.stage == 5:
            self.aboutPage.hide()
        self.titleText.show()
        self.menu.show()
        self.stage = 0

    def gameOver(self):
        DisplayDriver.engine.removeTask(self.taskId)
        self.animatedBackground.start()
        self.running = False
        self.stage = 2
        self.hide()
        self.gameOverText.show()

    def speedUp(self, lines):
        self.waits -= lines

    def moveBlockDown(self):
        if self.running:
            collide = self.stack.isColliding(self.block)
            if not collide:
                self.block.moveDown()
                return False
            else:
                if self.tickNum not in (0, -1):
                    self.alreadyDone = False
                    self.tickNum = -1
                    self.stack.addToStack(self.block)
                    addScore, addLines = self.stack.checkLines()
                    self.score.add(addScore, addLines)
                    self.speedUp(addLines)
                    return True

    def moveBlockToBottem(self):
        if self.running and self.block != self.oldBlock:
            while True:
                outcome = self.moveBlockDown()
                if outcome:
                    self.oldBlock = self.block
                    return

    def rotateBlock(self):
        if self.running:
            functionsToPerform = (None, self.moveBlockLeft, self.moveBlockRight)
            for function in functionsToPerform:
                if function:
                    for i in range(self.size[0] - 2):
                        if function():
                            self.block.rotateRight()
                            if not self.stack.canMove(0, self.block):
                                self.block.rotateLeft()
                            else:
                                return True

                    for i in range(self.size[0] - 2):
                        if function == self.moveBlockLeft:
                            self.moveBlockRight()
                        else:
                            self.moveBlockLeft()
                else:
                    self.block.rotateRight()
                    if not self.stack.canMove(0, self.block):
                        self.block.rotateLeft()
                    else:
                        return True

    def moveBlockLeft(self):
        if self.running:
            if self.stack.canMove(-1, self.block):
                self.block.moveLeft()
                return True
            return False

    def moveBlockRight(self):
        if self.running:
            if self.stack.canMove(1, self.block):
                self.block.moveRight()
            else:
                return True
            return False

    def newBlock(self):
        if self.block:
            self.block.removeNode()
        if not self.nextBlock:
            self.nextBlock = random.choice(self.blockTypes)([self.pos[0] - 8, self.pos[1] + 3])
            self.nextBlock.render(DisplayDriver.engine)
            self.nextBlock.setPos([self.pos[0] - 8, self.pos[1] + 3])

            self.block = random.choice(self.blockTypes)(self.pos)
            self.block.setPos([self.pos[0] + int(self.size[0] / 2), self.pos[1] + 1])
            self.block.render(DisplayDriver.engine)
        else:
            self.block = self.nextBlock
            self.block.setPos([self.pos[0] + int(self.size[0] / 2), self.pos[1] + 1])
            self.nextBlock = random.choice(self.blockTypes)([self.pos[0] - 8, self.pos[1] + 3])
            self.nextBlock.render(DisplayDriver.engine)
            self.nextBlock.setPos([self.pos[0] - 8, self.pos[1] + 3])

    def tick(self):
        if self.tickNum == 0:
            self.newBlock()
            self.moveBlocked = False
            self.tickNum += 1
        else:
            if self.tickNum in xrange(0, 200, int(self.waits / 2) + 1):
                self.moveBlockDown()
            self.tickNum += 1

        if self.stack.isGameOver():
            self.gameOver()

        self.checkKeys()

    def start(self):
        if not self.running:
            self.stage = 1
            self.animatedBackground.stop()
            self.show()
            self.titleText.hide()
            self.gameOverText.hide()
            self.menu.hide()
            self.score.reset()
            self.stack.emptyBoard()
            self.tickNum = 0
            self.waits = 20
            self.running = True
            self.taskId = DisplayDriver.engine.addTask(self.tick)

    def hide(self):
        self.block.hide()
        self.nextBlock.hide()
        self.nextBlockText.hide()
        self.border.hide()
        self.border2.hide()
        self.stack.hide()
        self.score.hide()
        self.menu.hide()
        self.gameOverText.hide()
        self.titleText.hide()
        self.helpPage.hide()

    def show(self):
        self.block.show()
        self.nextBlock.show()
        self.nextBlockText.show()
        self.border.show()
        self.border2.show()
        self.stack.show()
        self.score.show()
        self.menu.show()
        self.gameOverText.show()
        self.titleText.show()

    def destroy(self):
        self.block.removeNode()
        self.nextBlock.removeNode()
        self.nextBlockText.removeNode()
        self.border.removeNode()
        self.border2.removeNode()
        self.stack.removeNode()
        self.score.removeNode()
        self.menu.removeNode()
        self.gameOverText.removeNode()
        self.titleText.removeNode()
        self.helpPage.removeNode()


DisplayDriver.engine.setFrameRate(15)
DisplayDriver.engine.graphics.setBackground(' ')
DisplayDriver.init()
Tetris([14, 17], [30, 0])  # Make a tetris instance with size 14*17 and position 20,0
