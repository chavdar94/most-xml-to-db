# db.py
import json
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    return psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Products" (
        id TEXT PRIMARY KEY,
        name TEXT NULL,
        product_status TEXT NULL,
        price REAL NULL,
        price_eur REAL NULL,
        price_bgn REAL NULL,
        currency TEXT NULL, 
        gallery TEXT[] NULL,
        manufacturer TEXT NULL,
        category TEXT NULL,
        properties TEXT[] NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        slug TEXT NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def insert_products(products):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO "Products" (
        id, name, product_status,  
        price, price_eur, price_bgn, currency, gallery, manufacturer, 
        category, properties, created_at, slug
    ) 
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) 
    ON CONFLICT (id) DO NOTHING
    """

    for product in products:
        # properties_json = json.dumps(product.get('properties')) if product.get('properties') else None
        values = (
            product.get("id"),
            product.get("name"),
            product.get("product_status"),
            product.get("price"),
            product.get("price_eur"),
            product.get("price_bgn"),
            product.get("currency"),
            product.get("gallery"),
            product.get("manufacturer"),
            product.get("category"),
            product.get("properties"),
            product.get("created_at"),
            product.get("slug"),
        )

        try:
            cursor.execute(insert_query, values)
        except Exception as e:
            conn.rollback()
            print(f"Error inserting product ID: {product.get('id')} - {e}")

    conn.commit()
    cursor.close()
    conn.close()
