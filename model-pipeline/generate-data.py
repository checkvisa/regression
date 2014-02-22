#!/usr/bin/python

import urllib2
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

majorDict = {}
with open('./mdict', 'r') as major:
	for line in major:
		key, value = line.strip().split(' ==> ')
		majorDict[key] = value

utc = datetime.utcnow()
if int(str(utc).split()[1].split(":")[0])>=16:
	dispdate = str(utc - timedelta(days=9999)).split()[0]
else:
	dispdate = str(utc - timedelta(days=10000)).split()[0]
url = "http://www.checkee.info/main.php?dispdate="+dispdate
print url

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
checkoo = []

for tr in soup.find_all('tr'):
	check = []
	for td in tr.find_all('td'):
		check.append(td.string)
	# skip unwanted tables
	if len(check)!=11: continue
	if check[0]=='BeiJing': continue
	if check[6]=='Status': continue
	# skip waiting days larger than 1000 days
	if int(check[9])>1000: continue
	# skip 2013 data
	# if check[7][:4]=='2013':continue
	try:
		major = majorDict[check[5].lower()]
		# print major
	except:
		major = "N/A"

  	# print checko
  	checko = [check[1].encode('utf-8'), check[2], check[3], check[4], major, check[6], 
  	check[7].split('-')[0], check[7].split('-')[1], check[7].split('-')[2],
  	check[8].split('-')[0], check[8].split('-')[1], check[8].split('-')[2],
  	check[9]]
  	print checko
  	checkoo.append(checko)
# print checkoo

with open('dat.tsv', 'wb') as tsvfile:
	writer = csv.writer(tsvfile, delimiter='\t')
	writer.writerows(checkoo)

