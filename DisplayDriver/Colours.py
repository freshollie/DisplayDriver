"""
Colors text in console mode application (win32).
Uses ctypes and Win32 methods SetConsoleTextAttribute and
GetConsoleScreenBufferInfo.

$Id: color_console.py 534 2009-05-10 04:00:59Z andre $
"""

from ctypes import windll, Structure, c_short, c_ushort, byref

SHORT = c_short
WORD = c_ushort

class COORD(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("X", SHORT),
    ("Y", SHORT)]

class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

# winbase.h
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# wincon.h
FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

def getTextAttr():
  """Returns the character attributes (colors) of the console screen
  buffer."""
  csbi = CONSOLE_SCREEN_BUFFER_INFO()
  GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
  return csbi.wAttributes

def setTextAttr(color):
  """Sets the character attributes (colors) of the console screen
  buffer. Color is a combination of foreground and background color,
  foreground and background intensity."""
  SetConsoleTextAttribute(stdout_handle, color)

colourDict={'black',FOREGROUND_BLACK,
            'blue', FOREGROUND_BLUE,
            'green', FOREGROUND_GREEN,
            'cyan', FOREGROUND_CYAN,
            'red', FOREGROUND_RED,
            'magenta', FOREGROUND_MAGENTA,
            'yellow', FOREGROUND_YELLOW,
            'grey', FOREGROUND_GREY
            }

colourToKey={'black','FOREGROUND_BLACK',
            'blue', 'FOREGROUND_BLUE',
            'green', 'FOREGROUND_GREEN',
            'cyan', 'FOREGROUND_CYAN',
            'red', 'FOREGROUND_RED',
            'magenta', 'FOREGROUND_MAGENTA',
            'yellow', 'FOREGROUND_YELLOW',
            'grey', 'FOREGROUND_GREY'
            }

backgroundColourDict={
            'black',BACKGROUND_BLACK,
            'blue', BACKGROUND_BLUE,
            'green', BACKGROUND_GREEN,
            'cyan', BACKGROUND_CYAN,
            'red', BACKGROUND_RED,
            'magenta', BACKGROUND_MAGENTA,
            'yellow', BACKGROUND_YELLOW,
            'grey', BACKGROUND_GREY
            }

backgroundColourToKey={
            'black','BACKGROUND_BLACK',
            'blue', 'BACKGROUND_BLUE',
            'green', 'BACKGROUND_GREEN',
            'cyan', 'BACKGROUND_CYAN',
            'red', 'BACKGROUND_RED',
            'magenta', 'BACKGROUND_MAGENTA',
            'yellow', 'BACKGROUND_YELLOW',
            'grey', 'BACKGROUND_GREY'
            }

class ColouredString(str):
  def __init__(self,string):
    str.__init__(self,string)

  def applyEffect(self, effect):
    for i in range(len(self)):
      self[i]=None

  def setColour(self, colour):
    if colour in colourDict:
      self.applyEffect(colourToKey['colour'])

  def setBackground(self,colour):
    if colour in backgroundColourDict:
      self.background=colour
