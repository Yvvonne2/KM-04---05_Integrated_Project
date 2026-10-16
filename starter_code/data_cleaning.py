"""
data_cleaning.py
-----------------
Task 2: Load the raw CSV files and clean them.
"""

import pandas as pd


def load_raw_data(products_path: str, sales_path: str):
    products_df = pd.read_csv(products_path)
    sales_df = pd.read_csv(sales_path)
    return (products_df, sales_df)


def clean_products(products_df: "pd.DataFrame") -> "pd.DataFrame":
    df = products_df.copy()

    # Data types expected after cleaning:
    #   product_id   : str  (TEXT primary key)
    #   product_name : str  (NOT NULL)
    #   category     : str  (Title Case)
    #   unit_price   : float
    #   in_stock     : str  ("True" / "False")

    # Remove exact duplicate rows (e.g. P003 appears twice)
    df = df.drop_duplicates()

    # Drop rows with missing product_name — a product with no name is unusable
    df = df.dropna(subset=["product_name"])

    # Drop rows with missing unit_price — we cannot calculate revenue without a price
    df = df.dropna(subset=["unit_price"])

    # Standardise category to Title Case (e.g. "beverages" -> "Beverages")
    df["category"] = df["category"].str.title()

    df = df.reset_index(drop=True)
    return df


def clean_sales(sales_df: "pd.DataFrame", valid_product_ids) -> "pd.DataFrame":
    df = sales_df.copy()

    # Remove exact duplicate rows (e.g. S0011 appears twice)
    df = df.drop_duplicates()

    # Remove rows whose product_id is not in the cleaned products table
    df = df[df["product_id"].isin(valid_product_ids)]

    # Parse sale_date from multiple formats into a single datetime, then to YYYY-MM-DD string.
    # South African convention: DD-MM-YYYY / DD/MM/YYYY for ambiguous day-first formats.
    # Formats present in the data:
    #   YYYY-MM-DD  (ISO, unambiguous)
    #   YYYY/MM/DD  (ISO with slashes, unambiguous)
    #   DD/MM/YYYY  (day-first with slashes)
    #   DD-MM-YYYY  (day-first with dashes)
    # Each format is tried in order; first successful parse wins.
    def parse_date(val):
        if pd.isna(val):
            return pd.NaT
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return pd.to_datetime(val, format=fmt)
            except (ValueError, TypeError):
                continue
        return pd.NaT

    df["sale_date"] = df["sale_date"].apply(parse_date)

    # Drop rows where sale_date could not be parsed or was missing
    df = df.dropna(subset=["sale_date"])

    # Convert to standard string format YYYY-MM-DD
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")

    # Drop rows with missing quantity — we cannot calculate revenue without it
    df = df.dropna(subset=["quantity"])
    df["quantity"] = df["quantity"].astype(int)

    # Fill missing payment_method with "Unknown" — honest, does not guess a specific method
    df["payment_method"] = df["payment_method"].fillna("Unknown")

    # Fill missing customer_type with "Unknown"
    df["customer_type"] = df["customer_type"].fillna("Unknown")

    df = df.reset_index(drop=True)
    return df


def cleaning_summary(raw_df: "pd.DataFrame", clean_df: "pd.DataFrame", name: str) -> str:
    raw_count = len(raw_df)
    clean_count = len(clean_df)
    removed = raw_count - clean_count
    return f"{name}: {raw_count} raw rows -> {clean_count} clean rows ({removed} removed)"
