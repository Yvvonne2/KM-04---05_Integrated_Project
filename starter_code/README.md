# Thabo's Corner Store — Sales Insights System

**Student:** Yvonne Mthiyane  
**Project:** KM-04 / KM-05 Integrated Project  
**Password to run reports:** `spaza2026`

---

## How to Install and Run

### 1. Prerequisites
- Python 3.10 or later
- Git

### 2. Install dependencies
```bash
cd starter_code
pip install -r requirements.txt
```

### 3. Run the project
```bash
cd starter_code
python main.py
```

You will be prompted for a password. Enter: `spaza2026`

The program will:
- Load and clean the raw CSV data
- Build `store.db` (SQLite database)
- Print analysis results to the terminal
- Save two charts: `revenue_per_product.png` and `monthly_trend.png`

---

## Task 1 — Computational Thinking Plan

See `PLAN.md` in the project root for the full plan written before coding began.

---

## Task 2 — Data Cleaning Decisions

### Raw data summary
- `products.csv`: **16 raw rows → 12 clean rows (4 removed)**
- `sales.csv`: **71 raw rows → 43 clean rows (28 removed)**

### Products cleaning decisions

| Issue | Decision | Reason |
|---|---|---|
| P006 missing `unit_price` | Row dropped | Cannot calculate revenue without a price |
| P013 missing `unit_price` | Row dropped | Same reason as above |
| P009 missing `product_name` | Row dropped | A product with no name is not usable data |
| P003 exact duplicate row | Duplicate removed | Keeping one copy is correct; two identical rows would double-count |
| `beverages` → `Beverages` | Title Case applied to all categories | Inconsistent capitalisation causes incorrect GROUP BY results in SQL |

### Sales cleaning decisions

| Issue | Decision | Reason |
|---|---|---|
| Missing `sale_date` (S0004, S0029, S0034, S0039, S0054, S0059, S0064, S0069) | Row dropped | Cannot analyse sales trends without a date |
| Missing `quantity` (S0006, S0053) | Row dropped | Cannot calculate revenue without a quantity |
| Invalid `product_id` P099 (S0024, S0048, S0062) | Row dropped | References a product that does not exist — data entry error |
| Sales referencing P006, P009, P013 | Row dropped | These products were removed during product cleaning (missing price/name), so their sales cannot be used |
| Missing `payment_method` | Filled with `"Unknown"` | Honest placeholder — guessing Cash/Card/Mobile would introduce false data |
| Missing `customer_type` | Filled with `"Unknown"` | Optional context field; does not affect revenue calculations |
| Duplicate row S0011 | Duplicate removed | Keeping one copy is correct |

### Date format standardisation

Dates in `sales.csv` appeared in four formats:
- `YYYY-MM-DD` (ISO — unambiguous)
- `YYYY/MM/DD` (ISO with slashes — unambiguous)
- `DD/MM/YYYY` (day-first with slashes)
- `DD-MM-YYYY` (day-first with dashes)

**Decision:** All dates were standardised to `YYYY-MM-DD` using **day-first** parsing for ambiguous formats (e.g. `05-01-2026` is read as 5 January 2026, not 1 May 2026). This follows South African date convention (DD/MM/YYYY) and is documented here so there is no silent ambiguity.

---

## Task 3 — Database Schema and SQL Queries

### Schema

```sql
CREATE TABLE products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT,
    unit_price   REAL,
    in_stock     TEXT
);

CREATE TABLE sales (
    sale_id        TEXT PRIMARY KEY,
    product_id     TEXT,
    quantity       INTEGER,
    sale_date      TEXT,
    payment_method TEXT,
    customer_type  TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### Query 1 — Total Revenue per Product (JOIN + SUM)

```sql
SELECT p.product_name,
       ROUND(SUM(s.quantity * p.unit_price), 2) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
```

**Results:**
```
('5kg Maize Meal',        801.0)
('Eggs (6 pack)',         364.0)
('Bar One Chocolate',     224.0)
('Sugar 1kg',             220.5)
('Coca-Cola 500ml',       148.0)
('Airtime Voucher R10',   140.0)
('Simba Chips 120g',      132.0)
('Full Cream Milk 1L',    129.0)
('Fanta Orange 500ml',    111.0)
('Data Bundle 1GB',        98.0)
('Coca-Cola 500ml',        74.0)
('White Bread 700g',       48.0)
```

### Query 2 — Best Selling Product by Units (SUM + LIMIT)

```sql
SELECT p.product_name, SUM(s.quantity) AS total_units
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_units DESC
LIMIT 1
```

**Result:**
```
('Bar One Chocolate', 16)
```

### Query 3 — Sales Count by Payment Method (COUNT + GROUP BY)

```sql
SELECT payment_method, COUNT(*) AS transaction_count
FROM sales
GROUP BY payment_method
ORDER BY transaction_count DESC
```

**Results:**
```
('Cash',         14)
('Mobile Money', 11)
('Card',         10)
('Unknown',       8)
```

### Query 4 (Custom) — Revenue by Category

*Business question: Which product category earns Thabo the most money?*

```sql
SELECT p.category,
       ROUND(SUM(s.quantity * p.unit_price), 2) AS category_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC
```

**Results:**
```
('Household',     1021.5)
('Dairy',          493.0)
('Snacks',         356.0)
('Beverages',      333.0)
('Airtime & Data', 238.0)
('Bakery',          48.0)
```

### Query 5 (Custom) — Monthly Sales Count and Revenue

*Business question: How is the store performing month by month?*

```sql
SELECT SUBSTR(s.sale_date, 1, 7) AS month,
       COUNT(*) AS num_sales,
       ROUND(SUM(s.quantity * p.unit_price), 2) AS monthly_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY month
ORDER BY month
```

**Results:**
```
('2026-01', 25, 1592.5)
('2026-02', 18,  897.0)
```

---

## Task 5 — Chart Descriptions

### Chart 1: `revenue_per_product.png` — Bar Chart of Revenue per Product

This bar chart shows the total rand revenue earned by each product across all recorded sales. The tallest bar belongs to **5kg Maize Meal (R801)**, which is the highest-revenue product despite being a low-margin staple — it sells in high quantities. **Eggs (6 pack)** comes second at R364. The chart makes it immediately clear which products are driving the most income and which (like White Bread at R48) contribute very little.

### Chart 2: `monthly_trend.png` — Line Chart of Monthly Sales Trend

This line chart plots the total units sold per month. January 2026 saw **52 units** sold across 25 transactions, while February 2026 dropped to **44 units** across 18 transactions. The downward trend between the two months is visible at a glance and prompts the question of whether this is a seasonal dip or the start of a longer decline — something Thabo should monitor as more months of data are collected.

---

## Task 6 — Data Security: CIA Triad Reflection

### How the security design maps to the CIA Triad

**Confidentiality** is the principle that only authorised people can see sensitive information. The login gate in `security.py` enforces this by requiring a correct password before any sales reports are displayed. Crucially, the password is never stored as plain text — only its SHA-256 hash is kept in the code. Even if someone reads the source file, they cannot reverse the hash back into the original password. This means Thabo's sales data stays private from anyone who does not know the password.

**Integrity** is the principle that data is accurate and has not been tampered with. The login gate alone does not protect integrity — that is handled in `database.py` through the relational schema design. The `products` table uses `product_id` as a PRIMARY KEY, which prevents duplicate product records. The `sales` table uses a FOREIGN KEY linking `product_id` back to `products`, which prevents a sale from being recorded against a product that does not exist. The `NOT NULL` constraint on `product_name` ensures no nameless product can enter the database. Together these constraints keep the data trustworthy.

**Availability** is the principle that data is accessible when needed. The biggest availability risk for this project is that the entire database (`store.db`) lives on a single laptop. If that laptop is lost, stolen, or the hard drive fails, all of Thabo's sales history is gone. The recommended protection is a regular automated backup — for example, copying `store.db` to a cloud storage service (such as Google Drive or AWS S3) every night. A version-controlled GitHub repository also provides a partial backup of the code, though not the database itself.

> **Note on hash storage:** In this project, `STORED_PASSWORD_HASH` is hardcoded in `security.py`. In a production system it would be better to store the hash in the database (in a `users` table), so that passwords can be changed without editing source code and so that multiple users with different access levels could be supported.

---

## Task 7 — Key Business Insights for Thabo

Here is a plain-language summary of what the data shows about your corner store.

**Your biggest money-maker is 5kg Maize Meal.** It brought in R801 over the period — more than double the next product. Even though each bag is not the most expensive item on your shelf, customers buy it regularly and in decent quantities. Make sure you never run out of stock.

**Bar One Chocolate is your most popular product by units sold** — 16 units across the period. It is a quick, cheap impulse buy that customers grab at the till. Keeping a well-stocked display near the counter could push this number even higher.

**The Household category (Maize Meal + Sugar) earns the most revenue overall (R1 021.50)**, followed by Dairy (R493). These everyday essentials are the backbone of your income. Beverages and Snacks are popular but earn less because the items are lower-priced.

**Cash is still your most common payment method** (14 transactions), but Mobile Money (11) and Card (10) are close behind. This tells you that a significant portion of your customers expect to pay digitally — it is worth making sure your card machine and mobile payment options are always working.

**Sales dropped from January to February** — from 52 units and R1 592.50 down to 44 units and R897. This could be a normal post-January slowdown, or it could signal a problem. As you collect more months of data, this trend line will become much more informative.

**One product needs restocking:** Data Bundle 1GB is currently marked as out of stock. Given that Airtime & Data is your fifth-highest revenue category, getting this back on the shelf is worth prioritising.

---

## File Structure

```
KM 04 - 05_Integrated_Project/
├── PLAN.md                        # Task 1 — computational thinking plan
├── data/
│   ├── products.csv               # Raw product data
│   └── sales.csv                  # Raw sales data
└── starter_code/
    ├── main.py                    # Entry point — run this
    ├── data_cleaning.py           # Task 2 — data cleaning
    ├── database.py                # Task 3 — SQLite database & SQL queries
    ├── analysis.py                # Task 4 — Python programming logic
    ├── visualize.py               # Task 5 — matplotlib charts
    ├── security.py                # Task 6 — password hashing & login gate
    ├── requirements.txt           # pandas, matplotlib
    ├── store.db                   # Generated SQLite database (after running)
    ├── revenue_per_product.png    # Generated chart (after running)
    └── monthly_trend.png          # Generated chart (after running)
```
