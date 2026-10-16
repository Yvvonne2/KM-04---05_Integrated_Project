"""
visualize.py
-------------
Task 5: Turn your analysis into charts.
"""

import matplotlib.pyplot as plt


def bar_chart_revenue_per_product(product_names: list, revenues: list, save_path: str = "revenue_per_product.png"):
    """Create and save a bar chart of total revenue per product."""
    plt.figure(figsize=(12, 6))
    bars = plt.bar(product_names, revenues, color="steelblue", edgecolor="white")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.ylabel("Revenue (R)")
    plt.title("Total Revenue per Product — Thabo's Corner Store")
    # Label each bar with its value
    for bar, rev in zip(bars, revenues):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                 f"R{rev:.0f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def line_chart_monthly_trend(monthly_trend: dict, save_path: str = "monthly_trend.png"):
    """Create and save a line chart of total quantity sold per month."""
    months = sorted(monthly_trend.keys())
    totals = [monthly_trend[m] for m in months]
    plt.figure(figsize=(8, 5))
    plt.plot(months, totals, marker="o", color="darkorange", linewidth=2, markersize=8)
    for x, y in zip(months, totals):
        plt.text(x, y + 1, str(y), ha="center", va="bottom", fontsize=9)
    plt.ylabel("Units Sold")
    plt.xlabel("Month")
    plt.title("Monthly Sales Trend — Thabo's Corner Store")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
