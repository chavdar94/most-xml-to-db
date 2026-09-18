# main.py
import logging
import time
from pathlib import Path

from db import create_tables, insert_products
from fetch_xml import fetch_xml_data
from parse_data import parse_xml_to_products

BASE_DIR = Path(__file__).resolve().parent
LOGGER_FILE = BASE_DIR / "logger.log"

# Configure logging

logging.basicConfig(
    filename=LOGGER_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    url = "https://portal.mostbg.com/api/product/xml/all?currency=EUR"

    start_time = time.time()

    try:
        # Fetch XML data
        logging.info("Starting to fetch XML data from %s", url)
        xml_data = fetch_xml_data(url, method="POST")
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
