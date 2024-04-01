
from ursina import *
import importlib

import TextTset

app = Ursina(vsync=60)
roof = False
Write_Bool = False
TestInt1 = 2
TestInt2 = 2
window.color = color.color(0, 0, 0)
Button.default_color = color._20
window.color = color._25
Barg = ""
with open("C:/Users/Zach's LapTop/OneDrive/Desktop/GitLabcraft/labcraftZach/CapStone/TextTset.py", 'r+') as f:
    # Read the entire content of the file
    Barg = f.read()

file_text = TextField(max_lines=30, scale=1, register_mouse_input = True, text='1234',wordwrap = 30)
from textwrap import dedent
file_text.text = dedent(Barg)
b = Button(model='quad', scale=.35, x=-.5, color=color.lime, text='click me, to write to file', text_size=.5, text_color=color.black)
c = Button(model='quad', scale=.4, x=.5, color=color.lime, text='click me, to write to test method', text_size=.5, text_color=color.black)
file_text.render()

def Write_To_Meth():
    global Write_Bool
    with open("C:/Users/Zach's LapTop/OneDrive/Desktop/GitLabcraft/labcraftZach/CapStone/TextTset.py", 'w') as f:
        f.write(file_text.text)
    Write_Bool = True

def Test_Meth():
    importlib.reload(TextTset)
    global roof
    roof = True
def update():
    global Write_Bool
    global roof
    global TestInt1
    global TestInt2
   
    if held_keys["enter"]:
        file_text.text+= '\n'
    if not Write_Bool:
        b.on_click = (Write_To_Meth)
    if not roof:
        c.on_click = (Test_Meth)
    if roof == True:
        try:
            print(TextTset.addem(TestInt1,TestInt2))
        except:
            print("noop<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        roof = False
    if Write_Bool == True:
        
        Write_Bool = False
app.run()

