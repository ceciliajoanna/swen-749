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
import urllib.request 
import os
import subprocess
import pdb
import re
from os.path import expanduser
from utils import extract_gz_file,extract_tar_gz

PYTHON_HEXVERSION = 0x03000000
DOWNLOAD_URL = 'http://cran.us.r-project.org/src/base/'
def CheckPython():
    if PYTHON_HEXVERSION  > sys.hexversion:
        print(sys.version)
        print("Please run this script in Python 3.0.0")
        return False
    else:
        print("Python version Test OK!")
        return True

def tail():
    command = ["R","--version"] # your bash script execute command goes here
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in iter(popen.stdout.readline,b'' ):
        yield line,
    popen.communicate()


def CheckExistingR(version):
    details = next(tail())
    print ("Output:")
    match = re.search('(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)',str(details))
    if match:
        release = match.group(1)
        majorv = match.group(2)
        minorv = match.group(3)
        if version[0] == str(release):
            if version[2] == str(majorv):
                if version[4] == str(minorv):
                    print("You have the same version.You don't need to install it.")
                    return False
        return True
    else:
        print("Some problem in parsing the version of R from the system")


def CheckDirectory(version):
    #check if the download directory exists or not
    home = expanduser("~")
    if not os.path.isdir(home +"/R-packages"):
        call(['mkdir',home +'/R-packages'])
    return home + '/R-packages/R-'+version[0]+'-'+version[2]+'-'+version[4],home + '/R-packages/R-'+version[0]+'-'+version[2]+'-'+version[4]+'.tar.gz'
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
       return True
    else:
        return False
        

def DownloadR(URL,version):
    directory,newFile = CheckDirectory(version)
    print(URL)
    response = urllib.request.urlretrieve(URL,newFile)
    return directory,newFile
    
def BuildFinalUrl(version):
    return  DOWNLOAD_URL + "R-"+str(version[0]) + '/R-' + version[0] + '.' + version[2] + '.' + version[4] + ".tar.gz"
def InstallRDep():
    call(['sudo','apt-get','install','build-essential','f2c','gfortran','libblas-dev','liblapack-dev','g++'])

def InstallR(filename,directory,version):
    InstallRDep()
    extract_tar_gz(filename,directory)
    print(os.getcwd())
    os.chdir(directory+'/R-'+version+'/')
    call(['./configure'])
    call(['make'])
    call(['make','check'])
    if os.path.isfile(directory+'/R-'+version+'/bin/R'):
        MakeSymLink(directory+'/R-'+version+'/',version)
    else:
        print('Binaries did not compile succefffully! Contact the administrator')
    #call(['make','install'])

def MakeSymLink(path,version):
    call(['sudo','ln','-s',path+'bin/R','/usr/bin/R-'+version])
    print("R is installed")

def FindSymLink(version):
    if os.path.exists('/usr/bin/R-'+version):
        print("The version is already installed")
        return True
    print('No exsting symlinks found')
    return False

if CheckPython():
    version = str(0)
    #Step 2 check if there is existing R language installed
    #while(version = input("Enter the version of R to be installed:")):
    #    print("The version you entered is incorrect.The script will re-run and input the correct version")
    version = input("Enter the version of R to be installed:")
    
    if CheckExistingR(version):
        if not FindSymLink(version):
            ParseMajorVersion(version)
            URL = BuildFinalUrl(version)
            directory,newFile = DownloadR(URL,version)
            InstallR(newFile,directory,version)
