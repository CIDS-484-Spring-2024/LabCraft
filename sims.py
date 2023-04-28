from ursina import *


#f writes to the Pendulum file, so students can graph and chart
# based off the values they input for Amplitude and Frequency
f = open("Pendulum", "w") 
f.write("time "+"oscilations "+'\n')
#p writes to the Planet file, so students can graph and chart
#based off of the X position the Z position, and the time it takes to complete
#them with the System sim
p = open("Planet", "w")
p.write("time "+","+"Z-Pos"+","+"X-Pos"+'\n')
#T is used as an incremental value to represent time in
#the Solar System file
T=0



def oscSim(self):
 self.t += time.dt
 self.planet.x = math.cos(.5*(self.t)) + self.position.x
 self.planet.y = self.position.y
 #self.planet.rotation is used just for QOL purposes
 #it makes the planet rotate, does nothing else
 #to quote Marge Simpson "I just think it's neat"
 self.planet.rotation += Vec3(0,1,0)
 self.planet.z = math.sin(.5*(self.t)) + self.position.z
 global T
 p.write(str(T)+","+str(round(self.planet.z,2))+","+str(round(self.planet.x,2))+"\n")
 T=T+1
 self.moon.z=math.sin(1*(self.t)) + self.planet.z-.1
 self.moon.x=math.cos(1*(self.t)) + self.planet.x-.1
 self.moon.y=self.position.y
def simple_pendulum(self):
 self.t += time.dt
 #freq and amp have default values, that are changed
 #based off of user input, the code for this is in the labcraft.py file
 #the reason they have default values is because the simulation won't work
 #with just a declared variable to start, it needs a defined value
 freq=.5
 angle=0
 self.pendulum.x = self.position.x+.7
 #do not fricking delete the self.Amp variable I put a lot of work into making that work
 angle= self.Amp*math.sin(2*math.pi*self.Freq*self.t)
 self.pendulum.y=self.position.y
 self.pendulum.z=self.position.z
 self.pendulum.rotation = Vec3(angle,0,0)
 #You can't for some reason write the angle to the file, so I just set it equal to format
 #format and angle are the same variable type, I don't know why, I'm very tired. I'd come back to it
 #but I'm always very tired.
 format=angle
 #the values writen to the file is the angle and whatever the time is for the corresponding angle
 #if you want to change any variable for the file, just delete the variable that is inside the 
 #(round(EXAMPLE,2)) code.
 f.write(str(round(self.t,2))+","+str(round(format,2))+"\n")