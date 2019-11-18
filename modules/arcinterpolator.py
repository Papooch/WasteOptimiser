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


def interpolateArc(startAngle, endAngle, radius, clockwise=True, maxlength=1, maxangle=.2):
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

   arcstops = list(np.linspace(0, angle, max(lsegments,asegments)+1))
   for arc in arcstops:
      points.append(pol2cart(radius, startAngle + arc * (1-2*clockwise)))

   x, y = zip(*points)
   plt.plot(x, y)
   plt.show()

   return points

if __name__ == "__main__":
   pointpoints = []
   pointpoints.append(interpolateArc(np.pi, np.pi/2, 50, True, 20, .2,))
   pointpoints.append(interpolateArc(np.pi, np.pi/2, 50, False, 20, .2,))

   for points in pointpoints:
      x, y = zip(*points)
      plt.plot(x, y)
   plt.show()