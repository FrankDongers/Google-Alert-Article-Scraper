from bs4 import BeautifulSoup
from html.parser import HTMLParser
import requests
import os
import csv
import socket
import sys
from geolite2 import geolite2
from goose3 import Goose

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

europe = ["United Kingdom","Scotland","Hungary","Germany","Belgium","European Union","Switzerland","Norway","Netherlands","France","Ireland","Estonia","Finland","Malta","Sweden","Italy","Slovakia","Republic of Moldova","Spain","Luxembourg","Austria"]
asia = ["India","Thailand","Singapore","Nepal","Republic of Korea","Taiwan","China","Japan","Macao","Qatar","Malaysia","Pakistan","Bangladesh"]
north_america = ["United States","Canada"]
africa = ["South Africa","Rwanda","Tanzania"]
oceana = ["New Zealand","Australia"]
south_america = ["Colombia"]
na = ["N/A"]

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
"cz":"Czech Republic",
"de":"Germany",
"dk":"Denmark",
"dm":"Dominica",	
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
	euroCounter = 1
	northCounter = 1
	asiaCounter = 1
	africaCounter = 1
	oceanaCounter = 1
	southCounter = 1
	naCounter = 1
	for line in filehandle:
		splitArray = line.split(",")
		linkVal = splitArray[0]
		timeVal = splitArray[1][:-1]

		print ("Scanning... ", i)
		
		try:
			#deal with URL
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
					#print("Not Found**")
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
				if (contientVal == "Europe"):
					if (euroCounter == 0):
						with open('input_europe.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							euroCounter = euroCounter + 1
					with open('input_europe.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Asia"):
					if (asiaCounter == 0):
						with open('input_asia.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							asiaCounter = asiaCounter + 1
					with open('input_asia.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "North America"):
					if (northCounter == 0):
						with open('input_northamerica.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							northCounter = northCounter + 1
					with open('input_northamerica.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Africa"):
					if (africaCounter == 0):
						with open('input_africa.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							africaCounter = africaCounter + 1
					with open('input_africa.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "Oceana"):
					if (oceanaCounter == 0):
						with open('input_oceana.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							oceanaCounter = oceanaCounter + 1
					with open('input_oceana.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				elif(contientVal == "South America"):
					if (southCounter == 0):
						with open('input_southamerica.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							southCounter = southCounter + 1
					with open('input_southamerica.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])
				else:
					if (naCounter == 0):
						with open('input.csv', 'a') as file:
							write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							write_file.writerow(["id", "title", "text", "continent", "time"])
							naCounter = naCounter + 1
					with open('input.csv', 'a') as file:
						write_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						write_file.writerow([str(i+1), articleTitle, articleText, countryLabel, timeVal])

		except:
			print("timeout")
			pass
		i = i + 1

