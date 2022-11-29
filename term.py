import platform
import os
from logging import basicConfig, getLogger
import distutils.spawn
import distutils.core
import subprocess
from tkinter import messagebox
import webbrowser
import ctypes,sys

gui_mode = ""

def gui_test():
  global gui_mode
  if gui_mode != False:
    try:
      response = messagebox.askokcancel('showinfo', "EIT-DevOps Cross-Platform Installer")
      if response == False:
        return sys.exit()
    except Exception as e:
      print("EIT-DevOps Cross-Platform Installer: cli mode")
      gui_mode = False
  return gui_mode

def main(argv):
  global gui_mode
  for i in range(1, len(sys.argv)):
    if sys.argv[i] in ("-h", "--help"):
      display_user_message("help")
      return sys.exit()
    elif sys.argv[i] in ("--cli"):
      gui_mode = False
    elif sys.argv[i] in ("-a", "--about"):
      about = True  
      
main(sys.argv)
print(gui_mode)