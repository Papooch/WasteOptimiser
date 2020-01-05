import re
import numpy as np
from operator import add, sub


def cart2pol(x, y):
   """Converts cartesian coordinates to polar"""

   rho = np.sqrt(x**2 + y**2)
   phi = np.arctan2(y, x)
   return [rho, phi]


def pol2cart(rho, phi):
   """Converts polar coordinates to ccartesian"""

   x = rho * np.cos(phi)
   y = rho * np.sin(phi)
   return [x, y]


def interpolateArcAngle(startAngle, endAngle, radius, clockwise=True, maxlength=1, maxangle=.2):
   """Returns a list of points along the specified arc from start to end, ommiting the endpoint"""

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
   """Returns a list of points along the specified arc from start to end, ommiting the endpoint"""

   radius = np.sqrt((center[0]-end[0])**2 + (center[1]-end[1])**2)

   startAngle = np.arctan2(start[1]-center[1], start[0]-center[0])
   endAngle = np.arctan2(end[1]-center[1], end[0]-center[0])

   points = interpolateArcAngle(startAngle, endAngle, radius, clockwise=clockwise, maxlength=maxlength, maxangle=maxangle)
   points = [list(map(add, point, center)) for point in points]
   return points


class ShapeExtractor:
   def __init__(self, gcode, suppressLeadIn = False, arcMaxAngle = 0.2, arcMaxLength = 10, leadInTolerance = 0.1):
      self.gcode = gcode
      self.arcMaxAngle = arcMaxAngle
      self.arcMaxLength = arcMaxLength
      self.supressLeadIn = suppressLeadIn
      self.leadInTolerance = leadInTolerance

      self._instructions = re.split("\s", self.gcode)
      self._shapeList = []
      self._penDown = False
      self._absoluteMove = True
      self._coords = [0, 0]
      self._currentShape = []

   def get_shapes(self):
      """Returns list found shapes in gcode, optionally omits the lead-in move"""

      if self.supressLeadIn:
         outList = []
         for shape in self._shapeList:
            shape = np.array(shape)
            while np.linalg.norm(shape[0] - shape[-1]) >= self.leadInTolerance:
               shape = shape[1:]
            outList.append(shape.tolist())
         return outList
      return self._shapeList


   def run(self):
      """Iterates over all instructions and extracts shapes"""

      inst_iterator = iter(self._instructions) # create iterator of instruction so we can call next()
      for inst in inst_iterator:
         mode = self._instruction_mode(inst)
         if mode == 1:  # move instruction (G)
            code = int(inst[1:])
            message = ""
            if code >= 90: # set absolute or incremental move
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
                  #TODO: Add exception checking
                  coord = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  self._go_straight(coord)
                  self._penDown = False
                  message = "pen up"
               else: # something else, pen down
                  if self._penDown:
                     self._currentShape.append(self._coords.copy())
                  self._penDown = True
                  message = "pen down"
               message += " [" + str(round(self._coords[0], 5)) + " " + str(round(self._coords[1], 5)) + "]"

               if code == 1: # straigh line (expexting X#.# Y#.#)
                  #TODO: add exception checking
                  coord = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  self._go_straight(coord)
               elif code in [2, 3]: # cw, ccw arc (expecting X#.# Y#.# I#.# J#.#)
                  #TODO: add exception checking
                  end = [self._split_coordinates(next(inst_iterator), "X")[1], self._split_coordinates(next(inst_iterator), "Y")[1]]
                  center = [self._split_coordinates(next(inst_iterator), "I")[1], self._split_coordinates(next(inst_iterator), "J")[1]]
                  cw = True
                  if code == 3: cw = False
                  self._go_arc(end, center, cw)

            else:
               continue
            if 'debug' in globals() and debug: print(inst, message)


   def _go_straight(self, end):
      """Go in a straight line (can also be rapid travel move)"""

      for i in [0, 1]:
         self._coords[i] = end[i] + (not self._absoluteMove)*self._coords[i]


   def _go_arc(self, end, center, is_clockwise):
      """Arc interpolation move, always draws polyline of specified resolution"""

      if self._absoluteMove:
         start = self._coords
      else:
         start = [0, 0]       
      points = interpolateArc(start, end, center, is_clockwise, self.arcMaxLength, self.arcMaxAngle)
      if not self._absoluteMove:
         points = [list(map(add, point, self._coords)) for point in points]
      self._currentShape.extend(points)
      for i in [0, 1]:
         self._coords[i] = end[i] + (not self._absoluteMove)*self._coords[i]


   def _finish_shape(self):
      """Adds current shape to shapeList and creates a new empty one"""

      if self._currentShape:
         self._currentShape.append(self._coords.copy())
         self._shapeList.append(self._currentShape)
         self._currentShape = []
         if 'debug' in globals() and debug: print("Shape finished")


   def _instruction_mode(self, inst):
      """Returns a number depending on instruction type """ #TODO: Deprecate this
      if not inst:
         return 0
      elif inst[0] == "G":
         return 1
      elif inst[0] in ["X", "Y", "I", "J"]:
         return 2
      else:
         return 0


   def _split_coordinates(self, inst, expecting=""):
      """Return a tuple of Letter and Value of an instruction, optionally checks for expected letter"""

      if expecting and expecting != inst[0]:
            raise ValueError(f'Expected {expecting}, got {inst[0]}')     
      return (inst[0], float(inst[1:]))


if __name__ == "__main__":
   import matplotlib.pyplot as plt

   debug = True

   gcode = None
   with open("../../gcode/2-drzak.gcode", 'r') as f:
      gcode = f.read()

   #print(split_gcode(gcode))
   xtr = ShapeExtractor(gcode)
   xtr.supressLeadIn = True
   xtr.run()

   plt.axis('equal')

   for shape in reversed(xtr.get_shapes()):
      x, y = zip(*shape)
      plt.fill(x, y)

   plt.show()
