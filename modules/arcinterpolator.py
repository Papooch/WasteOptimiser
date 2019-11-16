import re
import numpy as np
from operator import add, sub
import matplotlib.pyplot as plt


def cart2pol(x, y):
   rho = np.sqrt(x**2 + y**2)
   phi = np.arctan2(y, x)
   return [rho, phi] 


def pol2cart(rho, phi):
   x = rho * np.cos(phi)
   y = rho * np.sin(phi)
   return [x, y]


def interpolateArc(startAngle, endAngle, center, radius, maxlength=1, maxangle=.2, clockwise=True):
   #radius = math.sqrt((ceter(0)-end(0))**2 + (center(1)-end(1))**2)
   ccwangle = endAngle - startAngle
   if ccwangle <= 0: ccwangle += np.pi*2
   if ccwangle >= 2*np.pi: ccwangle -= np.pi*2
   cwangle = 2*np.pi - ccwangle
   ccwlength = ccwangle*radius
   cwlength = cwangle*radius
   print(f'Clockwise angle is {round(cwangle, 4)}, Anti-clockwise angle is {round(ccwangle, 4)}')
   print(f'Clockwise lenght is {round(cwlength, 4)}, Anti-clockwise lenght is {round(ccwlength, 4)}')

   points = []

   if clockwise:
      lsegments = 0
      asegments = 0
      if cwlength >= maxlength:
         lsegments = int(cwlength/maxlength)
      if cwangle >= maxangle:
         asegments = int(cwangle/maxangle)

      arcstops = list(np.linspace(0, cwangle, max(lsegments,asegments)+1))
      for arc in arcstops:
         points.append(pol2cart(radius, startAngle - arc))


   x, y = zip(*points)
   plt.plot(*pol2cart(radius, startAngle), 'r*')
   plt.plot(x, y)

   plt.show()



interpolateArc(np.pi, np.pi/2, [0, 0], 50, 20, .2)