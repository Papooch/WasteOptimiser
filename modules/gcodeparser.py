import re
import numpy as np
from operator import add, sub


def split_gcode(text):
   return re.split("\s", text)

def cart2pol(x, y):
   rho = np.sqrt(x**2 + y**2)
   phi = np.arctan2(y, x)
   return [rho, phi] 

def pol2cart(rho, phi):
   x = rho * np.cos(phi)
   y = rho * np.sin(phi)
   return [x, y]

def interpolateArc(start, end, center, maxlength, maxangle, clockwise=True):
   radius = math.sqrt((ceter(0)-end(0))**2 + (center(1)-end(1))**2)
   startOrigin = list(map(sub, start, center))
   endOrigin = list(map(sub, end, center))
   startAngle = cart2pol(*startOrigin)
   endAngle = cart2pol(*endOrigin)
   angle = abs(endAngle - startAngle)



class ShapeExtractor:
   def __init__(self, gcode):
      self.gcode = gcode
      self.instructions = []
      self.waitigForParams = False
      self.penDown = False
      self.lastPenDown = False
      self.absoluteMove = True
      self.coords = [0, 0]
      self.shapeList = []
      self.currentShape = []

   def run(self):
      self.instructions = split_gcode(self.gcode)
      for inst in self.instructions:
         self._interpret_instruction(inst)


   def _interpret_instruction(self, inst):
      mode = self._instruction_mode(inst)
      if mode == 0:
         return
         #print(inst, " is not important")
      elif mode == 1: # move instruction
         code = int(inst[1:])
         message = ""
         if code >= 90:
            self.waitingForParams = False
            self._finish_shape()
         elif code <= 5:
            self.waitingForParams = True
         else: print(inst, "also not important"); return

         if code == 90:
            self.absoluteMove = True
            message = "setting absolute move"
         elif code == 91:
            self.absoluteMove = False
            message = "setting relative move"
         
         if code == 00:
            self._finish_shape()
            self.penDown = False
            message = "pen up"
         else:
            if self.penDown: self.currentShape.append(self.coords.copy())
            self.penDown = True
            #message = "pen down"

         print(inst, " ", message)
      elif mode == 2: # move coordinates
         coord = float(inst[1:])
         idx = 0
         if inst[0] == "X": idx = 0
         elif inst[0] == "Y": idx = 1
         self.coords[idx] = coord + (not self.absoluteMove)*self.coords[idx] # add current coords if in relative mode
         print("\t", inst[0], "=", coord)

         print("\t\t", [round(c, 8) for c in self.coords])


   def _finish_shape(self):
      if self.currentShape:
         self.currentShape.append(self.coords.copy())
         self.shapeList.append(self.currentShape)
         self.currentShape = []


   def _instruction_mode(self, inst):
      if not inst:
         return 0
      elif inst[0] == "G":
         return 1
      elif inst[0] in ["X", "Y"]:
         return 2
      else:
         return 0




class VMachine:
   def __init__(self, units='mm', mode=0, position=[0, 0]):
      self.units = 'units' # 'mm' | 'in'
      self.mode = mode     # 0:absolute, 1:incremental
      self.position = position

   def move(self,pos):
      self.position


class GParser:
   def __init__(self, file):
         self.gcode = open(file, 'r').read().split(" ")

   def _parse_line(self, line):
      pass

if __name__ == "__main__":
   import matplotlib.pyplot as plt

   gcode = None
   with open("../gcode/1-ctverec.gcode", 'r') as f:
      gcode = f.read()
   
   #print(split_gcode(gcode))
   xtr = ShapeExtractor(gcode)
   xtr.run()
   
   for shape in xtr.shapeList:
      x, y = zip(*shape)
      plt.plot(x, y)

   plt.show()


