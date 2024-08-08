# db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Products" (
        id TEXT PRIMARY KEY,
        name TEXT NULL,
        product_status TEXT NULL,
        haspromo INTEGER NULL,
        price REAL NULL,
        price_with_vat REAL NULL,
        price_without_vat REAL NULL,
        currency TEXT NULL, 
        main_picture_url TEXT NULL,
        manufacturer TEXT NULL,
        category TEXT NULL,
        subcategory TEXT NULL,
        partnum TEXT NULL,
        vendor_url TEXT NULL,
        properties JSON NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        slug TEXT NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def insert_products(products):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO "Products" (
        id, name, product_status, haspromo, 
        price, price_with_vat, price_without_vat, currency, main_picture_url, manufacturer, 
        category, subcategory, partnum, vendor_url, properties, created_at, slug
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (id) DO NOTHING
    '''

    for product in products:
        # properties_json = json.dumps(product.get('properties')) if product.get('properties') else None
        values = (
            product.get('id'),
            product.get('name'),
            product.get('product_status'),
            product.get('haspromo'),
            product.get('price'),
            product.get('price_with_vat'),
            product.get('price_without_vat'),
            product.get('currency'),
            product.get('main_picture_url'),
            product.get('manufacturer'),
            product.get('category'),
            product.get('subcategory'),
            product.get('partnum'),
            product.get('vendor_url'),
            product.get('properties'),
            product.get('created_at'),
            product.get('slug')
        )

        try:
            cursor.execute(insert_query, values)
        except Exception as e:
            conn.rollback()
            print(f"Error inserting product ID: {product.get('id')} - {e}")

    conn.commit()
    cursor.close()
    conn.close()
