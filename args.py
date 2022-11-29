import sys
import getopt

def display_user_message(msg):
  print(msg)

def main(argv):
  for i in range(1, len(sys.argv)):
    if sys.argv[i] in ("-h", "--help"):
      display_user_message("help")
      return sys.exit()
    elif sys.argv[i] in ("-q", "--quiet", "--silent"):
      silent_mode = True 
    elif sys.argv[i] in ("-y", "--yes"):
      assume_yes = True
    elif sys.argv[i] in ("-n", "--no"):
      assume_yes = False
    elif sys.argv[i] in ("-py", "--python"):
      install_python_tools = True
    elif sys.argv[i] in ("-ps", "--powershell"):
      install_powershell_tools = True
    elif sys.argv[i] in ("-c", "--config"):
      install_powershell_tools = True
    elif sys.argv[i] in ("-a", "--about"):
      about = True
      
main(sys.argv)