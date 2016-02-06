from .Input import *
from .Intervals import *
import threading
import time
            
            

class Chars:
    TOPLEFTCORNER=chr(201)
    TOPRIGHTCORNER=chr(187)
    BOTTEMLEFTCORNER=chr(200)
    BOTTEMRIGHTCORNER=chr(188)
    HORIZEDGE=chr(205)
    VERTICLEEDGE=chr(186)
    EDGECORNERRIGHT=chr(204)
    EDGECORNERLEFT=chr(185)
    EDGRCORNERUP=chr(202)
    EDGRCORNERDOWN=chr(203)
    CROSS=chr(206)
    HORIZLINE=chr(196)
    BACKGROUNDCHAR='\xF0'

def removeBackground(entity,character=' '):
    newEntity=[]
    for line in entity:
        if type(line)==str:
            line.replace(character,Chars.BACKGROUNDCHAR)
            newEntity.append(line)
        else:
            newEntity.append([])
            for pixel in line:
                if pixel==character:
                    newEntity[-1].append(Chars.BACKGROUNDCHAR)
                else:
                    newEntity[-1].append(pixel)
                    

class GuiObjectBase(list):

    def __init__(self,pos=[0,0],image=['']):
        self.initPos=pos[:]
        self.layer=1
        if type(image)==str:
            image=[image]
        self.append(image)
        self.append(pos)
        self.rendered=None

    def setPos(self,pos,y=None):
        if y == None:
            self[1]=pos[:]
        else:
            self[1]=[pos,y]

    def setImage(self,image):
        self[0]=image[:]

    def getPos(self):
        return self[1][:]

    def getX(self):
        return self[1][0]

    def getY(self):
        return self[1][1]

    def setX(self,x):
        self[1][0]=x

    def setY(self,y):
        self[1][1]=y

    def getHeight(self):
        return len(self[0])

    def render(self,core):
        core.graphics.addEntity(self)
        self.rendered=core

    def removeNode(self):
        if self.rendered:
            self.rendered.graphics.removeEntity(self)
            self.rendered=None

    def hide(self):
        self.rendered.graphics.hideEntity(self)

    def show(self):
        self.rendered.graphics.showEntity(self)

    def setLayer(self, layer):
        self.layer = layer


class NewGuiObjectBase(object):

    def __init__(self,pos=[0,0],image=['']):
        self.initPos=pos[:]
        self.layer=1
        if type(image)==str:
            image=[image]
        self.image = image
        self.pos = pos[:]
        self.rendered=None

    def setPos(self,pos,y=None):
        if y == None:
            self.pos=pos[:]
        else:
            self.pos=[pos,y]

    def setImage(self,image):
        self.image = image[:]

    def getPos(self):
        return self.pos[:]

    def getX(self):
        return self.pos[0]

    def getY(self):
        return self.pos[1]

    def setX(self,x):
        self.pos[0]=x

    def setY(self,y):
        self.pos[1]=y

    def render(self,core):
        core.graphics.addEntity(self)
        self.rendered=core

    def removeNode(self):
        if self.rendered:
            self.rendered.graphics.removeEntity(self)
            self.rendered=None

    def hide(self):
        self.rendered.graphics.hideEntity(self)

    def show(self):
        self.rendered.graphics.showEntity(self)

class Border(GuiObjectBase):

    def __init__(self,diamentions,pos=[0,0],chars=[Chars.VERTICLEEDGE,Chars.VERTICLEEDGE,Chars.HORIZEDGE,Chars.HORIZEDGE]\
                 ,corners=[Chars.TOPLEFTCORNER,Chars.TOPRIGHTCORNER,Chars.BOTTEMLEFTCORNER,Chars.BOTTEMRIGHTCORNER]):
        GuiObjectBase.__init__(self,[pos[0]-len(chars[0])+1,pos[1]])
        self.diamentions=diamentions[:]
        self.chars=chars[:]
        self.corners=corners[:]
        self.makeBorder()

    def makeBorder(self):
        self[0]=[]
        for char in self.chars[3]:
            self[0].append([])
            for i in range(len(self.chars[0])):
                self[0][-1].append(self.corners[0])
            for i in range(self.diamentions[0]-2):
                self[0][-1].append(char)
            for i in range(len(self.chars[0])):
                self[0][-1].append(self.corners[1])
            
        for row in range(self.diamentions[1]-2):
            self[0].append([])
            for char in self.chars[0]:
                self[0][-1].append(char)
            for i in range(self.diamentions[0]-2):
                self[0][-1].append('\xF0')
            for char in self.chars[1]:
                self[0][-1].append(char)
                
        for char in self.chars[2]:
            self[0].append([])
            for i in range(len(self.chars[0])):
                self[0][-1].append(self.corners[2])
            for i in range(self.diamentions[0]-2):
                self[0][-1].append(char)
            for i in range(len(self.chars[0])):
                self[0][-1].append(self.corners[3])

class OnscreenText(GuiObjectBase):
    
    def __init__(self,text,pos=[0,0]):
        GuiObjectBase.__init__(self,pos=pos)
        self.setText(text)

    def setText(self,text):
        if type(text)==str:
            text=[text]
        self[0]=text             

class Choice(OnscreenText):

    def __init__(self,text,command,pos=[0,0]):
        OnscreenText.__init__(self,[text],pos)
        self.command=command
        
    def getCommand(self):
        return self.command
        

class ChoiceMenu(object):

    def __init__(self,choices,cursors,pos=[0,0],spaces=1):
        self.choices=[]
        self.choiceNum=0
        if len(cursors)==1:
            cursors=[cursors[0],cursors[0]]

        self.cursor=[]
        for i in range(2):
            self.cursor.append(OnscreenText(cursors[i]))
            
        self.choices=[]
        num=0
        for choice in choices:
            choice.setPos([pos[0],pos[1]+(spaces+1*num)])
            self.choices.append(choice)
            num+=1
            
        self.currentChoice=self.choices[self.choiceNum]
        self.updateCursorPos()

    def getChoice(self):
        return self.currentChoice
    
    def nextChoice(self):
        if self.choiceNum<len(self.choices)-1:
            self.choiceNum+=1
            self.currentChoice=self.choices[self.choiceNum]
        else:
            pass

        self.updateCursorPos()

    def previousChoice(self):
        if self.choiceNum>0:
            self.choiceNum-=1
            self.currentChoice=self.choices[self.choiceNum]
        else:
            pass

        self.updateCursorPos()

    def updateCursorPos(self):
        self.cursor[0].setPos([self.currentChoice.getX()-3,self.currentChoice.getY()])
        self.cursor[1].setPos([self.currentChoice.getX()+len(self.currentChoice[0][0])+2,self.currentChoice.getY()])

    def selectChoice(self):
        self.currentChoice.getCommand()()

    def hide(self):
        for choice in self.choices:
            choice.hide()
        for cursor in self.cursor:
            cursor.hide()

    def show(self):
        for choice in self.choices:
            choice.show()
        for cursor in self.cursor:
            cursor.show()

    def render(self,renderer):
        for choice in self.choices:
            choice.render(renderer)
        for cursor in self.cursor:
            cursor.render(renderer)

    def setLayer(self, layer):
        for choice in self.choices:
            choice.setLayer(layer)
        for cursor in self.cursor:
            cursor.setLayer(layer)

    def removeNode(self):
        for choice in self.choices:
            choice.removeNode()
        for cursor in self.cursor:
            cursor.removeNode()

class Rectangle(GuiObjectBase):

    def __init__(self,pos,size,char='#'):
        GuiObjectBase.__init__(self,pos)
        image=[] # Weird problems caused by this...
        for line in range(size[1]):
            image.append([char]*size[0])
        self.setImage(image)

class TextBox(object):

    def __init__(self,pos,size,background=' '):
        self.background=Rectangle([pos[0],pos[1]+1],size,background)
        self.border=Border([size[0],size[1]+2],pos)
        self.size=size
        self.text=[]
        for i in range(self.size[0]):
            self.text.append(OnscreenText(text=[''],pos=[pos[0]+1,pos[1]+i+1]))

    def setText(self,text,startLine=0):
        for i in range(startLine,self.size[0]):
            if len(line)>self.size[0]-2:
                if line[24]==" ":
                    self.text[i].setText([line[:24]])
                    line=line[24:]
                    
                else:
                    for x in range(25,0,-1):
                        if line[x-1]==" ":
                            self.text[i].setText([line[:x-1]])
                            line=line[x-1:]
                            break
            else:
                self.text[i].setText([line])
                break

    def setLine(self,line,text,wrap=False):
        if len(text)>self.size[0]-2:
            if wrap:
                self.setText(text,line)
            else:
                text=text[:self.size[0]-2]
        self.text[line].setText([text])

    def render(self,renderer):
        self.background.render(renderer)
        self.border.render(renderer)
        for text in self.text:
            text.render(renderer)

    def removeNode(self):
        self.background.removeNode()
        self.border.removeNode()
        for text in self.text:
            text.removeNode()

    def hide(self):
        self.background.hide()
        self.border.hide()
        for text in self.text:
            text.hide()

    def show(self):
        self.background.show()
        self.border.show()
        for text in self.text:
            text.show()

    def setPos(self,pos):
        self.background.setPos(pos)
        self.border.setPos(pos)

        for text in self.text:
            for i in range(self.size[1]):
                self.text.setPos([self.pos[0]+1,self.pos[1]+i+1])

    def setLayer(self, layer):
        self.background.setLayer(layer)
        self.border.setLayer(layer)
        for text in self.text:
            text.setLayer(layer)

class Ticker(TextBox):
    def __init__(self,pos,size,reversed=True):
        self.reversed=reversed
        TextBox.__init__(self,pos,size)
        self.length=size[1]
        self.clear()

    def newLine(self,text,scroll=True):
        self.line.append(text)
        self.lineNum+=1
        if not self.isScrolled:
            self.bottemDisplayNum=self.lineNum
            self.tick()
            self.printDisplay()
            
        else:
            self.scrollDown()

        if not scroll:
            self.scrollUp()

    def showLines(self):
        for line in self.lines:
            line.show()

    def hideLines(self):
        for line in self.lines:
            line.hide()
            
    def tick(self):
        for i in range(self.length-1,0,-1):
            self.display[i]=self.display[i-1]
        self.display[0]=self.line[-1]

    def printDisplay(self):
        i=self.length-1
        if self.reversed:
            for line in reversed(self.display):
                self.setLine(i,line)
                i-=1
        else:
            for line in self.display:
                self.setLine(i,line)
                i-=1
            
            
    def scrollUp(self):
        original=self.bottemDisplayNum
        if self.isScrolled:
            option=1
            self.bottemDisplayNum-=1
        else:
            option=2
            self.bottemDisplayNum=self.lineNum-1
            self.isScrolled=True
            
        if self.bottemDisplayNum-self.length>-1:
            for i in range(1,self.length):
                self.display[i-1]=self.display[i]
            self.display[self.length-1]=self.line[self.bottemDisplayNum-self.length]
        else:
            self.bottemDisplayNum=original
            if option==2:
                self.isScrolled=False
        self.printDisplay()

    def scrollDown(self):
        if self.isScrolled:
            if self.bottemDisplayNum+1==self.lineNum:
                self.isScrolled=False
            
            self.bottemDisplayNum+=1
            for i in range(self.length-1,0,-1):
                self.display[i]=self.display[i-1]
            self.display[0]=self.line[self.bottemDisplayNum-1]
        self.printDisplay()

    def checkLine(self,line):
        letterInLine=False
        for letter in line:
            if letter!=" ":
                letterInLine=True
                break
        return letterInLine

    def clear(self):
        self.line=[]
        self.display=[]
        self.lineNum=0
        self.lastMessages=['','']
        self.bottemDisplayNum=0
        self.isScrolled=False
        for i in range(self.length):
            self.display.append("")
        self.printDisplay()
        
    

class DirectInput(OnscreenText):
    
    def __init__(self,text,pos,inputTo=None):
        OnscreenText.__init__(self,[text],pos=pos)
        Input.bindAll(self.pressed)
        Input.bindAllRelease(self.releaseShift)
        self.shift=False
        self.takingInput=False
        self.text=text
        self.inputTo=inputTo
        self.currentInput=''
        self.updateText()

    def pressed(self,key):
        if self.takingInput:
            if key in KeyCode.KEYTOLETTER:
                letter=KeyCode.KEYTOLETTER[key]
                if self.shift:
                    letter=letter.upper()
                self.currentInput+=letter
                self.updateText()
            elif key==KeyCode.RETURN:
                if self.inputTo:
                    self.inputTo(self.currentInput)
                    self.takingInput=False
            elif key==KeyCode.BACKSPACE:
                self.currentInput=self.currentInput[:-1]
                self.updateText()
            elif key==KeyCode.SHIFT:
                self.shift=True
            else:
                pass

    def updateText(self):
        if self.takingInput:
            cursor='|'
        else:
            cursor=''
        self[0]=[self.text+self.currentInput+cursor]

    def activate(self):
        self.takingInput=True
        self.updateText()

    def disable(self):
        self.takingInput=False
        self.updateText()

    def run(self):
        self.activate()
        threading.Thread(target=self.mainLoop).start()

    def getInput(self):
        return self.currentInput

    def releaseShift(self,key):
        if key==KeyCode.SHIFT:
            self.shift=False

    def mainLoop(self):
        while self.takingInput:
            Input.checkBindings()
            time.sleep(0.01)


class InputBox(TextBox):

    def __init__(self,pos,size,lines,background=' '):
        TextBox.__init__(self,pos,size,background)
        self.text=[]
        self.running=False
        i=0
        for instance in lines:
            self.text.append(instance)
            self.text[-1].setPos([pos[0]+1,pos[1]+i+1])
            i+=1
        Input.bind(KeyCode.UPARROW,self.previousInput)
        Input.bind(KeyCode.DOWNARROW,self.nextInput)

    def previousInput(self):
        if self.running:
            self.text[self.inputNum].disable()
            if self.inputNum!=0:
                self.inputNum-=1
            self.activateCurrentInput()

    def nextInput(self):
        if self.running:
            self.text[self.inputNum].disable()
            self.inputNum+=1
            if self.inputNum==len(self.text):
                self.inputNum-=1
            self.activateCurrentInput()

    def getValue(self,index):
        return self.text[index].value

    def activateCurrentInput(self):
        self.text[self.inputNum].activate()

    def activate(self):
        self.running=True
        self.inputNum=0
        self.activateCurrentInput()

    def run(self):
        self.running=True
        self.inputNum=0
        self.activateCurrentInput()
        threading.Thread(target=self.mainLoop).start()

    def disable(self):
        self.running=False
        for textGui in self.text:
            textGui.disable()

    def mainLoop(self):
        while self.running:
            Input.checkBindings()
            time.sleep(0.01)

class Button(OnscreenText):

    def __init__(self,text,pos,command):
        self.command=command
        self.text=text
        self.active=False
        OnscreenText.__init__(self,[text],pos=pos)
        Input.bind(KeyCode.RETURN,self.doCommand)

    def doCommand(self):
        if self.active:
            self.command()

    def updateText(self):
        if self.active:
            cursors=['<','>']
        else:
            cursors=[' ',' ']
            
        self.setText([cursors[0]+self.text+cursors[1]])

    def activate(self):
        self.active=True
        self.updateText()

    def disable(self):
        self.active=False
        self.updateText()

    def run(self):
        self.activate()
        threading.Thread(target=self.mainLoop).start()

    def mainLoop(self):
        while self.active:
            Input.checkBindings()
            time.sleep(0.01)
        

class OptionScroller(OnscreenText):

    def __init__(self,text,options=[],optionRange=[],pos=[0,0],start='bottom',step=1,inputTo=None):
        OnscreenText.__init__(self,text,pos)
        self.active=False
        self.inputTo=inputTo
        self.text=text
        if optionRange:
            self.upBound=optionRange[1]
            self.downBound=optionRange[0]
            if start=='bottom':
                self.value=self.downBound
            elif start=='middle':
                self.value=int(abs(self.downBound-self.upBound)/2)
            else:
                self.value=self.upBound

            self.updateText()
            self.step=step
            Input.bind(KeyCode.RIGHTARROW,self.increaseValue)
            Input.bind(KeyCode.LEFTARROW,self.decreaseValue)
        elif options:
            self.valueNum=0
            self.options=options
            self.value=self.options[self.valueNum]
            self.updateText()
            Input.bind(KeyCode.RIGHTARROW,self.nextValue)
            Input.bind(KeyCode.LEFTARROW,self.previousValue)
            Input.bind(KeyCode.RETURN,self.returnInput)
        else:
            raise AttributeError('No options given')

    def updateText(self):
        if self.active:
            cursors=['<','>']
        else:
            cursors=[' ',' ']
            
        self.setText([self.text+cursors[0]+str(self.value)+cursors[1]])

    def returnInput(self):
        if self.inputTo:
            self.inputTo(self.value)
            self.active=False
            self.updateText()
            

    def increaseValue(self):
        if self.active:
            self.value+=self.step
            if self.value>self.upBound:
                self.decreaseValue()
            self.updateText()

    def decreaseValue(self):
        if self.active:
            self.value-=self.step
            if self.value<self.downBound:
                self.increaseValue()
            self.updateText()

    def nextValue(self):
        if self.active:
            self.valueNum+=1
            if self.valueNum!=len(self.options):
                self.value=self.options[self.valueNum]
            else:
                self.valueNum-=1
                
            self.updateText()

    def previousValue(self):
        if self.active:
            self.valueNum-=1
            if self.valueNum>=0:
                self.value=self.options[self.valueNum]
            else:
                self.valueNum+=1
                
            self.updateText()
            
    def activate(self):
        self.active=True
        self.updateText()

    def disable(self):
        self.active=False
        self.updateText()

    def run(self):
        self.activate()
        threading.Thread(target=self.mainLoop).start()

    def getValue(self):
        return self.value

    def mainLoop(self):
        while self.active:
            Input.checkBindings()
            time.sleep(0.01)

class Explosion(GuiObjectBase):
    FRAMES=[['',
             '',
             '####x'.replace('#',Chars.BACKGROUNDCHAR)
             ],
            
            ['',
             '##\\###/'.replace('#',Chars.BACKGROUNDCHAR),
             '####X'.replace('#',Chars.BACKGROUNDCHAR),
             '##/###\\'.replace('#',Chars.BACKGROUNDCHAR)
             ],
            
            ['\\#######/'.replace('#',Chars.BACKGROUNDCHAR),
             '##\\###/##'.replace('#',Chars.BACKGROUNDCHAR),
             '',
             '##/###\\##'.replace('#',Chars.BACKGROUNDCHAR),
             '/#######\\'.replace('#',Chars.BACKGROUNDCHAR)
            ],
            
            ['\\#######/'.replace('#',Chars.BACKGROUNDCHAR),
             '',
             '',
             '',
             '/#######\\'.replace('#',Chars.BACKGROUNDCHAR)
            ]]



    def __init__(self,pos,engine):
        self.pos=[pos[0]-3,pos[0]-2]
        GuiObjectBase.__init__(self,pos)
        self.engine=engine
        self.seq=Sequence(engine)
        for i in range(len(self.FRAMES)):
            self.seq.append(Func(self.nextFrame))
        self.seq.append(Func(self.removeNode))
        self.currentFrame=-1

    def nextFrame(self):
        self.currentFrame+=1

        try:
            self.setImage(self.FRAMES[self.currentFrame])
        except:
            self.currentFrame=-1

    def play(self):
        self.render(self.engine)
        self.seq.append(Func(self.removeNode))
        self.seq.start()

    def loop(self):
        self.seq=Sequence('Explosion',self.engine)
        for i in range(len(self.FRAMES)):
            self.seq.append(Func(self.nextFrame))
        self.render(self.engine)
        self.seq.loop()
        

    
    
        
    
    
        
