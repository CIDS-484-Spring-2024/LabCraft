from ursina import*
global num
num=0
def Convrt():
 global num
 global Box
 num=int(Box.text)
def Print():
 global num
 global bum
 bum=1
 print(num+bum)
 destroy(Box)
 destroy(chuck)
 destroy(duck)
#chuck = Button(scale=.1, y=-.2, color=color.blue)
def update ():
 global Box
 global chuck
 #Box = InputField()
 #chuck = Button(scale=.1, y=-.2, color=color.blue)
 #chuck.on_click = print("click")
app = Ursina()
global Box
#global num

global bum
Box = InputField()
chuck = Button(scale=.1, y=-.2, color=color.blue)
chuck.on_click = Convrt
duck = Button(scale=.1, y=-.2, x=.4, color=color.red,text="Hi")
duck.on_click = Print
app.run()