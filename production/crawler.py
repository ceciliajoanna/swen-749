"""
Crawler to acquire data on the Web.
"""
from urllib.parse import urljoin
from utils import Library
from html.parser import HTMLParser

import urllib.request as urllib2

ROOT_URL = "http://cran.r-project.org/web/packages/available_packages_by_name.html" 

class AvailablePackagesParser(HTMLParser):
	is_parsing_table = False
	is_library_name = False
	is_library_description = False
	list_libraries = []
	current_obj = None



	def handle_starttag(self, tag, attrs):

		if tag == "table" and attrs[0][1] == "Available CRAN packages by name.":
			self.is_parsing_table = True

		# this verification ensure that the empty line rows are desconsidered
		# if tag == "tr" and len(attrs) > 0 and attrs[0][0] == "id":



		# this if just ensure that the links in the top for pagination are not considered 
		if self.is_parsing_table:
			if tag == "a" :
				self.is_library_name = True
				for attr in attrs:
					if attr[0] == "href":
						self.current_obj.url_info = urljoin(ROOT_URL,attr[1])
			elif tag == "td": 
				self.is_library_description = True
			elif tag == "tr": 
				self.current_obj = Library()


	def handle_data(self, data):
		if self.is_library_description:
			self.current_obj.short_description = data
		if self.is_library_name:
			self.current_obj.name = data


	def handle_endtag(self, tag):
		if tag == "a" :
			self.is_library_name = False
		elif tag == "td": 
			self.is_library_description = False
		elif tag == "tr": 
			self.list_libraries.append(self.current_obj)
			self.current_obj = Library()

	def get_libs(self):
		return self.list_libraries






class WebCrawler:
	
	def run(self):
		raw_response = urllib2.urlopen(ROOT_URL)
		charset = raw_response.info().get_param('charset', 'utf8')
		html_content = raw_response.read().decode(charset)
		parser = AvailablePackagesParser()
		parser.feed(html_content)
		libraries = parser.get_libs()

		
		for lib in libraries:
			print(lib)



