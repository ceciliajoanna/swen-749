import gzip
import tarfile

def open_url(url, pattern):
	"""" This function returns all the patterns found in a Web page """ 
	raw_response = urllib2.urlopen(url)
	charset = raw_response.info().get_param('charset', 'utf8')
	html_content = raw_response.read().decode(charset)
	return re.findall(pattern, html_content)




def extract_gz_file(file_name):
	""" Given the filename of a gzip file, it extracts it"""
	zip_file = gzip.open(file_name, 'rb')
	file_content = zip_file.read()
	zip_file.close()

	uncompressed_file = open(file_name.replace(".gz",""),"wb")
	uncompressed_file.write(file_content)
	uncompressed_file.close()
	
def extract_tar_gz(file_name):
    tfile = tarfile.open(file_name,'r:gz')
    tfile.extractall()
    tfile.close()
    print ("Tarfile Extracted")
