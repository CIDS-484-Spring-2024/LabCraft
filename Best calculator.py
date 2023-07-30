from ursina import*


app = Ursina()
window.fullscreen = True
#picture ratios are 1.9 to 1
Slidetexture1=load_texture('assets/Slide1.png')
Slidetexture2=load_texture('assets/Slide 2.png')
Slidetexture3=load_texture('assets/Slide 3.png')
Bob=Entity(model="quad", texture="assets/Slide1.png", position=(0,0,0), scale=(16.15,8.5))
CoBoo = Button(scale=(.5,.1), x=-.6,y=-.2,color=color.rgb(189,0,255),text="Start Game")
BooCo = Button(scale=(.3,.1),x=-.7,y=-.3,color=color.rgb(1,255,31),text="Exit Game")
global q
q=0
def update():
    global q
    if int(q%3)==0:
        Bob.texture=Slidetexture1
    if int(q%3)==1:
        Bob.texture=Slidetexture2
    if int(q%3)==2:
        Bob.texture=Slidetexture3
    q+=(.5*time.dt)
    CoBoo.on_click=application.quit
    BooCo.on_click=application.quit

app.run()