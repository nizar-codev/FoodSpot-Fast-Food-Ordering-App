import sqlite3

def create_database():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            password TEXT,
            is_logged_in INTEGER DEFAULT 0
        )
    """)
     
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone TEXT,
        address TEXT,
        items TEXT,
        subtotal INTEGER,
        delivery_charge INTEGER,
        grand_total INTEGER,
        order_date TEXT,
        invoice_path TEXT
    )
""")

    conn.commit()
    conn.close()

def add_invoice_column():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE orders
            ADD COLUMN invoice_path TEXT
        """)
        print("invoice_path column added.")
    except sqlite3.OperationalError:
        print("invoice_path column already exists.")

    conn.commit()
    conn.close()


def save_user(name, phone, email, password):
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    # Check if a user already exists
    cursor.execute("SELECT id FROM users LIMIT 1")
    existing_user = cursor.fetchone()

    if existing_user:
        # Update existing user
        cursor.execute("""
            UPDATE users
            SET
                name = ?,
                phone = ?,
                email = ?,
                password = ?,
                is_logged_in = ?
            WHERE id = ?
        """, (name, phone, email, password, 1, existing_user[0]))

    else:
        # Insert first user
        cursor.execute("""
            INSERT INTO users
            (name, phone, email, password, is_logged_in)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, email, password, 1))

    conn.commit()
    conn.close()

def save_order(customer_name, phone, address, items,
               subtotal, delivery_charge, grand_total, order_date, invoice_path):

    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders
        (customer_name, phone, address, items,
         subtotal, delivery_charge, grand_total, order_date, invoice_path)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
    """, (
        customer_name,
        phone,
        address,
        items,
        subtotal,
        delivery_charge,
        grand_total,
        order_date,
        invoice_path
    ))

    conn.commit()
    conn.close()

def get_user():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")

    user = cursor.fetchone()

    conn.close()

    return user


def get_logged_in_user():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE is_logged_in = 1 LIMIT 1")

    user = cursor.fetchone()

    conn.close()

    return user

def show_users():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


def logout_user():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET is_logged_in = 0
    """)

    conn.commit()
    conn.close()
    delete_all_orders()

    print("User logged out.")


def show_orders():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


def get_orders():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_name,
               phone,
               address,
               items,
               grand_total,
               order_date,
               invoice_path
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return orders

def delete_all_orders():
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders")

    conn.commit()
    conn.close()


import os
import sqlite3

def delete_order(invoice_path):
    conn = sqlite3.connect("foodspot.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM orders WHERE invoice_path = ?",
        (invoice_path,)
    )

    conn.commit()
    conn.close()