import urllib.request as urllib2
import re

def find_pattern(url, pattern):
	"""" This function returns all the patterns found in a Web page """ 
	raw_response = urllib2.urlopen(url)
	charset = raw_response.info().get_param('charset', 'utf8')
	html_content = raw_response.read().decode(charset)
	return re.findall(pattern, html_content)


def exists(url):
	""" Returns true if the Web page exists (i.e. HTTP code response is 2xx) """

	if not url: 
		return False
	try:
		urllib2.urlopen(url)
		return True
	except urllib2.HTTPError as e:
		return e.code < 300 and e.code >= 200

	return False

def extract_gz_file(file_name):
	""" Given the filename of a gzip file, it extracts it"""
	zip_file = gzip.open(file_name, 'rb')
	file_content = zip_file.read()
	zip_file.close()

	uncompressed_file = open(file_name.replace(".gz",""),"wb")
	uncompressed_file.write(file_content)
	uncompressed_file.close()
	