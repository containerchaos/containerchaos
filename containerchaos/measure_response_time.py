import csv
import datetime

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns


def measure_response_time(url, criteria, write=True):
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

    if write:
        with open(out_path, 'a') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if csvFile.tell() == 0:
                writer.writeheader()
            writer.writerow({'timestamp': date_time, 'responseTime': response_time, 'criteria': criteria})

        csvFile.close()
    return out_path


def generate_histogram(path, title):
    '''
    Saves a histogram with average response time per number of requests

    :param path: Path to a csv file
    '''
    response_times = pd.read_csv(path)

    criteria_dict = response_times.groupby("criteria")["responseTime"].apply(list).to_dict()
    critera_keys = list(criteria_dict.keys())
    criteria_values = list(criteria_dict.values())

    plt.title(title)
    plt.style.use("seaborn-deep")
    plt.hist(x=criteria_values, bins=30, label=critera_keys)
    plt.legend(loc="upper right")
    plt.xlabel("Response Time in Seconds")
    plt.ylabel("Number of Requests")
    plt.savefig(title + " Histogram")
    plt.show()


def generate_density_plot(path, title):
    '''
    Saves a density plot with density of requests per second

    :param path: Path to a csv file
    '''
    response_times = pd.read_csv(path)

    criteria_dict = response_times.groupby("criteria")["responseTime"].apply(list).to_dict()
    critera_keys = list(criteria_dict.keys())
    # criteria_values = list(criteria_dict.values())

    for criteria in critera_keys:
        subset = response_times[response_times["criteria"] == criteria]

        sns.distplot(subset["responseTime"], hist=False, kde=True, kde_kws={"linewidth": 3}, label=criteria)

    plt.title(title)
    plt.legend(loc="upper right")
    plt.xlabel("Response Time in Seconds")
    plt.ylabel("Density")
    plt.savefig(title + " Density Plot")
    plt.show()


local_simple_csv = "output/local/simple/Response-Times.csv"
local_complex_csv = "output/local/complex/Response-Times.csv"

cloud_simple_csv = "output/gcloud/simple/Response-Times.csv"
cloud_complex_csv = "output/gcloud/complex/Response-Times.csv"

generate_histogram(local_simple_csv, "Local Machine Simple Task")
generate_density_plot(local_complex_csv, "Local Machine Complex Task")

generate_density_plot(cloud_simple_csv, "Cloud Simple Task")
generate_histogram(cloud_complex_csv, "Cloud Complex Task")
