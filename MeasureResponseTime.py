import csv
import datetime

import requests


def measure_response_time(url):
    '''
    Measures and saves an API request's response time to a CSV file

    :param url: The URL for API request
    :return: Path to a CSV file with response time in seconds with its timestamp as columns
    '''

    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    date_time = datetime.datetime.now()
    fieldnames = ['timestamp', 'responseTime']  # Headers of the CSV file
    out_path = 'Response-Times.csv'

    with open(out_path, 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if csvFile.tell() == 0:
            writer.writeheader()
        writer.writerow({'timestamp': date_time, 'responseTime': response_time})

    csvFile.close()
    return out_path


path_to_csv = measure_response_time('https://jsonmock.hackerrank.com/api/countries/')
