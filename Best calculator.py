from ursina import *


app = Ursina()

x=0

Bob = Entity(model="cube")
Chuck = Button(scale=.1,x=-.2)

def CLRCHAN():
  global x
  x=1

Chuck.on_click = CLRCHAN

def update():
 
    global x
    if (x==0):
     Bob.color= color.blue
    if (not x==0):
      Bob.color = color.red
   # Chuck.on_click = x=1
    


app.run()