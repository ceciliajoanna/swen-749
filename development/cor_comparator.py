import difflib
import os
import re
import csv
from itertools import tee


folder_name = "C:\\Users\\Joanna\\Dropbox\\Mestrado\\EUA\\Disciplinas\\2015_Spring\\SWEN-749\\Final Project\\Replicated Papers\\R releases\\"
releases = ["R1","R2","R3"]
csv_report_file_path = "C:\\Users\\Joanna\\Dropbox\\Mestrado\\EUA\\Disciplinas\\2015_Spring\\SWEN-749\\Final Project\\Replicated Papers\\cor_diff_report.csv"



def pairwise(iterable):
	"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = tee(iterable)
	next(b, None)
	return zip(a, b)

#Iterate over all releases folder and create a list of files
versions_list = []
for release in releases:
	release_folder_name = folder_name + release
	for subdir, dirs, files in os.walk(release_folder_name):
		for f in files:
			if f == "cov.c":
				versions_list.append(os.path.join(subdir, f))


	
print("Generating diff report")
with open(csv_report_file_path, "w", newline='') as csvfile:
	csv_report = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_report.writerow(['Version A','Version B','Difference Ratio'])
	for version_a,version_b in pairwise(versions_list):
		file_content_a = open(version_a).read()
		file_content_b = open(version_b).read()
		matcher = difflib.SequenceMatcher(a=file_content_a, b=file_content_b)
		r_version_a = re.search('R-([0-9.a-z]*)',version_a).group(0)
		r_version_b = re.search('R-([0-9.a-z]*)',version_b).group(0)
		csv_report.writerow([r_version_a,r_version_b,str(1 - matcher.ratio())])
		print("diff {0} {1} | diffstat -s >> 'cor_diff.txt'".format(version_a,version_b))
print("Finished report generation")


