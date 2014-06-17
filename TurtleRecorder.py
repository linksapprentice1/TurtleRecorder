from Tkinter import *
from TrackedTurtle import *
from TrackedTurtleFiles import *
from collections import *
from tkColorChooser import *    

SIZE = 750

class GUI( Frame ):
   def __init__( self ):
      Frame.__init__( self )

      self.turtle = TrackedTurtle()

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
      self.turtle.trimPath()
      self.turtle.followPath()

   def done(self):
      self.turtle.trimPath()
      generateFiles(self.turtle)

   def reset(self):
      self.turtle.resetPath()
      self.canvas.delete("all")

   def changeDrawStatus(self, event):
      self.is_drawing = not self.is_drawing

   def paint( self, event ):
      if event.x < 0 or event.y < 0:
          return
      if self.is_drawing:
          self.turtle.updatePath(self.color, pen_down = True, x = event.x-SIZE/2, y = SIZE/2-event.y)
          self.canvas.create_oval((event.x - 3, event.y - 3, event.x + 3, event.y + 3), fill = self.color)
      else:
          self.turtle.updatePath(self.color, pen_down = False, x = event.x-SIZE/2, y = SIZE/2-event.y)

   def pickColor(self):
       self.color = askcolor(self.color, title = "Choose pen color")[1] or self.color

def runGUI():
   GUI().mainloop()
