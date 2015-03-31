
# -*- coding: utf-8 -*-

import urllib.request as urllib2
import re
import gzip
import tarfile
from urllib.parse import urljoin
from utils import find_pattern, exists
import subprocess


class LibraryInstaller:
	
	def install(self):
		file_name = library_url.rsplit('/',1)[1]
		urllib2.urlretrieve (library_url, file_name)
		command = ["R", "CMD", "INSTALL", file_name]
