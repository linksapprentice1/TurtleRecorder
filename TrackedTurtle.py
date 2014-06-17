from turtle import *

class TrackedTurtle():
   def __init__( self ):
       self.path = []

   def updatePath(self, color, pen_down, x, y):
       self.path.append((color, pen_down, x, y))

   def trimPath(self):
       trimmed_path = []
       for p1, p2 in zip(self.path, self.path[1:]):
           if p1[1] or p2[1]:
               trimmed_path.append(p1)
       self.path = trimmed_path

   def followPath(self):
       self.turtle = Turtle()
       self.turtle.pensize(3) 
       for color, pen_down, x, y in self.path:
           self.turtle.pencolor(color) 
           self.turtle.pendown() if pen_down else self.turtle.penup()
           self.turtle.setpos((x, y))

   def resetPath(self):
       self.path = []

