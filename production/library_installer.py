
# -*- coding: utf-8 -*-


import subprocess
import re
import gzip
import tarfile
import sys
from urllib.parse import urljoin
import urllib.request as urllib2
from utils import find_pattern, exists
from utils import find_library_url



class LibraryInstaller:
	
	def install(self, library, library_version, r_version = "R"):
		library_url = find_library_url(library_name,library_version):
		file_name = library_url.rsplit('/',1)[1]
		urllib2.urlretrieve (library_url, file_name)
		command = [r_version, "CMD", "INSTALL", file_name]





arguments = sys.argv

if len(arguments) == 3:
	library_name = arguments[1]
	library_version = arguments[2]
	library_url = find_library_url(library_name,library_version)
	if not library_url:
		print("ERROR: library {0} version {1} not found!".format(library_name,library_version))
	else:
		installer = LibraryInstaller()
		installer.install(library_name, library_version)
else:
	print("Usage: >> Library_Name Library_Version R_Version")

