# main.py
import time
import logging
from fetch_xml import fetch_xml_data
from parse_data import parse_xml_to_products
from db import create_tables, insert_products

# Configure logging
logging.basicConfig(
    filename='/path/to/your/app.log',  # Path to your log file
    level=logging.INFO,  # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    url = "http://most.traveldatabank.biz/ProductXML"

    start_time = time.time()

    try:
        # Fetch XML data
        logging.info("Starting to fetch XML data from %s", url)
        xml_data = fetch_xml_data(url)
        logging.info("XML data fetched successfully")

        # Parse XML data to products
        logging.info("Parsing XML data")
        products = parse_xml_to_products(xml_data)
        logging.info("XML data parsed successfully")

        # Create database tables
        logging.info("Creating database tables")
        create_tables()
        logging.info("Database tables created successfully")

        # Insert products into the database
        logging.info("Inserting products into the database")
        insert_products(products)
        logging.info("Products inserted successfully")

        end_time = time.time()
        total_time = end_time - start_time
        logging.info("Total execution time: %.2f seconds", total_time)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))


if __name__ == "__main__":
    main()



