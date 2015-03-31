# -*- coding: utf-8 -*-



# External Imports
from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib.parse import urljoin
import urllib.request as urllib2

import re

# Local Imports
from db_manager import Library, LibraryVersion, LibraryManager
from utils import cls, URL_LIBS_LIST





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
	STATE_INITIAL = -1
	STATE_LONG_DESCRIPTION = 0
	STATE_TABLE = 1
	STATE_ROW = 2
	STATE_KEY = 3
	STATE_VALUE = 4
	STATE_FINISHED = 5
	current_state = STATE_INITIAL
	last_key = None
	lib_info = dict()

	
	def handle_starttag(self, tag, attrs):
		if self.current_state == self.STATE_INITIAL and tag == "p": 
				self.current_state = self.STATE_LONG_DESCRIPTION
		elif self.current_state ==self.STATE_TABLE and tag == "tr":
				self.current_state = self.STATE_ROW
		elif self.current_state == self.STATE_ROW and tag == "td":
				self.current_state = self.STATE_KEY
		
	def handle_data(self, data):
		if self.current_state == self.STATE_LONG_DESCRIPTION:
			self.last_key = "long_description"
			self.lib_info[self.last_key] = data
		elif self.current_state == self.STATE_KEY:
			self.last_key = data.replace("\n","").replace(":","").lower()
			self.lib_info[self.last_key] = ""
		elif self.current_state == self.STATE_VALUE:
			self.lib_info[self.last_key] += data.replace("\n","")


	def handle_entityref(self,name):
		if self.last_key != None and self.current_state in [ self.STATE_LONG_DESCRIPTION , self.STATE_VALUE ] :
			self.lib_info[self.last_key] += str(name2codepoint[name])
		


	def handle_endtag(self, tag):
		if tag == "p" :
			self.current_state = self.STATE_TABLE
		elif tag == "table" :
			self.current_state = self.STATE_FINISHED
		elif self.current_state == self.STATE_KEY and tag == "td":
				self.current_state = self.STATE_VALUE
		elif self.current_state == self.STATE_VALUE and tag == "td":
				self.current_state = self.STATE_ROW

	def get_lib_info(self):
		return self.lib_info


class WebCrawler:
	"""
	Crawler to acquire data on the Web.
	"""
	def run(self):
		
		print("WebCrawler >> Getting information about Available Packages... ")
		raw_response = urllib2.urlopen(URL_LIBS_LIST)
		charset = raw_response.info().get_param('charset', 'utf8')
		html_content = raw_response.read().decode(charset)
		parser = AvailablePackagesParser()
		parser.feed(html_content)
		libraries = parser.get_libs()
		

		print("WebCrawler >> Retrieving package versions information... ")
		count = 0
		
		for lib in libraries:
			# Get info for the latest version 
			raw_response = urllib2.urlopen(lib.url_info)
			charset = raw_response.info().get_param('charset', 'utf8')
			html_content = raw_response.read().decode(charset)
			parser = PackageDetailParser()
			parser.feed(html_content)
			latest_version_info = parser.get_lib_info()
			# The latest package version info also contains the  long_description of the librari
			lib.long_description = latest_version_info.get("long_description",None)

			latest_version = LibraryVersion()
			latest_version.version_number = latest_version_info.get("version",None)
			latest_version.release_date = latest_version_info.get("published",None)
			latest_version.depends = latest_version_info.get("depends",None)
			latest_version.suggests = latest_version_info.get("suggests",None)
			latest_version.needs_compilation = latest_version_info.get("needscompilation",None)
			
			count = count + 1
			cls()
			print("WebCrawler >> Retrieving package versions information... ")
			print(str(count) +" out of " + str(len(libraries)))




			# Retrieves older versions
			# lib.versions.append(latest_version)
			# older_version_infos = 
		

		print("WebCrawler >> Saving data collected... ")
		#save the libraries
		library_manager = LibraryManager()
		library_manager.clear()
		library_manager.save(libraries)

		# save the versions


		print("WebCrawler >> Success! Data saved. I am done for today :D ")


