import time
import string
from ctypes import *
from ctypes.wintypes import *

#windll.user32.GetKeyState.restype=WORD
#windll.user32.GetKeyState.argtypes=[c_char]

class Input:
    '''
    Inputs, original concept written by Jamie Read
    '''

    _keyStatus = {}
    _binds = {}
    _releaseBinds = {}
    _keyWaits={}
    bindAllReleaseFunctions=[]
    bindAllFunctions=[]

    @staticmethod
    def isKeyPressed(key):
        '''
        Written in an open source program on the internet,
        returns True if the key is currently pressed
        '''
        return bool(windll.user32.GetKeyState(key) & 0x8000)

    @staticmethod
    def bind(key, function):
        """Bind a key to a function"""
        if key not in Input._binds:
            Input._binds[key] = [function]
        else:
            Input._binds[key].append(function)

    @staticmethod
    def bindAll(function):
        '''
        Bind all keys to a function
        '''
        Input.bindAllFunctions.append(function)

    @staticmethod
    def bindAllRelease(function):
        '''
        When any key is released this the function inputted
        will be called
        '''
        Input.bindAllReleaseFunctions.append(function)

    @staticmethod
    def bindRelease(key,function):
        '''
        The function inputed will be run if the key is
        released
        '''
    
        if key not in Input._releaseBinds:
            Input._releaseBinds[key]=[function]
        else:
            Input._releaseBinds[key].append(function)

    @staticmethod
    def ignoreAll(function):
        if function in Input.bindAllFunctions:
            Input.bindAllFunctions.remove(function)
        elif function in Input.bindAllReleaseFunctions:
            Input.bindAllReleaseFunctions.remove(function)

    @staticmethod
    def ignore(key,function):
        if key in Input._binds:
            Input._binds[key].remove(function)
        else:
            Input._binds[key]=[]
        
    @staticmethod
    def checkAllKeys():
        for i in range(253):
            if Input.isKeyPressed(i):
                Input._keyStatus[i]=True
            else:
                Input._keyStatus[i]=False

    @staticmethod
    def checkBindings():
        """
           Check through bindings and call appropriate functions
           written mostly by Oliver Bell
        """
        if Input._keyStatus:
            oldKeys=Input._keyStatus.copy()
        else:
            oldKeys=Input._keyStatus
        Input.checkAllKeys()
        if Input.bindAllFunctions: #Keys for bind all:
            for key in Input._keyStatus:
                if Input._keyStatus[key]:
                    if key in Input._keyWaits:
                        Input._keyWaits[key]+=1
                        if Input._keyWaits[key]>50:
                            for function in Input.bindAllFunctions:
                                function(key)
                    else:
                        Input._keyWaits[key]=1
                        for function in Input.bindAllFunctions:
                            function(key)
                        Input._keyWaits[key]+=1

        for key in Input._keyStatus:
            if oldKeys[key] and not Input._keyStatus[key]:
                if key in Input._keyWaits:
                    del Input._keyWaits[key]
                for releaseFunction in Input.bindAllReleaseFunctions:
                    releaseFunction(key) # The release function

        for key in Input._binds:
            if Input._keyStatus[key]:
                if key in Input._keyWaits:
                    if Input._keyWaits[key]>50:
                        for function in Input._binds[key]:
                            function()
                    Input._keyWaits[key]+=1
                else:
                    Input._keyWaits[key]=1
                    for function in Input._binds[key]:
                        function()
                    Input._keyWaits[key]+=1
                        
            elif oldKeys[key]:
                if key in Input._keyWaits:
                    del Input._keyWaits[key]
                    
                if key in Input._releaseBinds:
                    for releaseFunction in Input._releaseBinds[key]:
                        releaseFunction()

    @staticmethod
    def mainLoop():
        """ Main Loop to check weather the key is actually pressed"""
        while True:
            Input.checkBindings()
            time.sleep(0.01)

class KeyCode:
    '''
    Keycodes, linking names to keynumber

    Written by Jamie Read edited by Oliver Bell
    to add keytoletter dictionary
    '''
    
    
    KEYTOLETTER={}
    #Mouse
    LMB = 1
    RMB = 2
    MMB = 4
    XB1 = 5
    XB2 = 6

    #Specials (keyboard)
    BACKSPACE = 8
    TAB = 9
    RETURN = 13
    SHIFT = 16
    CTRL = 17
    ALT = 18
    PAUSE = 19
    CAPSLOCK = 20
    ESCAPE = 27
    SPACE = 32
    PAGEUP = 33
    PAGEDOWN = 34
    END = 35
    HOME = 36

    #Arrows
    LEFTARROW = 37
    KEYTOLETTER[37]='LeftArrow'
    UPARROW = 38
    KEYTOLETTER[37]='UpArrow'
    RIGHTARROW = 39
    KEYTOLETTER[37]='RightArrow'
    DOWNARROW = 40
    KEYTOLETTER[37]='DownArrow'

    #Back to specials
    SELECT = 41
    PRINT = 42
    EXECUTE = 43
    PRINTSCREEN = 44
    INSERT = 45
    DELETE = 46
    KEYTOLETTER[46]='Delete'
    HELP = 47

    #Numbers
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57

    #Letters
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90

    #And specials again
    LWIN = 91
    RWIN = 92
    APPS = 93
    SLEEP = 95

    #Numpad
    class Numpad:
        #Numbers
        ZERO = 96
        ONE = 97
        TWO = 98
        THREE = 99
        FOUR = 100
        FIVE = 101
        SIX = 102
        SEVEN = 103
        EIGHT = 104
        NINE = 105

        #Specials
        MULTIPLY = 106
        ADD = 107
        SEPERATOR = 108
        SUBTRACT = 109
        DECIMAL = 110
        DIVIDE = 111

    #Function keys
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135

    #Specials...
    LSHIFT = 160
    RSHIFT = 161
    LCTRL = 162
    RCTRL = 163
    LALT = 164
    RALT = 165

    #Pointless ones?
    BROWSER_BACK = 166
    BROWSER_FORWARD = 167
    BROWSER_REFRESH = 168
    BROWSER_STOP = 169
    BROWSER_SEARCH = 170
    BROWSER_FAVORITES = 171
    BROWSER_HOME = 172
    VOLUME_MUTE = 173
    VOLUME_DOWN = 174
    VOLUME_UP = 175
    MEDIA_NEXT_TRACK = 176
    MEDIA_PREV_TRACK = 177
    MEDIA_STOP = 178
    MEDIA_PLAY_PAUSE = 179
    LAUNCH_MAIL = 180
    LAUNCH_MEDIA_SELECT = 181
    LAUNCH_APP1 = 182
    LAUNCH_APP2 = 183

    #Stuff?
    OEM_1 = 186         #The US ;: key
    PLUS = 187
    COMMA = 188
    MINUS = 189
    FULL_STOP = 190
    OEM_2 = 191         #The US /? key
    OEM_3 = 192         #The US ~ key
    OEM_4 = 219         #The US [{ key
    OEM_5 = 220         #The US \| key
    OEM_6 = 221         #The US ]} key
    OEM_7 = 222         #The US '" key
    OEM_8 = 223         #Misc
    OEM_102 = 226       #Eh?

    #Ugh
    PLAY = 250
    ZOOM = 251
    NO_NAME = 252
    CLEAR = 253
    
    for i in range(len(string.ascii_lowercase)):
        KEYTOLETTER[i+65]=string.ascii_lowercase[i]

    for i in range(10):
        KEYTOLETTER[i+48]=str(i)

    for i in range(24):
        KEYTOLETTER[i+112]='F'+str(i+1)

    for i in range(10):
        KEYTOLETTER[i+48]=str(i)
        

    KEYTOLETTER[SPACE]=' '
    
    
