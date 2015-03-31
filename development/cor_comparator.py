import difflib
import os
import re
import csv

difflib.SequenceMatcher(None)

folder_name = "C:\\Users\\Joanna\\Dropbox\\Mestrado\\EUA\\Disciplinas\\2015_Spring\\SWEN-749\\Final Project\\Replicated Papers\\R releases\\"
latest_version_file = folder_name + "R3\\R-3.1.3\\src\\library\\stats\\src\\cov.c"
releases = ["R1","R2","R3"]

latest_version_file_content = open(latest_version_file).read()
print("Generating diff report")
with open("C:\\Users\\Joanna\\Dropbox\\Mestrado\\EUA\\Disciplinas\\2015_Spring\\SWEN-749\\Final Project\\Replicated Papers\\cor_diff_report.csv", "w", newline='') as csvfile:
	csv_report = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_report.writerow(['Version','Difference Ratio'])


	#Iterate over all releases folder
	for release in releases:
		release_folder_name = folder_name + release
		for subdir, dirs, files in os.walk(release_folder_name):
			for f in files:
				if f == "cov.c":
					file_content = open(os.path.join(subdir, f)).read()
					matcher = difflib.SequenceMatcher(a=latest_version_file_content, b=file_content)
					r_version = re.search('R-([0-9.a-z]*)',subdir).group(0)
					if r_version != "R-3.1.3": #ignore latest version because it is going to be equals to 1
						csv_report.writerow([r_version,str(matcher.ratio())])
					
