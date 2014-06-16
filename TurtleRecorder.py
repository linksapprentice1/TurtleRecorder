from Tkinter import *
from collections import *
from turtle import *
from tkColorChooser import *                  
import subprocess
import os

SIZE = 750

class GUI( Frame ):
   def __init__( self ):
      Frame.__init__( self )

      self.track = Track()

      self.is_drawing = False 
      self.color = "blue" 

      self.pack(expand = YES, fill = BOTH)
      self.master.title("Turtle Recorder")
      self.master.geometry(str(SIZE) + "x" + str(SIZE))

      Button(self, text="Color", command=self.pickColor).pack()
      Button(self, text="Demo", command=self.demo).pack()
      Button(self, text="Done", command=self.done).pack()
      Button(self, text="Reset", command=self.reset).pack()
      
      self.canvas = Canvas(self)
      self.canvas.pack(expand = YES, fill = BOTH)
      self.canvas.bind("<Button-1>", self.changeDrawStatus)   
      self.canvas.bind("<Motion>", self.paint)

   def demo(self):
      self.track.deleteAdjacentPenUps()
      TrackedTurtle().followPath(self.track.path)

   def done(self):
      self.track.deleteAdjacentPenUps()
      generateCode(self.track.path)

   def reset(self):
      self.track = Track()
      self.canvas.delete("all")

   def changeDrawStatus(self, event):
      self.is_drawing = not self.is_drawing

   def paint( self, event ):
      if event.x < 0 or event.y < 0:
          return
      if self.is_drawing:
          self.track.updatePath(color = self.color, pen_down = True, x = event.x-SIZE/2, y = SIZE/2-event.y)
          self.canvas.create_oval((event.x - 3, event.y - 3, event.x + 3, event.y + 3), fill = self.color)
      else:
          self.track.updatePath(color = self.color, pen_down = False, x = event.x-SIZE/2, y = SIZE/2-event.y)

   def pickColor(self):
       self.color = askcolor(color = self.color, title = "Choose pen color")[1] or self.color

class Track():
   def __init__( self ):
       self.point = namedtuple("point", "x y")
       self.path = []

   def updatePath(self, color, pen_down, x, y):
       self.path.append((color, pen_down, self.point._make((x,y))))

   def deleteAdjacentPenUps(self):
       trimmed_path = []
       for p1, p2 in zip(self.path, self.path[1:]):
           if p1[1] or p2[1]:
               trimmed_path.append(p1)
       self.path = trimmed_path

class TrackedTurtle():
   def __init__( self ):
       self.turtle = Turtle()
       self.turtle.pensize(3) 

   def followPath(self, path):
       for color, pen_down, point in path:
           self.turtle.pencolor(color) 
           self.turtle.pendown() if pen_down else self.turtle.penup()
           self.turtle.setpos(point)

def generateCode(path):
   py_file = "TurtleRecorded.py"
   f = open(py_file, 'w')
   f.write("from TurtleRecorder import TrackedTurtle \nfrom collections import namedtuple\npoint = namedtuple('point', 'x y')\nturtle = TrackedTurtle()\npath= " + str(path) + "\nturtle.followPath(path)")
   subprocess.Popen(["notepad.exe" if os.name == "nt" else "gedit", py_file])

def runGUI():
   GUI().mainloop()
