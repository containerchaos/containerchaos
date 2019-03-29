import csv
import datetime

import matplotlib.pyplot as plt
import pandas as pd
import requests


def measure_response_time(url, criteria):
    '''
    Measures and saves an API request's response time to a CSV file

    :param url: The URL for API request
    :param criteria: The criteria in effect
    :return: Path to a CSV file with response time in seconds with its timestamp as columns
    '''

    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    date_time = datetime.datetime.now()
    fieldnames = ['timestamp', 'responseTime', 'criteria']  # Headers of the CSV file
    out_path = 'Response-Times.csv'

    with open(out_path, 'a') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if csvFile.tell() == 0:
            writer.writeheader()
        writer.writerow({'timestamp': date_time, 'responseTime': response_time, 'criteria': criteria})

    csvFile.close()
    return out_path


def generate_graph(path):
    '''
    Saves a histogram with average response time per number of requests

    :param path: Path to a csv file
    '''
    response_times = pd.read_csv(path)

    criteria_dict = response_times.groupby("criteria")["responseTime"].apply(list).to_dict()
    critera_keys = list(criteria_dict.keys())
    criteria_values = list(criteria_dict.values())

    plt.style.use("seaborn-deep")
    plt.hist(x=criteria_values, bins=30, label=critera_keys)
    plt.legend(loc="upper right")
    plt.xlabel("Response Time in Seconds")
    plt.ylabel("Number of Requests")
    plt.savefig("responseTimes-figure")
    plt.show()


for i in range(100):
    path_to_csv = measure_response_time('https://jsonmock.hackerrank.com/api/countries/', "Criteria A")
    path_to_csv = measure_response_time('https://jsonmock.hackerrank.com/api/countries/', "Criteria B")
    path_to_csv = measure_response_time('https://jsonmock.hackerrank.com/api/countries/', "Criteria C")

generate_graph("Response-Times.csv")
