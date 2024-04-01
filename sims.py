from ursina import *
from math import *
from time import process_time 
import os.path
#f writes to the Pendulum file, so students can graph and chart
# based off the values they input for Amplitude and Frequency
Pend_file = open("Pendulum", "w") 
Pend_file.write("time "+"oscilations "+'\n')
#p writes to the earth file, so students can graph and chart
#based off of the X position the Z position, and the time it takes to complete
#them with the System sim
Earth_file = open("earth", "w")
Earth_file.write("time "+","+"Z-Pos"+","+"X-Pos"+'\n')
#T is used as an incremental value to represent time in
#the Solar System file
T=0
path = r"C:\Users\Zach's LapTop\onedrive\desktop\gitlabcraft\labcraftzach\Test"
name_of_file= "cannon"
complete_path=os.path.join(path+name_of_file)
Cannon_file = open(complete_path, "w")
Cannon_file.write(" Y coordinate "+":"+ " X coordinate "+":" " Time "+'\n')



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

 global T
 Earth_file.write(str(T)+","+str(round(self.earth.z,2))+","+str(round(self.earth.x,2))+"\n")
 T=T+1
 #self.moon rotates around the earth using the exact same code that the earth does
 #but instead of using self.position you use self.earth
 #it dips into the sun just a teeny bit, but that keeps it spicy
 self.moon.z= (1/2)*math.sin(1*(self.t)) + self.earth.z
 self.moon.x= (1/2)*math.cos(1*(self.t)) + self.earth.x
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
 Pend_file.write(str(round(self.t,2))+","+str(round(format,2))+"\n")
#beginning of apple sim
"""
def apple_sim(self):
  self.gravity=9.8/(self.t +0.000001)
  self.t += time.dt
  #x and z are the same as the button
  self.apple.x=self.position.x
  self.apple.z=self.position.z
  #y starts higher then the button so players can get a better look as the apple falls
  self.apple.y=3-self.t
  
"""
def cannon_sim(self):
    #using the formula for the point of a projectile at a given moment 
    #this simulation was created
    self.t+=time.dt
    
    angle_rad = radians(self.Angle)
    self.rotation=(self.Angle,180,0)
    self.velocityX=math.cos(angle_rad)*self.Velocity
    self.velocityY=math.sin(angle_rad)*self.Velocity
    self.gravity= 9.8
    Cannon_file.write(str(round(self.apple.y,2))+","+str(round(self.apple.z,2))+","+str(round(self.t,2))+"\n")
    self.e = Entity(model='cube', color=color.orange, scale=(0.05,time.dt,1),position=(self.apple.x,self.apple.y,self.apple.z), rotation=(0,0,0), texture='brick')
    self.apple.z +=0+self.velocityX*time.dt
    self.apple.y = 2.3+self.velocityY*self.t-((self.gravity*(self.t*self.t))/2)
    self.apple.x = self.x  
    
    

def while_sim(self):
  #simple while loop sim, while the player is in the block it's night
  #while the player is out of the block it's day
  if abs(self.player.x-self.block.x)<=.1 and abs(self.player.z-self.block.z)<=.1:
            self.block.color=color.blue
            self.Night=0
  if abs(self.player.x-self.block.x)>=.1 and abs(self.player.z-self.block.z)>=.1:
            self.block.color=color.red
            self.Night=1
def FV_sim(self):
   #simple force vector sim have fun seeing what you can do
   self.y=self.y
   self.x+=1

   
   
def Friction_sim(self):
   #Simple friction sim an initial forcce is decremented exponetially by a friction force
    if self.FricCo > 0:
      #initial force
      self.x=self.x+(5*time.dt)*self.FricCo
      #friction force
      self.FricCo=self.FricCo-.1
    self.z=self.z
def Loop_sim(self):
  #This is to make it less flashy
  Time_incr= 2*time.dt
  
  #For_Loop made out of if statements
  #because game loops don't apprieciate while or for loops
  
  #checks to see if the player is inside the block
  if abs(self.player.x-self.block.x)<=.5 and abs(self.player.z-self.block.z)<=.5:
           #then for 10 seconds
           #t is in cremented by 2 
           #and if the modulous of that is 1 we have day
           #and if it's 0 we have night
           if self.t<10:
              
               self.t+=Time_incr
               if int(self.t)%2==1:
                   self.Night=1
               if int(self.t)%2==0:
                   self.Night=0
           #then at the end everything is set back to 0
           if self.t>=10:
               self.Night=1
               
               
      
  
          
              

            

  
  