# parse_data.py
import xml.etree.ElementTree as ET
from datetime import datetime

from lib import slugify, parse_xml_children
from parse_currency_rates import fetch_bnb_exchange_rates

slug_cache = {}
currencies = fetch_bnb_exchange_rates()


def cached_slugify(value):
    if value in slug_cache:
        return slug_cache[value]
    slug = slugify(value)
    slug_cache[value] = slug
    return slug


def to_none_if_empty(value):
    return None if value == "" else value


def calculate_price_and_vat(price, currency):
    price_bgn = 0
    price_eur = 0

    if currency not in currencies:
        return None

    if currency == "USD":
        price_eur_no_vat = float(price) / currencies[currency]
        price_eur = price_eur_no_vat * 1.2 * 1.00312
        price_bgn = price_eur * currencies["EUR"]

    if currency == "EUR":
        price_bgn_no_vat = float(price) * currencies["EUR"]
        price_bgn = price_bgn_no_vat * 1.2
        price_eur = float(price) * 1.2

    return price_eur, price_bgn


def parse_xml_to_products(xml_data):
    root = ET.fromstring(xml_data)
    products = []

    for product in root.findall(".//product"):
        try:
            properties = [
                {"name": prop.get("name"), "value": prop.text}
                for prop in product.find("properties").findall("property")
            ]
        except AttributeError:
            properties = []

        category_element = product.find("category")
        category = to_none_if_empty(
            category_element.text if category_element is not None else None
        )

        # Determine the slug
        product_id = product.get("id")
        slug = cached_slugify(category) if category else product_id

        try:
            price = (
                product.find("price").text
                if product.find("price") is not None
                else None
            )
            currency = (
                product.find("currency").text
                if product.find("currency") is not None
                else None
            )

            price_eur, price_bgn = calculate_price_and_vat(price, currency)

            gallery = parse_xml_children(product.find("gallery"), "pictureUrl")
            properties = parse_xml_children(product.find("properties"), "property")

            product_info = {
                "id": product_id,
                "name": product.find("name").text
                    if product.find("name") is not None
                    else None,
                "product_status": product.find("product_status").text
                    if product.find("product_status") is not None
                    else None,
                "price": price,
                "price_eur": price_eur,
                "price_bgn": price_bgn,
                "currency": currency,
                "gallery": gallery,
                "manufacturer": product.find("manufacturer").text
                    if product.find("manufacturer") is not None
                    else None,
                "category": category,
                "properties": properties,
                "created_at": datetime.now(),
                "slug": slug,
            }
            products.append(product_info)
        except Exception as e:
            print(f"Error inserting product ID: {product_id} - {str(e)}")

    return products
