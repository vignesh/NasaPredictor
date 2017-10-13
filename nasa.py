import sys
import requests
import json
from datetime import datetime
from datetime import timedelta

def invalidLatitude(latitude):
	"""
	Check if latitude is invalid.
	Argument:
		latitude: input from flyBy function
	Return value:
		boolean: check if latitude is invalid
	"""
	try:
		latitude = float(latitude)
	except ValueError:
		return True

	if (-90 <= latitude <= 90):
		return False
	else:
		return True

def invalidLongitude(longitude):
	"""
	Argument:
		longitude: input from flyBy function
	Return value:
		boolean: check if longitude is invalid
	"""
	try:
		longitude = float(longitude)
	except ValueError:
		return True

	if (-180<= longitude <= 180):
		return False
	else:
		return True

def flyBy(latitude, longitude):
	"""
	Argument:
		latitude: input from main function
		longitude: input from main function
	Action:
		call getNasaData(latitude, longitude, key)
	"""
	key = "9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute"
	
	if invalidLatitude(latitude):
		print "Invalid latitude entered"
	elif invalidLongitude(longitude):
		print "Invalid longitude entered"
	else:
		getNasaData(latitude, longitude, key)

def getNasaData(latitude, longitude, key):
	"""
	Argument:
		latitude: float input from flyBy()
		longitude: float input from flyBy()
		key: string API key
	Action:
		call calculateNextDate(totalDates, sortedDates)
	"""
	parameters = {"lat": latitude,"lon": longitude, "api_key":key}
	endpoint =  "https://api.nasa.gov/planetary/earth/assets?"
	try:
		response = requests.get(endpoint, params = parameters) 
		totalDates = json.loads(response.content)["count"]
		sortedDates = sorted(json.loads(response.content)["results"])
	except Exception as e:
		print "Error occured when fetching data from Nasa"

	if totalDates > 0:
		calculateNextDate(totalDates, sortedDates)
	else:
		print "No Nasa data for given coordinates"

def calculateNextDate(totalDates, sortedDates):
	"""
	Argument:
		totalDates: integer of total dates from API response
		sortedDates: list of sorted date objects from API response
	Action:
		print calculated next date
	"""
	recentDate = formatDate(sortedDates[totalDates-1])
	totalDayDifference = 0
	for date in range(0,int(totalDates)-1):
		currentDate = formatDate(sortedDates[date])
		nextDate = formatDate(sortedDates[date+1])
		totalDayDifference += dateDifference(currentDate, nextDate)
	averageDayDifference = totalDayDifference/totalDates
	nextDate = recentDate + timedelta(days=averageDayDifference)
	print "Next time: " + str(nextDate)

def formatDate(dateObject):
	"""
	Argument:
		dateObject: object with date and id fields
	Return:
		date: datetime formatted date
	"""
	date = dateObject["date"]
	date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
	return date

def dateDifference(currentDate, nextDate):
	"""
	Argument:
		currentDate: datetime of current date
		nextDate: datetime of next date
	Return:
		integer day difference between currentDate and nextDate
	"""
	return abs((nextDate - currentDate).days)

def main():
	"""
	Run test cases
	"""
	flyBy(36.098592,-112.097796) #Grand Canyon
	flyBy(43.078154,-79.075891) #Niagra Falls
	flyBy(36.998979,-109.045183) #Four Corners Monument
	flyBy(37.7937007,-122.4039064) #Delphix San Francisco
	flyBy("invalidInput",22) #latitude not a number
	flyBy(-70,200) #longitude out of range
	flyBy(89, 1) #no image data present

if __name__ == "__main__":
    main()