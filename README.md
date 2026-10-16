# Thabo's Corner Store — Sales Insights System

**Student:** Yvonne Mthiyane  
**Student Number:** 0306091108085  
**Project:** KM-04 / KM-05 Integrated Project  
**Occupational Certificate:** Artificial Intelligence Software Developer · NQF Level 4

---

## Project Overview

This project builds a small but complete data application for Thabo's corner store.
It cleans raw CSV data, stores it in a relational SQLite database, analyses it with
Python, visualises the results as charts, and gates the reports behind a SHA-256
hashed password.

---

## Repository Structure

```
KM 04 - 05_Integrated_Project/
├── PLAN.md                        # Task 1 — computational thinking plan
├── SUBMISSION.txt                 # Submission details
├── data/
│   ├── products.csv               # Raw product data (14 products)
│   └── sales.csv                  # Raw sales data (71 records)
└── starter_code/
    ├── main.py                    # Entry point — run this
    ├── data_cleaning.py           # Task 2 — data cleaning
    ├── database.py                # Task 3 — SQLite database & SQL queries
    ├── analysis.py                # Task 4 — Python programming logic
    ├── visualize.py               # Task 5 — matplotlib charts
    ├── security.py                # Task 6 — password hashing & login gate
    ├── requirements.txt           # pandas, matplotlib
    ├── store.db                   # Generated SQLite database
    ├── revenue_per_product.png    # Generated bar chart
    └── monthly_trend.png          # Generated line chart
```

---

## How to Run

```bash
cd starter_code
pip install -r requirements.txt
python main.py
```

Password: `spaza2026`

---

## Full Documentation

All task documentation — data cleaning decisions, SQL queries and results,
chart descriptions, CIA-triad reflection, and business insights — is in
[`starter_code/README.md`](starter_code/README.md).
