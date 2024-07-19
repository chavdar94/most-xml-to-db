# parse_data.py
import xml.etree.ElementTree as ET
import json


def to_none_if_empty(value):
    return None if value == '' else value


def parse_xml_to_products(xml_data):
    root = ET.fromstring(xml_data)
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
            'product_status': product.find('product_status').text if product.find(
                'product_status') is not None else None,
            'haspromo': to_none_if_empty(
                product.find('haspromo').text if product.find('haspromo') is not None else None),
            'general_description': product.find('general_description').text if product.find(
                'general_description') is not None else None,
            'classname': product.find('classname').text if product.find('classname') is not None else None,
            'classname_full': product.find('classname_full').text if product.find(
                'classname_full') is not None else None,
            'class_id': to_none_if_empty(
                product.find('class_id').text if product.find('class_id') is not None else None),
            'price': to_none_if_empty(product.find('price').text if product.find('price') is not None else None),
            'currency': product.find('currency').text if product.find('currency') is not None else None,
            'main_picture_url': product.find('main_picture_url').text if product.find(
                'main_picture_url') is not None else None,
            'manufacturer': product.find('manufacturer').text if product.find('manufacturer') is not None else None,
            'category': to_none_if_empty(
                product.find('category').text if product.find('category') is not None else None),
            'subcategory': to_none_if_empty(
                product.find('subcategory').text if product.find('subcategory') is not None else None),
            'partnum': product.find('partnum').text if product.find('partnum') is not None else None,
            'vendor_url': product.find('vendor_url').text if product.find('vendor_url') is not None else None,
            'properties': json.dumps(properties)
        }
        products.append(product_info)

    return products
