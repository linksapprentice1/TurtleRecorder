import os
import subprocess
import inspect
import shutil
import sys

def generateFiles(tracked_turtle):
   py_file = "TurtleRecording.py"

   #create executable on Windows
   if os.name == "nt":
      py_dir = _mkdir("./TurtleRecording1/")
      _generatePy(py_dir + py_file, tracked_turtle)
      _generateTrackedTurtleModule(py_dir, tracked_turtle)
      _generateSetup(py_file, py_dir)
      _generateExe(py_dir)
      _generateBat(py_dir[:-2] + ".exe", py_dir)
      _movePyFiles(py_dir, py_dir + "src/")
      subprocess.Popen("explorer " + os.path.normpath(py_dir))

   #just open python file on Linux
   elif os.name == "posix":
      _generatePy(py_file, tracked_turtle)
      subprocess.Popen(["nautilus", os.getcwd()])
      subprocess.Popen(["gedit", py_file])

   sys.exit()

def _incrementDir(the_dir):
   return the_dir[:-2] + str(int(the_dir[-2])+1) + the_dir[-1]

def _mkdir(the_dir):
   while os.path.exists(the_dir):
      the_dir = _incrementDir(the_dir)
   os.makedirs(the_dir)
   return the_dir

def  _generateTrackedTurtleModule(py_dir, tracked_turtle):
   f = open(py_dir + "TrackedTurtle.py", 'w')
   f.write(inspect.getsource(inspect.getmodule(tracked_turtle)))
   f.close()

def _generatePy(py_file, tracked_turtle):
   f = open(py_file, 'w')
   f.write("""from TrackedTurtle import *
turtle = TrackedTurtle()
turtle.path = """ + str(tracked_turtle.path) + """
turtle.followPath()""")
   f.close()

def _generateSetup(py_file, py_dir = ""):
   f = open(py_dir + "setup.py", 'w')
   f.write("""from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(
   windows = ['""" + py_file + """'],
   options = {
      'py2exe': {
      'packages': 'Tkinter, turtle, tkColorChooser',
      'includes': 'TrackedTurtle, collections, os, subprocess'
      }
   }
)""")
   f.close()

def _generateExe(py_dir = ""):
   os.chdir(py_dir)
   subprocess.call("python setup.py")
   os.chdir("..")

def _generateBat(exe_name, py_dir = ""):
   f = open(py_dir + "CLICK_ME.bat", 'w')
   f.write("cd dist\nstart " + exe_name + "\nexit 0")
   f.close()

def _movePyFiles(py_dir, src_dir):
   os.makedirs(src_dir)
   for f in os.listdir(py_dir):
      if f.endswith(".py"):
         shutil.copy(py_dir + f, src_dir)
         os.remove(py_dir + f)
