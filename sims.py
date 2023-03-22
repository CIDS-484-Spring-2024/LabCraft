from ursina import *

global Amp
Amp=20
f = open("Pendulum", "w") 
p = open("Planet", "w")
z =open("Z", "w")
f.write("time "+"theta "+'\n')
T=0
Z=0
def input(key):
 global Amp
 if key == ('1'):
  Amp=1
 if key == ('2'):
  Amp=2
 if key == ('3'):
  Amp=3
 if key == ('4'):
  Amp=4
 if key == ('5'):
  Amp=5
 if key == ('6'):
  Amp=6
 if key == ('7'):
  Amp=7
 if key == ('8'):
  Amp=8
 if key == ('9'):
  Amp=9
  
def oscSim(self):
 self.t += time.dt
 self.planet.x = math.cos(.5*(self.t)) + self.position.x
 self.planet.y = self.position.y-.4
 self.planet.rotation += Vec3(0,1,0)
 self.planet.z = math.sin(.5*(self.t)) + self.position.z
 global T
 Format=self.planet.rotation[1]
 p.write(str(T)+","+str(round(Format,2))+"\n")
 T=T+1
def simple_pendulum(self):
 self.t += time.dt
 global Z
 global T
 global Amp
 
 freq=.5
 angle=0
 self.pendulum.x = self.position.x+.7
 angle= Amp*math.sin(2*math.pi*freq*self.t)
 self.pendulum.y=self.position.y
 self.pendulum.z=self.position.z
 #self.pendulum.y = math.sin(self.t)+self.position.y
 #self.pendulum.z = -math.cos(self.t)+self.position.z
 self.pendulum.rotation = Vec3(angle,0,0)
 format=self.pendulum.rotation[0]/360
 f.write(str(T)+","+str(round(format,2))+"\n")
 z.write(str(Z)+"\n")