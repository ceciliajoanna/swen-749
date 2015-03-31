from urllib.parse import urljoin
import urllib.request as urllib2
import re
from html.entities import name2codepoint


# URLs definition
URL_LIBS_ROOT = "http://cran.r-project.org/"
URL_LIBS_LIST = urljoin(URL_LIBS_ROOT, "/web/packages/available_packages_by_name.html")
URL_LIBS_CONTRIB=  urljoin(URL_LIBS_ROOT, "/src/contrib/")
URL_LIBS_ARCHIVE = urljoin(URL_LIBS_CONTRIB, "Archive/")


import os	

def cls():
	os.system(['clear','cls'][os.name == 'nt'])



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

def extract_tar_gz(file_name,path):
	tfile = tarfile.open(file_name,'r:gz')
	tfile.extractall(path)
	tfile.close()
	print ("Tarfile Extracted")










