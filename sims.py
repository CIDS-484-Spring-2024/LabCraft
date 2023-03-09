rom ursina import *


f = open("Pendulum", "w") 
p = open("Planet", "w")
f.write("time "+"theta "+'\n')
time =0
def oscSim(self):
 self.t += time.dt
 self.planet.x = math.cos(self.t) + self.position.x
 self.planet.y = self.position.y
 self.planet.rotation += Vec3(0,5,0)
 self.planet.z = math.sin(self.t) + self.position.z
            
def simple_pendulum(self):
 self.pendulum.x = self.position.x + .7
 self.pendulum.y = self.position.y
 self.pendulum.z = self.position.z
 self.pendulum.rotation += Vec3(1,0,0)
 global time
 format=self.pendulum.rotation[0]
 f.write(str(time)+","+str(round(format,2))+"\n")
 time=time+1
  
