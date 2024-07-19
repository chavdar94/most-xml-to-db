# fetch_xml.py
import requests


def fetch_xml_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.content
