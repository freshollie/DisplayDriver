class Sequence(dict):
    
    def __init__(self,name,engine,*intervals):
        self.started=False
        self.engine=engine
        self['name']=name
        self['sequence']=[]
        for interval in intervals:
            self['sequence'].append(interval)

    def append(self,interval):
        self['sequence'].append(interval)

    def start(self):
        if not self.started:
            if 'loop' in self:
                del self['loop']
            self.started=True
            self.engine.addSequence(self)

    def loop(self):
        if not self.started:
            self['loop']=True
            self.started=True
            self.engine.addSequence(self)

    def finish(self):
        if self.started and 'funcNum' in self:
            self['funcNum']=len(self['sequence'])+1
            
            
    def __str__(self):
        return 'Sequence object %s Running: %s' %(self['name'],self.running)

class Func(dict):

    def __init__(self,function,*args):
        self['function']=[function,args]

    def __str__(self):
        return 'Function Interval %s' %self['function'][0].__name__

class Wait(dict):

    def __init__(self,time):
        self['wait']=time

    def __str__(self):
        return 'Wait Interval %s' %self['wait']

class Parrallel(dict):

    def __init__(self,*intervals):
        self['parrallel']=[]
        for interval in intervals:
            self['parrallel'].append(interval)

    def __str__(self):
        return 'Parrallel interval %s' %([function for function in self['parrallel']])


