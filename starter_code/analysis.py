"""
analysis.py
------------
Task 4: Programming logic — functions, loops, conditionals and arrays.
"""


def total_sales_records(sales_rows: list) -> int:
    """Count the total number of sales records using a loop."""
    count = 0
    for row in sales_rows:
        count += 1
    return count


def low_stock_alert(products_rows: list, threshold: int = 5) -> list:
    """Return a list of product names where in_stock is False."""
    alerts = []
    for product in products_rows:
        if str(product["in_stock"]).strip().lower() == "false":
            alerts.append(product["product_name"])
    return alerts


def monthly_sales_trend(sales_rows: list) -> dict:
    """Aggregate total units sold per month (YYYY-MM) using a loop."""
    trend = {}
    for row in sales_rows:
        month = row["sale_date"][:7]  # "YYYY-MM"
        if month in trend:
            trend[month] += row["quantity"]
        else:
            trend[month] = row["quantity"]
    return trend


def classify_transaction_size(quantity: int) -> str:
    """Classify a transaction as Bulk, Multiple, Single, or Invalid based on quantity."""
    if quantity >= 5:
        return "Bulk"
    elif quantity >= 2:
        return "Multiple"
    elif quantity == 1:
        return "Single"
    else:
        return "Invalid"


def average_basket_size(sales_rows: list) -> float:
    """Calculate the average quantity per transaction across all sales records."""
    total = 0
    for row in sales_rows:
        total += row["quantity"]
    return round(total / len(sales_rows), 2)
