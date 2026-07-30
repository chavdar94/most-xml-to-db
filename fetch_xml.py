# fetch_xml.py
import requests


def fetch_xml_data(url, method):
    if method == 'GET':
        response = requests.get(url)
    else:
        response = requests.post(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.content
