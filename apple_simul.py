from ursina import *
from math import *
from time import process_time 
import os.path

def apple_sim(self):
  self.gravity=9.8/(self.t +0.000001)
  self.t += time.dt
  #x and z are the same as the button
  self.apple.x=self.position.x
  self.apple.z=self.position.z
  #y starts higher then the button so players can get a better look as the apple falls
  self.apple.y=3-self.t