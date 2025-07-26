import csv
import mysql.connector
from connection import mycursor, mydb
import os
from datetime import datetime

def parse_timestamp(timestamp_str):
    if not timestamp_str:
        return None
    try:
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def load_distribution_centers():
    print("Loading distribution_centers.csv...")
    with open('./data/distribution_centers.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO distribution_centers 
                     (id, name, latitude, longitude) 
                     VALUES (%s, %s, %s, %s)"""
            val = (
                int(row['id']),
                row['name'],
                float(row['latitude']),
                float(row['longitude'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} distribution centers")

def load_products():
    print("Loading products.csv...")
    with open('./data/products.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO products 
                     (id, cost, category, name, brand, retail_price, 
                      department, sku, distribution_center_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                int(row['id']),
                float(row['cost']),
                row['category'],
                row['name'],
                row['brand'],
                float(row['retail_price']),
                row['department'],
                row['sku'],
                int(row['distribution_center_id'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} products")

def load_users():
    print("Loading users.csv...")
    with open('./data/users.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO users 
                     (id, first_name, last_name, email, age, gender, 
                      state, street_address, postal_code, city, country, 
                      latitude, longitude, traffic_source, created_at) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                int(row['id']),
                row['first_name'],
                row['last_name'],
                row['email'],
                int(row['age']) if row['age'] else None,
                row['gender'],
                row['state'],
                row['street_address'],
                row['postal_code'],
                row['city'],
                row['country'],
                float(row['latitude']) if row['latitude'] else None,
                float(row['longitude']) if row['longitude'] else None,
                row['traffic_source'],
                parse_timestamp(row['created_at'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} users")

def load_orders():
    print("Loading orders.csv...")
    with open('./data/orders.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO orders 
                     (order_id, user_id, status, gender, created_at, 
                      returned_at, shipped_at, delivered_at, num_of_item) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                int(row['order_id']),
                int(row['user_id']),
                row['status'],
                row['gender'],
                parse_timestamp(row['created_at']),
                parse_timestamp(row['returned_at']),
                parse_timestamp(row['shipped_at']),
                parse_timestamp(row['delivered_at']),
                int(row['num_of_item'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} orders")

def load_inventory_items():
    print("Loading inventory_items.csv...")
    with open('./data/inventory_items.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO inventory_items 
                     (id, product_id, created_at, sold_at, cost, 
                      product_category, product_name, product_brand, 
                      product_retail_price, product_department, 
                      product_sku, product_distribution_center_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                int(row['id']),
                int(row['product_id']),
                parse_timestamp(row['created_at']),
                parse_timestamp(row['sold_at']),
                float(row['cost']),
                row['product_category'],
                row['product_name'],
                row['product_brand'],
                float(row['product_retail_price']),
                row['product_department'],
                row['product_sku'],
                int(row['product_distribution_center_id'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} inventory items")

def load_order_items():
    print("Loading order_items.csv...")
    with open('./data/order_items.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = """INSERT INTO order_items 
                     (id, order_id, user_id, product_id, inventory_item_id, 
                      status, created_at, shipped_at, delivered_at, returned_at) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                int(row['id']),
                int(row['order_id']),
                int(row['user_id']),
                int(row['product_id']),
                int(row['inventory_item_id']),
                row['status'],
                parse_timestamp(row['created_at']),
                parse_timestamp(row['shipped_at']),
                parse_timestamp(row['delivered_at']),
                parse_timestamp(row['returned_at'])
            )
            mycursor.execute(sql, val)
    mydb.commit()
    print(f"Loaded {mycursor.rowcount} order items")

def main():
    try:
        # Load tables in proper order to maintain referential integrity
        # load_distribution_centers()
        # load_products()
        load_users()
        load_orders()
        load_inventory_items()
        load_order_items()
        
        print("All data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        mydb.rollback()
    finally:
        mycursor.close()
        mydb.close()

if __name__ == "__main__":
    main()