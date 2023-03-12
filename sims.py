from ursina import *


f = open("Pendulum", "w") 
p = open("Planet", "w")
f.write("time "+"theta "+'\n')
T=0
Z=0
def oscSim(self):
 self.t += time.dt
 self.planet.x = math.cos(self.t) + self.position.x
 self.planet.y = self.position.y
 self.planet.rotation += Vec3(0,5,0)
 self.planet.z = math.sin(self.t) + self.position.z
 global T
 Format=self.planet.rotation[1]
 p.write(str(T)+","+str(round(Format,2))+"\n")
 T=T+1   
def simple_pendulum(self):
 global Z
 global T
 while Z<=100:
  self.pendulum.x = self.position.x + .7
  self.pendulum.y = self.position.y
  self.pendulum.z = self.position.z
  self.pendulum.rotation += Vec3(1,0,0)
  Z=Z+1
  format=self.pendulum.rotation[0]/360
  f.write(str(T)+","+str(round(format,2))+"\n")
  T=T+1
  Z=Z+1
 while Z>=-100:
  self.pendulum.x = self.position.x + .7
  self.pendulum.y = self.position.y
  self.pendulum.z = self.position.z
  self.pendulum.rotation += Vec3(-1,0,0)
  Z=Z-1
  format=self.pendulum.rotation[0]/360
  f.write(str(T)+","+str(round(format,2))+"\n")
  T=T+1
  Z=Z-1
  
