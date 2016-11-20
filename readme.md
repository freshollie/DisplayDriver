# DisplayDriver

Display Driver is an ascii display engine for python and began development
in august 2013. The engine is not very powerful but gives functional object
oriented programming. It was developed and so designed to work on windows only
and has never been tested on other platforms.

# Usage

DisplayDriver is designed to work on python 2.7 and 3.x, and does not need any
other modules other than built in modules to work.

The best way to understand how to program with display driver is to look
at the syntax I have used with the example games: Tetris, Pong, Pacman, and Snake,
all of which function far better than I ever expected them to.

The main concept of programming in Display Driver is Ticks, Display Driver
runs on a task based system, you add the task you want to be completed
and DisplayDriver will execute that task every frame before showing the
pixels.

Displaying something on screen is simple. Initialise a GuiObjectBase
with an image which is a 2D list, the 2D lists corripond directly
to what the image will look like on the screen.

For example:

 O
 
-|-

/ \

In 2D list form would be

[

 [' ','O'],

 ['-',|','-'],
 
 ['/',' ','\\']
 
]

After the object has initialised it can be rendered with the method render
of the GuiObjectBase, for example:

stickMan=GuiObjectBase(image=stickManLook)
stickMan.render(DisplayDriver.engine)

DisplayDriver being the DisplayDriver module


# Modules

Intervals - Idea taken from Panda3D, runs a new function every frame
with delays if needed designed for things like particle effects.

Input - Written mostly by Jamie Read, Input uses the win32api to collect
keyboard inputs. These keyboard inputs are bound to specific functions.
Input needs to be run in it's own thread if used. This does not affect
functionallity.

Colour - A module which most of the code for was found online. Used to
add colour to the terminal on windows.
