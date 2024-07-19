# db.py
import psycopg2
import os
import json
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
    conn.commit()
    cursor.close()
    conn.close()


def insert_products(products):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO products (
        id, uid, code, name, searchstring, product_status, haspromo, general_description, 
        classname, classname_full, class_id, price, currency, main_picture_url, manufacturer, 
        category, subcategory, partnum, vendor_url, properties
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (id) DO NOTHING
    '''

    for product in products:
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
            conn.rollback()
            print(f"Error inserting product ID: {product.get('id')} - {e}")

    conn.commit()
    cursor.close()
    conn.close()
