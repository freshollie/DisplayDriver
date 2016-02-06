####
# Documentation start: 2/12/15
#
# 2/12/15:
# Fixed start on an already existing sequence
# not putting funcnum to -1
#


class Sequence():
    
    def __init__(self,engine,*intervals):
        self.started=False
        self.engine=engine
        self.sequence=[]
        self.funcNum=-1
        self.shouldLoop=False
        for interval in intervals:
            self.sequence.append(interval)

    def append(self,interval):
        self.sequence.append(interval)

    def start(self):
        if not self.started:
            self.resetSequence()
            self.shouldLoop=False
            self.started=True
            self.engine.addSequence(self)

    def loop(self):
        if not self.started:
            self.resetSequence()
            self.shouldLoop=True
            self.started=True
            self.engine.addSequence(self)

    def isLoop(self):
        return self.shouldLoop

    def resetSequence(self):
        self.funcNum = -1
        for interval in self.sequence:
            if type(interval)==Wait:
                interval.waiting = None

    def getSequence(self):
        return self.sequence

    def getSequenceLength(self):
        return len(self.sequence)

    def setFuncNum(self,num):
        self.funcNum=num

    def getFuncNum(self):
        return self.funcNum

    def getInterval(self):
        return self.sequence[self.funcNum]

    def finish(self):
        if self.started:
            self.setFuncNum(self.getSequenceLength()+1)
            self.started = False
            
            
    def __str__(self):
        return 'Sequence object %s Running: %s' %(self['name'],self.running)

class Interval():

    def __init__(self,type):
        self.type=type

    def getType(self):
        return self.type
    

class Func(Interval):

    def __init__(self,function,*args):
        self.function=function
        self.arguments=args
        Interval.__init__(self,'Function')

    def getFunction(self):
        return self.function

    def getArguments(self):
        return self.arguments

    def __str__(self):
        return 'Function Interval %s' %self.function.__name__

class Wait(Interval):

    def __init__(self,time):
        self.time=time
        self.waiting=None
        Interval.__init__(self,'Wait')

    def getTime(self):
        return self.time

    def __str__(self):
        return 'Wait Interval %s' %self.time

class Parallel(Interval):

    def __init__(self,*intervals):
        self.parallel=[]
        for interval in intervals:
            self.parallel.append(interval)
        Interval.__init__(self,'Parallel')

    def append(self, interval):
        self.parallel.append(interval)

    def __str__(self):
        return 'Parallel interval %s' %([function for function in self.parallel])


