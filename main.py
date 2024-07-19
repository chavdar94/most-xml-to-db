import requests
import xml.etree.ElementTree as ET
import psycopg2
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

st = time.time()

# Getting the XML
url = "http://most.traveldatabank.biz/ProductXML"
response = requests.get(url)
xml_data = response.content

root = ET.fromstring(xml_data)


def to_none_if_empty(value):
    return None if value == '' else value


# Parsing the XML to Dict objects
products = []
for product in root.findall('.//product'):
    properties = [
        {
            'name': prop.get('name'),
            'value': prop.text
        } for prop in product.find('properties').findall('property')
    ]

    product_info = {
        'id': int(product.get('id')),
        'uid': to_none_if_empty(product.get('uid')),
        'code': product.find('code').text if product.find('code') is not None else None,
        'name': product.find('name').text if product.find('name') is not None else None,
        'searchstring': product.find('searchstring').text if product.find('searchstring') is not None else None,
        'product_status': product.find('product_status').text if product.find('product_status') is not None else None,
        'haspromo': to_none_if_empty(product.find('haspromo').text if product.find('haspromo') is not None else None),
        'general_description': product.find('general_description').text if product.find(
            'general_description') is not None else None,
        'classname': product.find('classname').text if product.find('classname') is not None else None,
        'classname_full': product.find('classname_full').text if product.find('classname_full') is not None else None,
        'class_id': to_none_if_empty(product.find('class_id').text if product.find('class_id') is not None else None),
        'price': to_none_if_empty(product.find('price').text if product.find('price') is not None else None),
        'currency': product.find('currency').text if product.find('currency') is not None else None,
        'main_picture_url': product.find('main_picture_url').text if product.find(
            'main_picture_url') is not None else None,
        'manufacturer': product.find('manufacturer').text if product.find('manufacturer') is not None else None,
        'category': to_none_if_empty(product.find('category').text if product.find('category') is not None else None),
        'subcategory': to_none_if_empty(
            product.find('subcategory').text if product.find('subcategory') is not None else None),
        'partnum': product.find('partnum').text if product.find('partnum') is not None else None,
        'vendor_url': product.find('vendor_url').text if product.find('vendor_url') is not None else None,
        'properties': json.dumps(properties)
    }
    products.append(product_info)

dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    uid INTEGER,
    code TEXT,
    name TEXT,
    searchstring TEXT,
    product_status TEXT,
    haspromo INTEGER,
    general_description TEXT,
    classname TEXT,
    classname_full TEXT,
    class_id INTEGER,
    price REAL,
    currency TEXT,
    main_picture_url TEXT,
    manufacturer TEXT,
    category TEXT,
    subcategory TEXT,
    partnum TEXT,
    vendor_url TEXT,
    properties JSONB
)
''')

# Insert product data into the database
insert_query = '''
INSERT INTO products (
    id, uid, code, name, searchstring, product_status, haspromo, general_description, 
    classname, classname_full, class_id, price, currency, main_picture_url, manufacturer, 
    category, subcategory, partnum, vendor_url, properties
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
) ON CONFLICT (id) DO NOTHING
'''

# Iterate over products and insert them
for product in products:
    # Convert properties to JSONB format if it's not None
    properties_json = json.dumps(product.get('properties')) if product.get('properties') else None

    values = (
        product.get('id'),
        product.get('uid'),
        product.get('code'),
        product.get('name'),
        product.get('searchstring'),
        product.get('product_status'),
        product.get('haspromo'),
        product.get('general_description'),
        product.get('classname'),
        product.get('classname_full'),
        product.get('class_id'),
        product.get('price'),
        product.get('currency'),
        product.get('main_picture_url'),
        product.get('manufacturer'),
        product.get('category'),
        product.get('subcategory'),
        product.get('partnum'),
        product.get('vendor_url'),
        properties_json
    )

    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        # Rollback transaction on error and log the issue
        conn.rollback()
        print(f"Error inserting product ID: {product.get('id')} - {e}")

# Commit the transaction and close the database connection
try:
    conn.commit()
except Exception as e:
    print(f"Error committing transaction: {e}")

conn.close()

et = time.time()
total = et - st
print(total)
