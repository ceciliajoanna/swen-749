from urllib.parse import urljoin
import urllib.request as urllib2
import re


# URLs definition
URL_LIBS_ROOT = "http://cran.r-project.org/"
URL_LIBS_LIST = urljoin(URL_LIBS_ROOT, "/web/packages/available_packages_by_name.html")
URL_LIBS_CONTRIB=  urljoin(URL_LIBS_ROOT, "/src/contrib/")
URL_LIBS_ARCHIVE = urljoin(URL_LIBS_CONTRIB, "Archive/")



class Library:
	name = ""
	short_description = ""
	long_description = None
	url_info = ""
	versions = []

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


	def to_dict(self):
		return {
			"name":self.name,
			"short_description":self.short_description,
			"long_description":self.long_description,
			"url_info":self.url_info
		}


class RVersion:
	version_number = ""
	release_date = ""

	def __str__(self):
		return str(self.version_number)



class LibraryVersion:
	version_number = ""
	release_date  = ""
	min_r_version = ""
	max_r_version = ""
	depends = ""
	suggests = ""
	needs_compilation = ""

	def __str__(self):
		return str(self.version_number)






