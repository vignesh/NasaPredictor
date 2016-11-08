import requests
import json
from datetime import datetime
from datetime import timedelta

class Nasa:

	def __init__(self):
		self.lat = raw_input("Which is the latitude of the location?\n")
		self.long = raw_input("What is the longitude of the location?\n")
		self.parameters = {"lon": self.long, "lat": self.lat, "api_key":"9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute"}
 
	def getRecent(self):
		response = requests.get("https://api.nasa.gov/planetary/earth/imagery?", params = self.parameters)
		imageryDate = json.loads(response.content)["date"]
		#imageryDate = response.content.split()[1] #get date from response
		#self.recent = imageryDate[imageryDate.find('"')+1:imageryDate.find(',')-1] #between quotes
		self.recent = datetime.strptime(imageryDate, "%Y-%m-%dT%H:%M:%S")
		#print self.recent
		#print "-----------------------BREAK"

	def getAverage(self):
		response = requests.get("https://api.nasa.gov/planetary/earth/assets?", params = self.parameters)
		totalDates = json.loads(response.content)["count"]
		totalResults = sorted(json.loads(response.content)["results"])
		#print totalResults[0]["date"]
		#assetDate = response.content.split("{")[1]
		#totalDates = assetDate[assetDate.find(":")+2:assetDate.find(",")] 
		totalDays = 0
		#print response.content
		for i in range(0,int(totalDates)-1):
			count +=1
			currentDate = totalResults[i]["date"]
			#assetDate = response.content.split("{")[i] #current date
			#currentDate = assetDate[assetDate.find(":")+3:assetDate.find(",")-1] 
			currentDate = datetime.strptime(currentDate, "%Y-%m-%dT%H:%M:%S")
			#assetDate = response.content.split("{")[i+1] #next date
			#nextDate = assetDate[assetDate.find(":")+3:assetDate.find(",")-1] 
			nextDate = totalResults[i+1]["date"]
			nextDate = datetime.strptime(nextDate, "%Y-%m-%dT%H:%M:%S")
			difference = abs(nextDate-currentDate).days #find difference 
			totalDays += difference
		self.average = totalDays/(int(totalDates)-1)
		print self.average

	def flyby(self):
		self.nextPhoto = self.recent + timedelta(days=int(self.average))
		print "The next time %s latitude %s longitude will be shot is %s." % (self.lat, self.long, self.nextPhoto)



	#def __del__(self):
	#	print self.lat
	#	print self.long


Location = Nasa()
Location.getRecent()
Location.getAverage()
Location.flyby()

#del Location

#check for lat and lon range, check if number/float
#request exxcept error
#check splittling for count(triple digit case)