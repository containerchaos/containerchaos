import requests
import csv
import datetime

"""
Python Script to measure a GET request's response time
Saves the response time in seconds with its timestamp to a CSV file (creates a new CSV file if none exists)
"""

response = requests.get('https://jsonmock.hackerrank.com/api/countries/')# Dummy URL used for testing, To be replaced

responseTime = response.elapsed.total_seconds()
dateTime = datetime.datetime.now()

fieldnames=['timestamp', 'responseTime'] #Headers of the CSV file
row = [dateTime, responseTime]

with open('responseTimes.csv', 'a') as csvFile:

  writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
  
  if csvFile.tell() == 0:
      writer.writeheader()
	  
  writer.writerow({'timestamp':dateTime, 'responseTime':responseTime})
  
csvFile.close()