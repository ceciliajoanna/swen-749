import urllib.request as urllib2
import re

URL = "http://cran.r-project.org/src/base/R-1/"
raw_response = urllib2.urlopen(URL)
charset = raw_response.info().get_param('charset', 'utf8')
html_content = raw_response.read().decode(charset)
pattern = '<a href="(.*)">R-(.*).tgz</a>'
r_versions = re.findall(pattern, html_content)
for r_version in r_versions:
	name = r_version[0]
	# lines commented cuz we already downloaded the files in previous execution
	urllib2.urlretrieve (URL+name,name)