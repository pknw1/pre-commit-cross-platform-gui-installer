import platform
import os
from logging import basicConfig, getLogger
import distutils.spawn
import distutils.core
import subprocess
from tkinter import messagebox
import webbrowser
import ctypes,sys

logger = getLogger()
log_level = os.getenv("LOG_LEVEL", "INFO")
basicConfig(level=log_level, format="%(asctime)s:%(levelname)s: %(message)s")

gui_mode = ""
current_platform = platform.system()
logger.debug(f"OS Detected : {current_platform}")

progs = {
  "homebrew"             : ["homebrew", "brew", "/bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'", "https://brew.sh/", "post-install-config"],
  "python39_linux"       : ["python39", "python3.9", "sudo apt install -y python3.9", "https://www.python.org/downloads/", "post-install-config"],
  "python39_osx"         : ["python39", "python3.9", "breew install python39", "https://www.python.org/downloads/", "post-install-config"],
  "python39_windows"     : ["python39", "python3.exe", "python3.exe", "https://www.python.org/downloads/", "post-install-config"],
  "pip_linux"            : ["pip_linux", "pip", "sudo apt install -y python3-pip", "https://www.python.org/downloads/", "post-install-config"],
  "pip_osx"              : ["pip_osx", "pip", "brew install pip3", "", "post-install-config"],
  "pre-commit_linux"     : ["pre-commit_linux", "pre-commit", "pip install -U pre-commit", "", "https://github.com/pre-commit/pre-commit/blob/main/.pre-commit-config.yaml"],
  "pre-commit_osx"       : ["pre-commit_osx", "pre-commit", "brew install pre-commit", "", "https://github.com/pre-commit/pre-commit/blob/main/.pre-commit-config.yaml"],
  "pre-commit_windows"   : ["pre-commit_windows", "pre-commit", "pip install -U pre-commit", "", "https://github.com/pre-commit/pre-commit/blob/main/.pre-commit-config.yaml"],
  "black"                : ["black", "black", "pip install -U black", "https://github.com/psf/black", "https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html"],
  "mypy"                 : ["mypy", "mypy", "pip install -U mypy", "https://github.com/python/mypy", "https://mypy.readthedocs.io/en/stable/config_file.html"],
  "pylint"               : ["pylint", "pylint", "python3 -m pip install -U pylint", "https://pypi.org/project/pylint/", "post-install-config"],
  "isort"                : ["isort", "isort", "python3 -m pip install -U isort[requirements_deprecated_finder,pipfile_deprecated_finder]", "https://pypi.org/project/isort/", "post-install-config"],
  "pwsh"                 : ["pwsh", "pwsh", "wget -O /tmp/pwsh.deb https://github.com/PowerShell/PowerShell/releases/download/v7.2.6/powershell-lts_7.2.6-1.deb_amd64.deb && dpkg -i /tmp/pwsh.deb", "https://docs.microsoft.com/en-us/powershell/scripting/gallery/installing-psget?view=powershell-7.2", "post-install-config"],
  "pwsh_osx"             : ["pwsh_osx", "pwsh", "brew install --cask powershell", "https://docs.microsoft.com/en-us/powershell/scripting/gallery/installing-psget?view=powershell-7.2", "post-install-config"],
  "psget"                : ["psget", "", "Install-PackageProvider -Name NuGet -Force", "https://docs.microsoft.com/en-us/powershell/scripting/gallery/installing-psget?view=powershell-7.2", "post-install-config"],
  "PSScriptAnalyzer"     : ["PSScriptAnalyzer", "ScriptAnalyzer", "Install-Module PSScriptAnalyzer -Force", "", "post-install-config"],
  "superlinter"          : ["superlinter", "docker image inspect github/super-linter:latest", "docker pull github/super-linter:latest", "https://github.com/github/super-linter/releases", "post-install-config"],
  "snap"                 : ["snap", "snap", "apt install -y snapd", "snapd", "post-install-config"]

}

python_tools = [
    "black", "mypy", "pylint", "isort", "superlinter"
    ]

powershell_tools = [
  "PSScriptAnalyzer", "superlinter"
]

requires_config = [
  "black", "mypy"
]


if current_platform == 'Linux':
  requirements = ["snap", "python39_linux", "pip_linux", "pre-commit_linux", "pwsh"]
elif current_platform == 'Darwin':
  requirements = ["homebrew", "python39_osx", "pre-commit_osx", "pwsh_osx"]
elif current_platform == 'Windows':
  requirements = ["psget", "python39_windows", "pre-commit_windows"]
else:
    requirements = []

def gui_test() -> bool:
  global gui_mode
  if gui_mode == False:
    print("EIT-DevOps Cross-Platform Installer: cli mode")
  else:
    try:
      response = messagebox.askokcancel('showinfo', "EIT-DevOps Cross-Platform Installer")
      gui_mode = True
      if response == False:
        return sys.exit()
    except Exception as e:
      print("EIT-DevOps Cross-Platform Installer: cli mode")
  return gui_mode


def isAdmin() -> bool:

  try:
      is_admin = (os.getuid() == 0)
  except AttributeError:
      is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
  return is_admin

    
def display_user_message(prompt:str) -> bool:
  global gui_mode
  logger.info(f"display_user_message: {prompt}")

  try:
    response = messagebox.askokcancel('showinfo', prompt)
    if response == False:
      return sys.exit()
  except Exception as e:
    logger.info(f"display_user_message error {e}")
    print(prompt)
    
  return None


def get_user_input(prompt:str) -> bool:
  global gui_mode
  logger.info(f"get_user_input: {prompt}")

  user_input = ""
  
  try:
    response = messagebox.askyesnocancel('askquestion', prompt)
  except Exception as e:
    logger.info(f"display_user_message error {e}")
    valid_responses = ["yes", "no"]
    while user_input not in valid_responses:
        user_input = input(f"{prompt} {valid_responses}? : ")
        if user_input in ("Yes", "yes", "y", "Y"):
          response = True
        elif user_input in ("No", "no", "N", "n"):
          response = False
        else:
          response = None
  if response == None:
    return sys.exit()
  
  return response
  
    
def configure_installed() -> bool:

  logger.info(f"configure_installed tools....")

  for package_name in requires_config:
    if get_user_input(f"Open configuration info for {package_name}"):
      webbrowser.open(progs[package_name][4], new=2)
      
  return None

  
def check_install_missing(package_name:str) -> bool:
  
  logger.info(f"check_install_missing: {package_name}")
  msg = (f"\n Checking for installation of\n {package_name} ...")
    
  if distutils.spawn.find_executable(progs[package_name][1]) != None:
    display_user_message(f"{msg} \n\n  {package_name} installed")
    return True
  else:
    msg = (f"  {package_name} not installed")
    if get_user_input(f"{msg} \n install {package_name}? \n\n {progs[package_name][3]}  "):
      install_software(progs[package_name][0])
  

def install_software(package_name:str) -> bool:
    logger.info(f"install_software: {package_name}")
  
    install_command = progs[package_name][2]

    try:
      process = subprocess.run(install_command.split(), capture_output=True, text=True, check=True)
      logger.info(f"install_software: {package_name} success")
      display_user_message(f"  {package_name} installation succesful") 
    except Exception as e:
      logger.info(f"install_software: {package_name} failed")
      logger.info(f" \n\n {e} \n\n")
      display_user_message(f"  {package_name} installation failed")


def intro_message():
  
  if about == True:      
    if isAdmin() == False:
      sudo_msg = "Installing as USER \n Some installations require sudo \n"
    else:
      sudo_msg = "INSTALLING AS ROOT"
      
    msg = (
      "EIT_DevOps Developer Platform "
      "----------------------------------\n\n "
      "pre-commit tools install\n"
      " for OSX, Linux & Win64\n\n"
      f"{sudo_msg}\n\n"
      "developed by EIT DevOps\n"
      "edfenergy/eit-devops-devtools\n"
    )
    display_user_message(f"{msg}")
  else:
    logger.info(f"skip about")

  
def exit_message():
  msg = (
    "EIT_DevOps Developer Platform "
    "----------------------------------\n\n "
    "pre-commit tools install\n"
    " for OSX, Linux & Win64\n\n\n"
  )
  display_user_message(f"{msg}")
  

def installer():
  
  logger.info(f"install missing from {requirements}")
  for required in requirements:
      check_install_missing(required)
  
  logger.info(f"install python tools from {python_tools}")
  if get_user_input("Install python tools? :"):
    for tool in python_tools:
      check_install_missing(tool) 
      
  logger.info(f"install python tools from {powershell_tools}")
  if get_user_input("Install powershell tools? :"):
    for tool in powershell_tools:
      check_install_missing(tool) 
  
  logger.info(f"configure installed tools")    
  if get_user_input("Configure installed tools? :"):    
      configure_installed()


#logger.info(f"isAdmin detect UID : {os.getuid()}")
#logger.info(f"Running on Platform : {current_platform}")
#logger.info(f"GUI Mode : {gui_test()}")



def main(argv):
  global gui_mode
  gui_mode == True
  print(gui_mode)
  for i in range(1, len(sys.argv)):
    if sys.argv[i] in ("-h", "--help"):
      display_user_message("help")
      return sys.exit()
    elif sys.argv[i] in ("--cli"):
      gui_mode = False
    elif sys.argv[i] in ("-a", "--about"):
      about = True
  
  installer()
  
main(sys.argv)


      