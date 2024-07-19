# main.py
import time
from fetch_xml import fetch_xml_data
from parse_data import parse_xml_to_products
from db import create_tables, insert_products


def main():
    url = "http://most.traveldatabank.biz/ProductXML"

    start_time = time.time()

    # Fetch XML data
    xml_data = fetch_xml_data(url)

    # Parse XML data to products
    products = parse_xml_to_products(xml_data)

    # Create database tables
    create_tables()

    # Insert products into the database
    insert_products(products)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
