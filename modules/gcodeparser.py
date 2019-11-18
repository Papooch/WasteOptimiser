import re
import numpy as np
from operator import add, sub


def cart2pol(x, y):
   rho = np.sqrt(x**2 + y**2)
   phi = np.arctan2(y, x)
   return [rho, phi]


def pol2cart(rho, phi):
   x = rho * np.cos(phi)
   y = rho * np.sin(phi)
   return [x, y]


def interpolateArcAngle(startAngle, endAngle, radius, clockwise=True, maxlength=1, maxangle=.2):
   #radius = math.sqrt((ceter(0)-end(0))**2 + (center(1)-end(1))**2)
   angle = endAngle - startAngle
   if angle <= 0: angle += np.pi*2
   if angle >= 2*np.pi: angle -= np.pi*2
   if clockwise: angle = 2*np.pi - angle
   length = angle*radius

   points = []

   lsegments = 0
   asegments = 0
   if length >= maxlength:
      lsegments = int(length/maxlength)
   if angle >= maxangle:
      asegments = int(angle/maxangle)

   arcstops = list(np.linspace(0, angle, max(lsegments,asegments)+1, endpoint=False))
   for arc in arcstops:
      points.append(pol2cart(radius, startAngle + arc * (1-2*clockwise)))

   return points


def interpolateArc(start, end, center, clockwise=True, maxlength=20, maxangle=.4):
   radius = np.sqrt((center[0]-end[0])**2 + (center[1]-end[1])**2)

   startAngle = np.arctan2(-center[1], -center[0])
   endAngle = np.arctan2(end[1]-center[1], end[0]-center[0])

   #startAngle = cart2pol(*startOrigin)[1]
   #endAngle = cart2pol(*endOrigin)[1]
   points = interpolateArcAngle(startAngle, endAngle, radius, clockwise=clockwise, maxlength=maxlength, maxangle=maxangle)
   points = [list(map(add, point, center)) for point in points]
   points = [list(map(add, point, start)) for point in points]

   return points


class ShapeExtractor:
   def __init__(self, gcode):
      self.gcode = gcode
      self.arcMaxAngle = 0
      self.arcMaxLength = 0
      self.supressLeadIn = False
      self.leadInTolerance = 0.1

      self._instructions = re.split("\s", self.gcode)
      self._shapeList = []
      self._penDown = False
      self._absoluteMove = True
      self._coords = [0, 0]
      self._currentShape = []

   def get_shapes(self):
      if self.supressLeadIn:
         outList = []
         for shape in self._shapeList:
            shape = np.array(shape)
            while np.linalg.norm(shape[0] - shape[-1]) >= self.leadInTolerance:
               shape = shape[1:]
            outList.append(list(shape))
         return outList
      return self._shapeList


   def run(self):
      inst_iterator = iter(self._instructions)
      for inst in inst_iterator:
         mode = self._instruction_mode(inst)

         if mode == 1:  # move instruction
            code = int(inst[1:])
            message = ""
            if code >= 90:
               self._finish_shape()
               if code == 90:
                  self._absoluteMove = True
                  message = "setting absolute move"                
               elif code == 91:
                  self._absoluteMove = False
                  message = "setting relative move"

            elif code <= 5:
               if code == 00: # rapid move -> finish current shape
                  self._finish_shape()
                  message = "pen up"
                  coord = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  self._go_straight(coord)
                  self._penDown = False
               else: # something else, pen down
                  if self._penDown:
                     self._currentShape.append(self._coords.copy())
                  self._penDown = True
                  message = "pen down"
                  #message = "pen down"

               if code == 1: # straigh line (expexting X#.# Y#.#)
                  coord = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  self._go_straight(coord)
               elif code in [2, 3]: # cw, ccw arc
                  end = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  center = [self._split_coordinates(next(inst_iterator), "I")[1], self._split_coordinates(next(inst_iterator), "J")[1]]
                  cw = True
                  if code == 3: cw = False
                  self._go_arc(end, center, cw)

            else:
               continue

            print(inst, message)

   def _go_straight(self, end):
      for i in [0, 1]:
         self._coords[i] = end[i] + (not self._absoluteMove)*self._coords[i]

   def _go_arc(self, end, center, is_clockwise):
      if self._absoluteMove:
         start = self._coords
      else:
         start = [0, 0]
         
      points = interpolateArc(self._coords, end, center, is_clockwise)
      self._currentShape.extend(points)

      for i in [0, 1]:
         self._coords[i] = end[i] + (not self._absoluteMove)*self._coords[i]

   def _finish_shape(self):
      if self._currentShape:
         self._currentShape.append(self._coords.copy())
         self._shapeList.append(self._currentShape)
         self._currentShape = []

   def _instruction_mode(self, inst):
      if not inst:
         return 0
      elif inst[0] == "G":
         return 1
      elif inst[0] in ["X", "Y", "I", "J"]:
         return 2
      else:
         return 0

   def _split_coordinates(self, inst, expecting=""):
      if expecting and expecting != inst[0]:
            raise ValueError(f'Expected {expecting}, got {inst[0]}')     
      return [inst[0], float(inst[1:])]


if __name__ == "__main__":
   import matplotlib.pyplot as plt

   gcode = None
   with open("../../gcode/4-hvezda.gcode", 'r') as f:
      gcode = f.read()

   #print(split_gcode(gcode))
   xtr = ShapeExtractor(gcode)
   xtr.supressLeadIn = True
   xtr.run()

   for shape in xtr.get_shapes():
      x, y = zip(*shape)
      plt.plot(x, y)

   plt.show()
