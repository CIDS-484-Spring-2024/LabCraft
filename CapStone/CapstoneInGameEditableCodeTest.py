
from ursina import *


app = Ursina(vsync=60)


window.color = color.color(0, 0, 0)
Button.default_color = color._20
window.color = color._25
Barg = ""
with open("c:/Users/Zach's LapTop/OneDrive/Desktop/GitLabcraft/labcraftZach/CapStone/TextTset.py", 'r+') as f:
    # Read the entire content of the file
    Barg = f.read()
te = TextField(max_lines=30, scale=1, register_mouse_input = True, text='1234',wordwrap = 30)
from textwrap import dedent
te.text = dedent(Barg)

te.render()

if held_keys["enter"]:
    te.text+= '\n'
        
app.run()