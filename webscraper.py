from bs4 import BeautifulSoup
from html.parser import HTMLParser
import requests
import os
import csv
import socket
import sys
from geolite2 import geolite2
from goose3 import Goose
import time

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

try:
	os.remove("output.txt")
except:
	pass

europe = ["United Kingdom","Scotland","Hungary","Germany","Belgium","European Union","Switzerland","Norway","Netherlands","France","Ireland","Estonia","Finland","Malta","Sweden","Italy","Slovakia","Republic of Moldova","Spain","Luxembourg","Austria","Spain"]
asia = ["India","Thailand","Singapore","Nepal","Republic of Korea","Taiwan","China","Japan","Macao","Qatar","Malaysia","Pakistan","Bangladesh"]
north_america = ["United States","Canada"]
africa = ["South Africa","Rwanda","Tanzania","Algeria"]
oceana = ["New Zealand","Australia"]
south_america = ["Colombia"]
na = ["N/A"]

completedLines = []

domainDict = {"ae":"United Arab Emirates",
"ar":"Argentina",
"al":"Albania",
"au":"Australia",
"bb":"Barbados",
"bd":"Bangladesh",
"be":"Belgium",
"br":"Brazil",
"ca":"Canada",
"ch":"Switzerland",
"cn":"China",
"co":"Colombia",
"cu":"Cuba",
"es":"Spain",
"cz":"Czech Republic",
"de":"Germany",
"dk":"Denmark",
"dm":"Dominica",
"dz":"Algeria",
"fr":"France",
"hk":"Hong Kong",
"hr":"Croatia",
"id":"Indonesia",
"il":"Israel",
"in":"India",
"it":"Italy",
"kr":"Republic of Korea",
"lk":"Sri Lanka",
"mo":"Macao",
"mx":"Mexico",
"no":"Norway",
"pe":"Peru",
"pt":"Portugal",
"qa":"Qatar",
"ru":"Russia",
"sa":"Saudi Arabia",
"se":"Sweden",
"sg":"Singapore",
"sk":"Slovakia",
"th":"Thailand",
"tr":"Turkey",
"tt":"Trinidad and Tobago",
"ua":"Ukraine",
"tw":"Taiwan",
"uk":"United Kingdom",
"pk":"Pakistan",
"my":"Malaysia",
"eu":"European Union",
"nz":"New Zealand",
"tz":"Tanzania",
"fi":"Finland",
"mt":"Malta",
"rw":"Rwanda",
"nl":"Netherlands",
"za":"South Africa",
"tv":"Tuvalu",
"hu":"Hungary",
"scot":"Scotland"}

file = "output.csv"
with open('links.txt', 'r+') as filehandle:
	i = 0
	isPersistent = True
	errorCount = 0

	#Create model input files
	if (isPersistent == False):
		with open('model/input/input_master.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_europe.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_asia.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_northamerica.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_africa.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_oceana.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_southamerica.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])

		with open('model/input/input_other.csv', 'a') as file:
			write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			write_file.writerow(["id", "title", "text", "continent", "time"])


	for line in filehandle:
		splitArray = line.split(",")
		linkVal = splitArray[0]
		timeVal = splitArray[1][:-1]

		print ("Scanning... ", i)
		
		try:
			#deal with URL (4 types)
			countryLabel = "N/A"
			tempArray = line.split("https://www",1)
			if (len(tempArray) > 1):
				pass
			else:
				tempArray = line.split("http://www",1)
				if (len(tempArray) > 1):
					pass
				else:
					tempArray = line.split("https://",1)
					if (len(tempArray) > 1):
						pass
					else:
						tempArray = line.split("http://",1)
						if (len(tempArray) > 1):
							pass
						else:
							pass
			processedWord = tempArray[1].lstrip('.')
			processedWord = processedWord.split("/",1)[0]
			domainExt = processedWord.split(".",1)[1]
			try:
				domainExt = domainExt.split(".",1)[1]
				print ("*Domain extention has multiple (.), splitting to determine location origin*")
			except:
				pass

			if domainExt in domainDict.keys():
				countryLabel = domainDict[domainExt]
			else:
				#IP Lookup
				try:
					ipAddress = socket.gethostbyname(processedWord)
					reader = geolite2.reader()
					match = reader.get(ipAddress)
					countryLabel = match['country']['names']['en']
					#print (match['country']['names']['en'])
					#print("=========")
				except:
					print("*IP not found! Domain of extention: " + domainExt +" was not identifiable*")
					pass

			tempVal = countryLabel.replace('\'', '').replace('{', '').replace('}', '')

			if tempVal in europe:
				contientVal = "Europe"
			elif tempVal in asia:
				contientVal = "Asia"
			elif tempVal in north_america:
				contientVal = "North America"
			elif tempVal in africa:
				contientVal = "Africa"
			elif tempVal in oceana:
				contientVal = "Oceana"
			elif tempVal in south_america:
				contientVal = "South America"
			else:
				contientVal = "N/A"

			#load and scrape site
			#r  = requests.get(linkVal)
			#data = r.text

			#soup = BeautifulSoup(data)
			#articleText = ""

			#for x in soup.find_all('p'):
			#	articleText = articleText + strip_tags(str(x))

			g = Goose()
			article = g.extract(url=linkVal)
			articleText = article.cleaned_text
			articleTitle = article.title

			

			if (articleText != "" and articleText != " " and linkVal.lower().find(".pdf") == -1):
				completedLines.append(line)
				errorCount = 0
				with open('model/input/input_master.csv', 'a') as file:
					write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])

				if (contientVal == "Europe"):
					with open('model/input/input_europe.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Asia"):
					with open('model/input/input_asia.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "North America"):
					with open('model/input/input_northamerica.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Africa"):
					with open('model/input/input_africa.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Oceana"):
					with open('model/input/input_oceana.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "South America"):
					with open('model/input/input_southamerica.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				else:		
					with open('model/input/input_other.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
		
		except KeyboardInterrupt:
			print ("KeyboardInterrupt")
			print("Last line completed: " + completedLines[-1])
			try:
				sys.exit(0)
			except SystemExit:
				os._exit(0)
		except Exception as e:
			print (e)
			errorCount = errorCount + 1
			print("======================")
			print("Last line completed =" + completedLines[-1])
			print("======================")
			if (errorCount > 2):
				time.sleep(60)
			pass
		i = i + 1

