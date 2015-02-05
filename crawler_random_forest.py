import urllib.request as urllib2
import re
import gzip
import tarfile

def open_url(url):
	raw_response = urllib2.urlopen(url)
	charset = raw_response.info().get_param('charset', 'utf8')
	html_content = raw_response.read().decode(charset)
	pattern = '<a href="(.*)">randomForest_(.*).tar.gz</a>'
	return re.findall(pattern, html_content)


def extract_R_info(file_name):
	zip_file = gzip.open(file_name, 'rb')
	file_content = zip_file.read()
	zip_file.close()

	uncompressed_file = open(file_name.replace(".gz",""),"wb")
	uncompressed_file.write(file_content)
	uncompressed_file.close()
	#print(file_content)


def parse_tar_file(tar_file,report):
	tar = tarfile.open(tar_file)
	# search for the DESCRIPTION file
	for member in tar.getmembers():
		if member.isfile() and member.name.endswith("DESCRIPTION"):
			description_file = tar.extractfile(member)
			content = description_file.read()
			depends = re.findall("Depends: (.*)",content.decode("utf8"))[0].replace(",","").replace("\r","").replace("\n","")
			version = re.findall("Version: (.*)",content.decode("utf8"))[0].replace("\r","").replace("\n","")

			report.write(str.encode(version))
			report.write(b",")
			report.write(str.encode(depends))
			report.write(b"\r\n")
	tar.close()
	


URL = "http://cran.r-project.org/src/contrib/Archive/randomForest/"
randomForestVersions = open_url(URL)
report = open("report_randomForest.csv","wb")
report.write(b"Version,Depends\r\n")	
for version in randomForestVersions:
	#download lib
	name = version[0]
	# lines commented cuz we already downloaded the files in previous execution
	#urllib2.urlretrieve (URL+name,name)
	#extract_R_info(name)
	
	parse_tar_file(name.replace(".gz",""),report)

report.close()

