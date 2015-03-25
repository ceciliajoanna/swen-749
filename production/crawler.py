# -*- coding: utf-8 -*-

"""
Crawler to acquire data on the Web.
"""
from urllib.parse import urljoin
from utils import Library
import html 
from html.parser import HTMLParser
import re
import urllib.request as urllib2
import html.entities as htmlentitydefs
from html.entities import name2codepoint



ROOT_URL = "http://cran.r-project.org/web/packages/available_packages_by_name.html" 

class AvailablePackagesParser(HTMLParser):
	is_parsing_table = False
	is_parsing_empty_row = False
	is_library_name = False
	is_library_description = False
	list_libraries = []
	current_obj = None



	def handle_starttag(self, tag, attrs):

		if tag == "table" and attrs[0][1] == "Available CRAN packages by name.":
			self.is_parsing_table = True

		# this verification ensure that the empty line rows are desconsidered
		if tag == "tr" and len(attrs) > 0 and attrs[0][0] == "id":
			self.is_parsing_empty_row = True

		# this if just ensure that the links in the top for pagination are not considered 
		if self.is_parsing_table and not self.is_parsing_empty_row:
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
			if self.is_parsing_empty_row:
				self.is_parsing_empty_row = False
			else:
				self.list_libraries.append(self.current_obj)
				self.current_obj = Library()

	def get_libs(self):
		return self.list_libraries



class PackageDetailParser(HTMLParser):
	STATE_INITIAL = 0
	STATE_TABLE = 1
	STATE_ROW = 2
	STATE_KEY = 3
	STATE_VALUE = 4
	STATE_FINISHED = 5
	current_state = STATE_INITIAL
	last_key = None
	lib_info = dict()

	
	def handle_starttag(self, tag, attrs):
		if self.current_state == self.STATE_INITIAL:
			if tag == "table" and re.match("Package .* summary",attrs[0][1]):
				self.current_state = self.STATE_TABLE
		elif self.current_state ==self.STATE_TABLE:
			if tag == "tr":
				self.current_state = self.STATE_ROW
		elif self.current_state == self.STATE_ROW:
			if tag == "td":
				self.current_state = self.STATE_KEY
		
	def handle_data(self, data):
		if self.current_state == self.STATE_KEY:
			self.last_key = data.replace("\n","")
			self.lib_info[self.last_key] = ""
		elif self.current_state == self.STATE_VALUE:
			self.lib_info[self.last_key] += data.replace("\n","")

	def handle_entityref(self,name):
		self.lib_info[self.last_key] += str(name2codepoint[name])
		


	def handle_endtag(self, tag):
		if tag == "table" :
			self.current_state = self.STATE_FINISHED
		elif self.current_state == self.STATE_KEY:
			if tag == "td":
				self.current_state = self.STATE_VALUE
		elif self.current_state == self.STATE_VALUE:
			if tag == "td":
				self.current_state = self.STATE_ROW




	def get_lib_info(self):
		return self.lib_info


class WebCrawler:
	
	def run(self):

		raw_response = urllib2.urlopen("http://cran.r-project.org/web/packages/A3/index.html")
		charset = raw_response.info().get_param('charset', 'utf-8')
		html_content = raw_response.read().decode('ASCII')
		# print(html_content)
		parser = PackageDetailParser()
		parser.feed(html_content)
		
		# print(parser.get_lib_info())


		# raw_response = urllib2.urlopen(ROOT_URL)
		# charset = raw_response.info().get_param('charset', 'utf8')
		# html_content = raw_response.read().decode(charset)
		# parser = AvailablePackagesParser()
		# parser.feed(html_content)
		# libraries = parser.get_libs()

		
		# for lib in libraries:
		# 	print(lib)
		# 	raw_response = urllib2.urlopen(ROOT_URL)
		# 	charset = raw_response.info().get_param('charset', 'utf8')
		# 	html_content = raw_response.read().decode(charset)
		# 	parser = PackageDetailParser()
		# 	parser.feed(html_content)

			
			# print(parser.get_lib_info())



