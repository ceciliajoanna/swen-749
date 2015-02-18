from subprocess import call
# Check if the computer has python 3 version installed
# Check if there is an existing R language installed
# If yes Check for a possibility in which you install for both the version of R
#If there is some conflict then user has to be notified for the uninstallation and installation.
#If there is a possibility then prompt the user for the appropriate Rversion and then chack for dependencies
# If all the dependencies are met then download the source file and start executing the installation process.
#If all the dependencies are not met then download all the necessary (Assume :Ubuntu for now)
#If all the dependencies are met then intiate the installation procedure.
#Inform the user of switching the R version before using it.

#Step 1
#Check the running version of Python
import sys
import binascii
import urllib 
import os
PYTHON_HEXVERSION = 0x03000000
def CheckPython():
    if PYTHON_HEXVERSION  > sys.hexversion:
        print(sys.version)
        print("Please run this script in Python 3.0.0")
        return False
    else:
        print("Python version Test OK!")
        return True

def CheckExistingR(version):
    call(['R','--version'])

def CheckDirectory():
    #check if the download directory exists or not
    if not os.path.isdir("~/R-packages"):
        call(['mkdir','~/R-packages'])
    call(['cd','~/R-packages/'])

def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

def ParseMajorVersion(version):
    #check the major version from the string and return it
    majorversion = version[0]
    if is_number(majorversion):
        return majorversion
    else:
        return False
        

def DownloadR(version):
    m = ParseMajorVersion(version)
    

def InstallRDep():
    call(['sudo','apt-get','build-dep','r-base'])

if CheckPython():
    version = 0
    #Step 2 check if there is existing R language installed
    while(not ParseMajorVersion(version = input("Enter the version of R to be installed:"))):
        print("The version you entered is incorrect.The script will re-run and input the correct version")
    CheckExistingR(version)
    #Install all the dependencies of R
