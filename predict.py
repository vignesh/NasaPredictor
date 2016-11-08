import requests
import json
from datetime import datetime
from datetime import timedelta

class Nasa:

	def __init__(self, latitude, longitude): #constructor
		try:
			self.lat = float(latitude) #check if latitude is numeric
			self.long = float(longitude) #check if longitude is numeric
			if ((-90 <= self.lat <= 90) and (-180 <= self.long <= 180)): #range check for latitude/longitude
				self.parameters = {"lon": self.long, "lat": self.lat, "api_key":"9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute"} #parameters 
				self.success = True #success boolean
			else:
				self.success = False #Location entered is invalid.
		except:
			self.success = False  #Location entered is invalid.
 
	def getRecent(self):
		try:
			response = requests.get("https://api.nasa.gov/planetary/earth/imagery?", params = self.parameters) 
			imageryDate = json.loads(response.content)["date"] #get recent image date
			self.recent = datetime.strptime(imageryDate, "%Y-%m-%dT%H:%M:%S") #format to datetime
		except: #catches if error occurs when retreiving imagery data
			self.success = False #No imagery data found for location.

	def getAverage(self):
		try:
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
		except: #catches if error occurs when retreiving asset data
			self.success = False #No asset data found for location.

	def calculateNext(self):
		self.nextPhoto = self.recent + timedelta(days=int(self.average)) #add average date to recent date git 
		print "The next time (%s latitude ,%s longitude) will be shot is %s." % (self.lat, self.long, self.nextPhoto)

	def __del__(self): #destructor
		if self.success == True:
			print "Successfuly found when the next satellite image will be taken.\n"
		else:
			print "Failed to find when the next time a satellite image will be taken.\n"

def flyBy(latitude, longitude): 
	try:
		Location = Nasa(latitude,longitude)
		Location.getRecent()
		Location.getAverage()
		Location.calculateNext()
		del Location
	except:
		return ("Failed to find when the next time a satellite image will be taken") #catches any unaccounted errors

def main():
	flyBy(36.098592,-112.097796) #Grand Canyon
	flyBy(43.078154,-79.075891) #Niagra Falls
	flyBy(36.998979,-109.045183) #Four Corners Monument
	flyBy(37.7937007,-122.4039064) #Delphix San Francisco
	flyBy(-100,20) #latitude out of range
	flyBy("lat",22) #string entered as parameter
	flyBy(89, 2) #no image data present

if __name__ == "__main__":
    main()
