import xml.etree.ElementTree as ET
from fetch_xml import fetch_xml_data


# Dictionary to hold currency exchange rates


def fetch_bnb_exchange_rates():
    currencies = {
        "USD": None,
        "EUR": 1.95583,
        "BGN": 1.0
    }

    url = "https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?download=xml"
    xml_data = fetch_xml_data(url)

    root = ET.fromstring(xml_data)
    rows = root.findall(".//ROW")[1:]  # Skip the header row if necessary

    for row in rows:
        currency_code = row.find('CODE').text
        if currency_code in currencies:
            rate_value = float(row.find('RATE').text)
            currencies[currency_code] = rate_value

    return currencies
