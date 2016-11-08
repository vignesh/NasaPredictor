import sys
import requests
import json
from datetime import datetime
from datetime import timedelta

class Nasa:

	def __init__(self, latitude, longitude):
		try:
			self.lat = int(latitude) #raw_input("Which is the latitude of the location?\n")
			self.long = int(longitude) #raw_input("What is the longitude of the location?\n")
			if ((-90 <= self.lat <= 90)and (-180 <= self.long <= 180)):
				self.success = False
				sys.exit("The location entered is invalid.")
			self.parameters = {"lon": self.long, "lat": self.lat, "api_key":"9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute"} #parameters 
			self.success = True
		except:
			self.success = False
			sys.exit("The location entered is invalid.")
 
	def getRecent(self):
		response = requests.get("https://api.nasa.gov/planetary/earth/imagery?", params = self.parameters) 
		imageryDate = json.loads(response.content)["date"] #get recent image date
		self.recent = datetime.strptime(imageryDate, "%Y-%m-%dT%H:%M:%S") #format to datetime

	def getAverage(self):
		response = requests.get("https://api.nasa.gov/planetary/earth/assets?", params = self.parameters)
		totalDates = json.loads(response.content)["count"] #get count of images
		totalResults = sorted(json.loads(response.content)["results"]) #sorted list by dates of results
		totalDays = 0 #day counter
		for i in range(0,int(totalDates)-1): #loop through all
			currentDate = totalResults[i]["date"] #get current date
			currentDate = datetime.strptime(currentDate, "%Y-%m-%dT%H:%M:%S") #formate to datetime
			nextDate = totalResults[i+1]["date"] #get next date
			nextDate = datetime.strptime(nextDate, "%Y-%m-%dT%H:%M:%S") #format to datetime
			difference = abs(nextDate-currentDate).days #find difference 
			totalDays += difference #add to total day counter
		self.average = totalDays/(int(totalDates)-1) #find average day count

	def calculateNext(self):
		self.nextPhoto = self.recent + timedelta(days=int(self.average)) #add average date to recent date 
		print "The next time (%s latitude ,%s longitude) will be shot is %s." % (self.lat, self.long, self.nextPhoto)

	def __del__(self):
		if self.success == True:
			print "Successfuly found the next time a satellite image will be taken.\n"
		else:
			print "Failed to find the next time a satellite image will be taken.\n"

def flyBy(latitude, longitude):
	Location = Nasa(latitude,longitude)
	Location.getRecent()
	Location.getAverage()
	Location.calculateNext()
	del Location

def main():
	#flyBy("a", 100)
	flyBy(90, 2)
	#flyBy(36.098592,-112.097796) #Grand Canyon
	#flyBy(43.078154,-79.075891) #Niagra Falls
	#flyBy(36.998979,-109.045183) #Four Corners Monument
	#flyBy(37.7937007,-122.4039064) #Delphix San Francisco

if __name__ == "__main__":
    main()

#del Location

#check for lat and lon range, check if number/float
#request exxcept error
#check splittling for count(triple digit case)