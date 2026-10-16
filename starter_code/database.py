"""
database.py
------------
Task 3: Build a relational database from your cleaned data.
"""

import sqlite3


def get_connection(db_path: str = "store.db") -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id   TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category     TEXT,
            unit_price   REAL,
            in_stock     TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id        TEXT PRIMARY KEY,
            product_id     TEXT,
            quantity       INTEGER,
            sale_date      TEXT,
            payment_method TEXT,
            customer_type  TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    conn.commit()


def insert_products(conn: sqlite3.Connection, products_df) -> None:
    # Clear existing data to avoid duplicates on re-run
    conn.execute("DELETE FROM products")
    products_df.to_sql("products", conn, if_exists="append", index=False)
    conn.commit()


def insert_sales(conn: sqlite3.Connection, sales_df) -> None:
    conn.execute("DELETE FROM sales")
    sales_df.to_sql("sales", conn, if_exists="append", index=False)
    conn.commit()


def query_total_revenue_per_product(conn: sqlite3.Connection):
    """Return each product's name and total revenue (quantity * unit_price), highest first."""
    sql = """
        SELECT p.product_name,
               ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_best_selling_product(conn: sqlite3.Connection):
    """Return the single product with the highest total quantity sold."""
    sql = """
        SELECT p.product_name, SUM(s.quantity) AS total_units
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_units DESC
        LIMIT 1
    """
    return conn.execute(sql).fetchall()


def query_sales_by_payment_method(conn: sqlite3.Connection):
    """Return the number of sales transactions per payment method."""
    sql = """
        SELECT payment_method, COUNT(*) AS transaction_count
        FROM sales
        GROUP BY payment_method
        ORDER BY transaction_count DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_one(conn: sqlite3.Connection):
    """Which product category earns the most total revenue?"""
    sql = """
        SELECT p.category,
               ROUND(SUM(s.quantity * p.unit_price), 2) AS category_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY category_revenue DESC
    """
    return conn.execute(sql).fetchall()


def query_custom_two(conn: sqlite3.Connection):
    """How many sales were made each month, and what was the total revenue per month?"""
    sql = """
        SELECT SUBSTR(s.sale_date, 1, 7) AS month,
               COUNT(*) AS num_sales,
               ROUND(SUM(s.quantity * p.unit_price), 2) AS monthly_revenue
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY month
        ORDER BY month
    """
    return conn.execute(sql).fetchall()
