import time
import requests
from urls import *

class VTApi:
    def __init__(self, api_key):
        self.api_key = api_key

    def scan_url(self, url):
        params = {'apikey': self.api_key, 'url': url}
        response = requests.post(SCAN_URL, data=params, timeout=1000)
        while True:
            if response.status_code == 200:
                if response.json()['response_code'] == 1:
                    return response.json()['scan_id']
            time.sleep(18)
            response = requests.post(SCAN_URL, data=params, timeout=1000)

    def url_report(self, resource):
        params = {'apikey': self.api_key, 'resource': resource}
        response = requests.get(URL_REPORT, params=params, timeout=1000)
        while True:
            if response.status_code == 200:
                if response.json()['response_code'] == 1:
                    data = response.json()
                    verbose_data = {
                        'url': data['url'],
                        'scan_date': data['scan_date'],
                        'results': f'({data["positives"]} / {data["total"]})',
                        'positives': data['positives'],
                        'more': data['permalink']
                    }
                    return verbose_data
            time.sleep(18)
            response = requests.get(URL_REPORT, params=params, timeout=1000)

    def scan_file(self, file):
        params = {'apikey': self.api_key}
        files = {'file': ('filefrombot', file)}
        response = requests.post(FILE_SCAN, files=files, params=params, timeout=1000)
        while True:
            if response.status_code == 200:
                return response.json()['resource']
            time.sleep(18)
            response = requests.post(FILE_SCAN, files=files, params=params, timeout=1000)
    
    def file_report(self, resource):
        params = {'apikey': self.api_key, 'resource': resource}
        response = requests.get(FILE_REPORT, params=params, timeout=1000)
        while True:
            if response.status_code == 200:
                if response.json()['response_code'] == 1:
                    data = response.json()
                    verbose_data = {
                        'results': f'({data["positives"]} / {data["total"]})',
                        'positives': data['positives'],
                        'scan_date': data['scan_date'],
                        'more': data['permalink']
                    }
                    return verbose_data
            time.sleep(18)
            response = requests.get(FILE_REPORT, params=params, timeout=1000)
