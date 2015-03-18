import sys
import urllib.request as urllib2
import re
import gzip
import tarfile
from urllib.parse import urljoin
from utils import find_pattern, exists
import subprocess

URL_LIBS_ROOT = "http://cran.r-project.org/"
URL_LIBS_WEB = urljoin(URL_LIBS_ROOT, "/web/packages/available_packages_by_name.html")
URL_LIBS_CONTRIB=  urljoin(URL_LIBS_ROOT, "/src/contrib/")
URL_LIBS_ARCHIVE = urljoin(URL_LIBS_CONTRIB, "Archive/")

def find_library_url(library_name,version):
	""" Find the library URL given its name and version. None is returned if the library could not be found """ 
	url_archive = urljoin(URL_LIBS_ARCHIVE, '{0}/{1}_{2}.tar.gz'.format(library_name, library_name,version) )
	url_contrib = urljoin(URL_LIBS_CONTRIB, '{0}_{1}.tar.gz'.format(library_name,version) )
	
	if exists(url_archive):
		return url_archive
	elif exists(url_contrib):
		return url_contrib
	else:
		return None


def install(library_url):
	# packageurl <- "http://http://cran.r-project.org/src/contrib/Archive/randomForest/randomForest_1.0.tar.gz"
	# install.packages(packageurl, repos=NULL, type="source")
	# command = ('packageurl <- {0}\n'.format(library_url))
	# command = command + 'install.packages(packageurl, repos=NULL, type="source")'
	file_name = library_url.rsplit('/',1)[1]
	urllib2.urlretrieve (library_url, file_name)
	command = ["R", "CMD", "INSTALL", file_name]
	# stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE
	p = subprocess.Popen(command)
	# out , err = p.communicate()
	# for i in  iter(p.stdout.readline, b''):
	#	print(i)
	# out, err = p.communicate(command)
	# print (out )
	
	



arguments = sys.argv

if len(arguments) == 3:
	library_name = arguments[1]
	version = arguments[2]
	library_url = find_library_url(library_name,version)
	if not library_url:
		print("ERROR: library {0} version {1} not found!".format(library_name,version))
	else:
		install(library_url)
else:
	print("Usage: >> install_library.py  libraryName version")

