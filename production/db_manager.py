
# MySQL connector from Oracle: 
# http://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
# http://stackoverflow.com/a/622308
# http://stackoverflow.com/a/25724855
# https://pypi.python.org/pypi/mysql-connector-python/2.0.3

import mysql.connector


DB_CONFIG = {
	'user': 'root',
	'password': '',
	'host': '127.0.0.1',
	'database': 'swen749',
	'raise_on_warnings': True,
}



class Library:
	name = ""
	short_description = ""
	long_description = None
	url_info = ""
	versions = []

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


	def to_dict(self):
		return {
			"name":self.name,
			"short_description":self.short_description,
			"long_description":self.long_description,
			"url_info":self.url_info
		}


class RVersion:
	version_number = ""
	release_date = ""

	def __str__(self):
		return str(self.version_number)



class LibraryVersion:
	version_number = None
	release_date  = None
	min_r_version = None
	max_r_version = None
	depends = None
	suggests = None
	needs_compilation = None

	def __str__(self):
		return str(self.version_number)

	def to_dict(self):
		return {
			"version_number":self.version_number,
			"release_date":self.release_date,
			"min_r_version":self.min_r_version,
			"max_r_version":self.max_r_version,
			"depends":self.depends,
			"suggests":self.suggests,
			"needs_compilation":self.needs_compilation,
		}







class LibraryManager:

	def clear(self):
		cnx = mysql.connector.connect(**DB_CONFIG)
		cursor = cnx.cursor()
		cursor.execute("TRUNCATE TABLE library")
		cursor.close()
		cnx.close()

	def save(self,libraries):
		cnx = mysql.connector.connect(**DB_CONFIG)
		cursor = cnx.cursor()

		for lib in libraries:
			sql_insert = "INSERT INTO library(name, short_description, long_description, url_info) VALUES( %(name)s, %(short_description)s, %(long_description)s, %(url_info)s)"
			params = lib.to_dict()
			cursor.execute(sql_insert,params)

			#insert the package's versions
			for version in lib.versions:
				sql_insert = "INSERT INTO library(name, short_description, long_description, url_info) VALUES( %(name)s, %(short_description)s, %(long_description)s, %(url_info)s)"
				params = version.to_dict()
				cursor.execute(sql_insert,params)

		cnx.commit()
		cursor.close()
		cnx.close()
