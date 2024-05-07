from ursina import *
from math import *
from time import process_time 


def oscSim(self):
 self.t += time.dt

 self.mercury.x = 2*math.cos(10*(self.t)) + self.position.x
 self.mercury.y = self.position.y
 self.mercury.rotation += Vec3(0,1,0)
 self.mercury.z = 2*math.sin(10*(self.t)) + self.position.z

 self.venus.x = 5*math.cos(self.t) + self.position.x
 self.venus.y = self.position.y
 self.venus.rotation += Vec3(0,1,0)
 self.venus.z = 5*math.sin(self.t) + self.position.z

 self.earth.x = 8*math.cos(.5*(self.t)) + self.position.x
 self.earth.y = self.position.y
 #self.earth.rotation is used just for QOL purposes
 #it makes the earth rotate, does nothing else
 #to quote Marge Simpson "I just think it's neat"
 self.earth.rotation += Vec3(0,1,0)
 self.earth.z = 8*math.sin(.5*(self.t)) + self.position.z

 self.mars.x = 11*math.cos(.3*(self.t)) + self.position.x
 self.mars.y = self.position.y
 self.mars.rotation += Vec3(0,1,0)
 self.mars.z = 11*math.sin(.3*(self.t)) + self.position.z

 self.jupiter.x = 14*math.cos(.1*(self.t)) + self.position.x
 self.jupiter.y = self.position.y
 self.jupiter.rotation += Vec3(0,1,0)
 self.jupiter.z = 14*math.sin(.1*(self.t)) + self.position.z

 self.saturn.x = 17*math.cos(.09*(self.t)) + self.position.x
 self.saturn.y = self.position.y
 self.saturn.rotation += Vec3(0,1,0)
 self.saturn.z = 17*math.sin(.09*(self.t)) + self.position.z

 self.uranus.x = 20*math.cos(.06*(self.t)) + self.position.x
 self.uranus.y = self.position.y
 self.uranus.rotation += Vec3(0,1,0)
 self.uranus.z = 20*math.sin(.06*(self.t)) + self.position.z

 self.neptune.x = 23*math.cos(.05*(self.t)) + self.position.x
 self.neptune.y = self.position.y
 self.neptune.rotation += Vec3(0,1,0)
 self.neptune.z = 23*math.sin(.05*(self.t)) + self.position.z

 self.pluto.x = 26*math.cos(.01*(self.t)) + self.position.x
 self.pluto.y = self.position.y
 self.pluto.rotation += Vec3(0,1,0)
 self.pluto.z = 26*math.sin(.01*(self.t)) + self.position.z


 #self.moon rotates around the earth using the exact same code that the earth does
 #but instead of using self.position you use self.earth
 #it dips into the sun just a teeny bit, but that keeps it spicy
 self.moon.z= (1/2)*math.sin(1*(self.t)) + self.earth.z
 self.moon.x= (1/2)*math.cos(1*(self.t)) + self.earth.x
 self.moon.y=self.position.y