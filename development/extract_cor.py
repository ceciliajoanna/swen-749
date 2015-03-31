import urllib.request as urllib2
import gzip
import tarfile
import os
folder_name = "C:\\Users\\Joanna\\Dropbox\\Mestrado\\EUA\\Disciplinas\\2015_Spring\\SWEN-749\\Final Project\\Replicated Papers\\R releases\\R1"

for subdir, dirs, files in os.walk(folder_name):
	for f in files:
		tgz_file = os.path.join(subdir, f)
		tar = tarfile.open(tgz_file, 'r')
		for item in tar:

			if item.name.endswith("cov.c"):
				tar.extract(item, folder_name)
				# library/stats/src/
				print( item.name )