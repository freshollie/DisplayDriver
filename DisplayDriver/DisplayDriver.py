'''
Display Driver, by freshollie.

Change Log:
8/2013: Start

...
....
11/2014: Major bug discovered with intervals and was then solved

3/2015: Rendering bug discovered and solved

'''
import time
import threading 
import sys
import os
from . import Colours
from .GuiObjects import TextBox

BACKGROUNDCHAR='\xF0'

class Graphics(object):
    '''
    Graphics is graphical driver for the engine. It makes the display
    and manages the enities. Some of the methods are here but
    completely unused like the methods containing 'Generate'
    '''
    
    def __init__(self,resolution=[79,23]):
        '''
        The initialisation contains some properties of the engine
        '''
        self.defaultColours=Colours.getTextAttr()
        self.res=resolution[:] # Setting resolution
        self.entityList=[] # Creates an empty entity list
        self.axis2index={'x':0,'y':1} # Unused
        self.backgroundLetter=' ' # Setting what the background will look like
        self.hiddenEntitys=[] # Setting the list of entities that are hidden
        
        self.removedList=[] # Used to stop the list from changing size
                            # if an entity is removed during a tick
                            
        self.lastDisplay=[] # Used to check if the display is exactly the same as
                            # the last display to see if it needs to print the display
                            

    def createBlankDisplay(self):
        '''
        Creates a blank display that the createDisplay method can
        over right to make the display.
        '''
        
        self.pixelArray=[] # Set pixel array to an empty list to be added to
        for row in range(self.res[1]): # Iterate for the number of rows the display needs to be
            self.pixelArray.append([]) # Add a row
            for pixel in range(self.res[0]): # Iterate for the number of pixels that need to be in a row
                self.pixelArray[row].append(self.backgroundLetter) # Add the background letter to the row

    def createDisplay(self,layer=0):
        '''
        Creates the display using the entity dictionary and a blank display.
        The function is called every display tick after all of the tasks
        have been called which means that the display will be using entitys
        that have been edited by the task
        '''


        if layer==0: # Create another blank display if the function is the first interation
            self.createBlankDisplay() # Create a blank display

        # The doingBg variable is used to make entitys that are in the background to be put down first so that they will not overlap
        # other entitys


        for entity in self.removedList: # Removing all of the entitys from that list that shouldn't be there
            self.entityList.remove(entity)
        self.removedList=[] # All entitys in the list have been removed so empties the list
        entityList=self.entityList[:] # Makes a copy of the entity list so that the list is not changed during iteration

        nextLayer=False
        
        for entity in entityList: # Iterate for every entity
            if entity not in self.hiddenEntitys: #Ignore the entity if it is in the hidden entity list
                if hasattr(entity, 'image'):
                    image = entity.image
                    
                else:
                    image=entity[0] # Make a reference of the entities image
                if entity.layer!=layer:
                    if entity.layer>layer:
                        nextLayer=True
                    continue
                    
                for rowNum in range(len(image)): # For interation in the height of the image
                    for pixelNum in range(len(image[rowNum])): # For interation in the width of the row
                        if hasattr(entity, 'pos'):
                            y = int(round(entity.getY()))
                            x = int(round(entity.getX()))
                        else:
                            y=int(round(pixelNum+entity[1][0])) # Setting the x of the pixel realative to the position of the entity
                            x=int(round(rowNum+entity[1][1])) # Setting the y of the pixel realative to the position of the entity
                        
                        if x<self.res[1] and x>=0 and y<self.res[0] and y>=0: # If the pixel is off screen, ignore
                            if image[rowNum][pixelNum]!=BACKGROUNDCHAR: # If the pixel is the invisible character, ignore
                                try:
                                    self.pixelArray[x][y]=image[rowNum][pixelNum] # Set the pixel array x and y position to the pixel of the image
                                except:
                                    print(entity)
                                    input('Error with this entity')

                            else:
                                pass
                        else:
                            pass
            else:
                pass
            
        if nextLayer:
            self.createDisplay(layer+1)

    def makeColour(self,text):
        '''
        Make colour is a method that decodes a string to make a pixel the colour it needs to be
        '''
        coloursList=text.split('\x01')[-1].split('\x02')[0] # Get the list of colours from the text
                                                            # By spliting it between \x01 and \x02

        if len(coloursList)>1: # If There is more than 1 colour split the colours up
            coloursList=coloursList.split('\\')[1:] # Make a list of the colours

        for index in range(len(coloursList)): # Iterate for the length of the colour list
            coloursList[index]=str(eval('Colours.'+coloursList[index])) # Colours is the name of the module and it adds the colours name to the Colours.X
                                                                        # and then uses eval to get the constant value and then uses str to convert that
                                                                        # value to a string 

        colourString='|'.join(coloursList) # Make the string that will be evaled when going into the arguments
        
        try:
            Colours.setTextAttr(eval(colourString)) # Try and set colour to the object created from the operation of the colours list
            sys.stdout.write(text.split('\x02\\')[-1])
        except SyntaxError:# If a syntax error is raised then it means that the colour list was not generated properly 
            print(colours) # Print the colours string that was generated
            raise SyntaxError # Raise the error to crash the program
            
    def addEntity(self,object):
        '''
        When an entity is rendered it is added to the entity
        list of the graphics engine which means that the
        graphics engine has a reference to that object so
        it can get key things from it like its position and
        image
        '''
        
        self.entityList.append(object) # Add the object to the list of entitys

    def removeEntity(self,object):
        '''
        To remove and entity it needs to be added to a remove
        list so that it doesn't get removed while the create
        display method is iterating
        '''
        
        self.removedList.append(object) # Add the object the list of entitys that needs to be removed on the next display tick

    def hideEntity(self,object):
        '''
        Used to hide and entity without having to remove it from
        the entity list. This is only to be used if the entity
        will be used again other wise lagg might be created as
        the engine is having to interate for every entity even
        if its hidden
        '''
        
        if object not in self.hiddenEntitys: # If the object is not already hidden
            self.hiddenEntitys.append(object) # Add the object to the list of hidden entities

    def showEntity(self,object):
        '''
        Same as hide entity but just shows it if its already hidden
        '''
    
        if object in self.hiddenEntitys: # If the object is hidden
            self.hiddenEntitys.remove(object) # Remove the object from the list of hidden entities

    def printDisplay(self):
        '''
        Print display is the output of the graphics engine
        it is run after a display has been created to print
        the frame
        '''

        if self.lastDisplay!=self.pixelArray: # Ignore if the display has not change
            #printString='' # Make the print variable a string
            if "idlelib" not in sys.modules:
                os.system('cls')
            printString=''
            colourPrintString=''
            for line in self.pixelArray: # Iterate for every line in the pixelArray
                for pixel in line:
                    if pixel.startswith('\x01') and '\x02' in pixel:
                        if printString!='':
                            Colours.setTextAttr(self.defaultColours)
                            sys.stdout.write(printString)
                            printString=''
                        sys.stdout.flush()
                        self.makeColour(pixel)
                        
                    else:
                        printString+=pixel
                printString+='\n'
            if printString!='':
                Colours.setTextAttr(self.defaultColours)
                print(printString)
                #printString+=''.join(line)+'\n'# Add the line to the print string
             # Clear the previous display
            #print(printString) # Print the new display
        self.lastDisplay=self.pixelArray[:] # Set the previous display variable to a copy of the current display

    def setRes(self,resolution):
        '''
        Set the resolution of the graphics engine
        '''
        
        self.res=resolution
        os.system('mode con:cols=%s lines=%s' %(self.res[0]+1,self.res[1]+2))
        
    def setBackground(self,letter):
        self.backgroundLetter=letter

class Core(object):
    '''
    Core is the main display driver. It runs the Display and manages the tasks.
    '''
    
    def __init__(self,frameRate=12,name='Game'):
        self.graphics=Graphics() # Define the graphical object
        self.name=name  # Set the name of the Display Driver
        self.frameNum=0 # Set the frame number it it on to 0
        self.startTime=time.time() # Setting the time the display driver was defined to the current time
        self.taskDict={} # Setting the task dict to empty
        self.quedSequences=[] # Setting the qued sequence list to empty
        self.quedTasks=[] # Setting the quest task list to empty

        # v Used in tests and can be ignored
        self.testLogo=['M""""""""M\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0dP\xF0\xF0\xF0M""""""""M\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0',
                   'Mmmm\xF0\xF0mmmM\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF088\xF0\xF0\xF0Mmmm\xF0\xF0mmmM\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0',
                   'MMMM\xF0\xF0MMMM\xF0.d8888b.\xF0dP.\xF0\xF0.dP\xF0d8888P\xF0MMMM\xF0\xF0MMMM\xF0.d8888b.\xF0dP\xF0\xF0dP\xF0\xF0dP\xF088d888b.',
                   "MMMM\xF0\xF0MMMM\xF088ooood8\xF0\xF0`8bd8'\xF0\xF0\xF0\xF088\xF0\xF0\xF0MMMM\xF0\xF0MMMM\xF088'\xF0\xF0`88\xF088\xF0\xF088\xF0\xF088\xF088'\xF0\xF0`88",
                   "MMMM\xF0\xF0MMMM\xF088.\xF0\xF0...\xF0\xF0.d88b.\xF0\xF0\xF0\xF088\xF0\xF0\xF0MMMM\xF0\xF0MMMM\xF088.\xF0\xF0.88\xF088.88b.88'\xF088\xF0\xF0\xF0\xF088",
                   "MMMM\xF0\xF0MMMM\xF0`88888P'\xF0dP'\xF0\xF0`dP\xF0\xF0\xF0dP\xF0\xF0\xF0MMMM\xF0\xF0MMMM\xF0`88888P'\xF08888P\xF0Y8P\xF0\xF0dP\xF0\xF0\xF0\xF0dP",
                   'MMMMMMMMMM\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0MMMMMMMMMM\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0\xF0']
        
        self.runOnceList=[] # Setting the run once list to empty
        self.sequences=[] # Setting the list of sequences to empty
        self.running=False # Used to signify if the display driver is running so that the thread can end
        self.frameLength=1.0/frameRate # Sets how long a frame is supposed to be based on the frames per second defined by the arguments
        self.frameRate=frameRate
        self.maxTaskValue=0 # maxTaskValue is used to give a task a designated number
        self.timeTaken=1 # Defined incase it is rederence before the main loop has started
        self.removedTasks=[] # Setting the removed last list to empty
        self.addedTasks={} # Setting the added task dict to empty
        self.seconds=0 # Used in debug for run time
        self.minutes=0 # Used in debug for run time
        self.hours=0 # Used in debug for run time
        self.days=0 # Used in debug for run time
        self.threadPrint=False # Used to set if to thread the print display (for higher fps)
        self.engineTime=0

    def setFrameRate(self,frameRate):
        '''
        Set a new framerate if the user would like their own tick rate
        but a slower tick rate is recomended for a less flickery experience
        '''

        self.frameLength=1.0/frameRate
        
        if frameRate>20:
            self.threadPrint=True

    def tickTime(self):
        '''
        Used to count how long the engine has been running for the debug
        utility
        '''
        tick=int(time.time()-self.startTime)
        if tick>=1: # Clock the time if the rounded down time from the last tick=1
            self.startTime=time.time() # Set a new start time
        self.seconds=int(self.seconds)+tick # Add 1 to the current number of seconds
        if self.seconds==60: # If the number of seconds=60
            self.minutes=int(self.minutes)+1 # add 1 to the minutes
            self.seconds=0 # Reset the seconds
        if self.minutes==60: # If the number of minutes=60
            self.hours=int(self.hours)+1 # Add 1 to the hours
            self.minutes=0 # Reset the minutes
        if self.hours==24: # If the number of hours=24
            self.days=int(self.days)+1 # Add 1 to the number of days
            self.hours=0 # Reset the hours
            
        # This part is used to make the time look like a digital clock
        if len(str(self.hours))==1: # If there is only 1 digit in hours
            self.hours='0'+str(self.hours) # Put a 0 in front
        else:
            self.hours=str(self.hours) # Otherwise make hours a string of hours
            
        if len(str(self.minutes))==1: # If there is only 1 digit in minutes
            self.minutes='0'+str(self.minutes) # Put a 0 in front
        else:
            self.minutes=str(self.minutes) # Otherwise make minutes a string of minutes
        
        if len(str(self.seconds))==1: # If there is only 1 digit in seconds
            self.seconds='0'+str(self.seconds) # Put a 0 in front
        else:
            self.seconds=str(self.seconds) # Otherwise make seconds a string of seconds

    def addTask(self,task,arguments=[],once=False):
        '''
        Adding a task to the engine is the only way to interact with
        the graphics engine and the display driver. When a task has
        been added, every frame the tasks will be run.
        '''

        maxTaskValue=self.maxTaskValue # Make a copy of the max task value
        i=0
        while True: # So you can have infinate tasks
            if str(i) not in self.taskDict: # Check that the task key has not already been used
                maxTaskValue=i # Set the max task value to that value
                break # Break out of the while loop
            i+=1
        self.taskDict[str(maxTaskValue)]=[task,arguments]
        if once:
            self.runOnceList.append(str(maxTaskValue))
        self.maxTaskValue=maxTaskValue
        return str(maxTaskValue)

    def enqueTask(self,task,arguments,once=False):
        self.quedTasks.append([task,arguments,once])

    def checkQuedTasks(self):
        if not self.sequences and self.quedTasks:
            task=self.quedTasks[0][0]
            arguments=self.quedTasks[0][1]
            once=self.quedTasks[0][2]
            self.addTask(task,arguments,once)
            self.quedTasks.remove(self.quedTasks[0])

    def removeTask(self,taskValue):
        self.removedTasks.append(taskValue)

    def removeUnneededTasks(self):
        for taskValue in self.runOnceList:
            del self.taskDict[taskValue]
        self.runOnceList=[]
    
    def mainLoop(self):
        while self.running:
            beforeTime=time.time()
            self.checkSequences()
            self.checkQuedSequences()
            self.checkQuedTasks()
            self.tick()
            self.tickTime()
            if self.threadPrint:
                try:self.graphics.createDisplay()
                except:pass
                threading.Thread(target=self.graphics.printDisplay).start()
            else:
                self.graphics.createDisplay()
                self.graphics.printDisplay()
            self.removeUnneededTasks()
            frameTime=time.time()-beforeTime
            if self.frameLength-frameTime>0:
                time.sleep(self.frameLength-frameTime)
            nowTime=time.time()
            self.timeTaken=nowTime-self.beforeTime
            self.frameRate=self.frameNum/self.timeTaken
        sys.exit()

    def enqueSequence(self,sequence):
        self.quedSequences.append(sequence)

    def addSequence(self,sequence):
        self.sequences.append(sequence)
        self.sequences[-1].funcNum=-1
        
    def deleteSequence(self,sequence):
        self.sequences.remove(sequence)

    def checkQuedSequences(self):
        if not self.sequences and self.quedSequences:
            self.addSequence(self.quedSequences[0])
            self.quedSequences.remove(self.quedSequences[0])

    def checkSequences(self):
        for sequence in self.sequences:
            if sequence.getFuncNum()+1==sequence.getSequenceLength():
                if not sequence.isLoop():
                    self.deleteSequence(sequence)
                    sequence.finish()
                    continue
                
                else:
                    sequence.setFuncNum(-1)

            sequence.setFuncNum(sequence.getFuncNum()+1)
            sequenceItem=sequence.getInterval()

            if sequenceItem.getType()=='Wait':
                if sequenceItem.waiting==None:
                    sequenceItem.waiting=time.time()+sequenceItem.time
                    sequence.setFuncNum(sequence.getFuncNum()-1)
                    continue
                else:
                    if time.time()<sequenceItem.waiting:
                        sequence.setFuncNum(sequence.getFuncNum()-1)
                        continue
                    else:
                        sequenceItem.waiting=None
                        sequence.setFuncNum(sequence.getFuncNum()+1)
                        if sequence.getFuncNum()==sequence.getSequenceLength(): # Fixed sequence problem with wait being at the end
                                                                                # of the sequence. 16/11/15
                            if not sequence.isLoop():
                                self.deleteSequence(sequence)
                                sequence.finish()
                                continue
                            
                            else:
                                sequence.setFuncNum(-1)
                                
            sequenceItem=sequence.getInterval()
            if sequenceItem.getType()=='Function':
                self.addTask(sequenceItem.getFunction(),sequenceItem.getArguments(),once=True)
                
            elif sequenceItem.getType()=='Parallel':
                for interval in sequenceItem.parallel:
                    self.addTask(interval.getFunction(),interval.getArguments(),once=True)
    
            else:
                continue
                
    def tick(self):
        self.frameNum+=1
        for key in self.removedTasks:
            del self.taskDict[key]
        taskDict=self.taskDict.copy()
        self.removedTasks=[]
        for taskKey in taskDict:
            self.doTask(taskDict[taskKey][0],taskDict[taskKey][1])
            
    def doTask(self,function,arguments,**kwds):
        function(*arguments,**kwds)

    def setTitle(self,name):
        self.name=name
        os.system('title %s' %(self.name))
    
    def start(self):
        self.running=True
        os.system('title %s' %(self.name))
        self.beforeTime=time.time()
        self.mainLoop()

    def stop(self):
        self.running=False

class Debug(TextBox):

    def __init__(self,pos=[44,0]):
        TextBox.__init__(self,pos,[35,8])
        self.isBackground=False
        self.startTime=0
        self.running=False

    def update(self):
        self.setLine(0,'Run Time: %s:%s:%s' %(engine.hours,engine.minutes,engine.seconds))
        self.setLine(1,'Number of tasks: %s' %(len(engine.taskDict)))
        self.setLine(2,'Number of rendered enities: %s' %(len(engine.graphics.entityList)))
        self.setLine(3,'Frame Number: %s' %(engine.frameNum))
        self.setLine(4,'Actual FPS: %s' %(engine.frameNum/engine.timeTaken))
        i=5
        for x in range(5,8):
             self.setLine(x,'')
        for key in engine.taskDict:
            self.setLine(i,str(engine.taskDict[key][0]))
            i+=1
            if i>7:
                break

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()
    
    def start(self):
        self.running=True
        self.render(engine)
        self.taskId=engine.addTask(self.update)
        self.setLayer(2)

    def stop(self):
        self.running=False
        self.removeNode()
        engine.removeTask(self.taskId)


         
engine=Core()
debug=Debug()

def init():
    threading.Thread(target=engine.start).start()
