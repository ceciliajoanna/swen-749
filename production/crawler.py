# -*- coding: utf-8 -*-

"""
Crawler to acquire data on the Web.
"""

#External Imports
import html 
import re
from urllib.parse import urljoin
import urllib.request as urllib2
import html.entities as htmlentitydefs
from html.parser import HTMLParser
from html.entities import name2codepoint
# Local Imports
from utils import URL_LIBS_LIST
from utils import Library
from db_manager import LibraryManager


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

		# this "if" just ensure that the links in the top for pagination are not considered 
		if self.is_parsing_table and not self.is_parsing_empty_row:
			if tag == "a" :
				self.is_library_name = True
				for attr in attrs:
					if attr[0] == "href":
						self.current_obj.url_info = urljoin(URL_LIBS_LIST,attr[1])
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
			self.last_key = data.replace("\n","").replace(":","").lowercase()
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
		
		print("WebCrawler >> Getting information about Available Packages... ")
		raw_response = urllib2.urlopen(URL_LIBS_LIST)
		charset = raw_response.info().get_param('charset', 'utf8')
		html_content = raw_response.read().decode(charset)
		parser = AvailablePackagesParser()
		parser.feed(html_content)
		libraries = parser.get_libs()
		
		print("WebCrawler >> Available Packages found. Saving packages... ")
		#save the libraries
		library_manager = LibraryManager()
		library_manager.clear()
		library_manager.save(libraries)


		print("WebCrawler >> Success! Available Packages saved. Retrieving packages versions... ")
		
		# for lib in libraries:
		# 	print(lib)
			# raw_response = urllib2.urlopen(lib.url_info)
			# charset = raw_response.info().get_param('charset', 'utf8')
			# html_content = raw_response.read().decode(charset)
			# parser = PackageDetailParser()
			# parser.feed(html_content)

			# latest_library_info = parser.get_lib_info()
			# # older_library_infos = 
			



