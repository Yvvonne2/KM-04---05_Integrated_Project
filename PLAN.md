# PLAN.md — Computational Thinking Plan

## Decomposition (Breaking the Problem Down)

The project has five clear sub-problems, each mapping to a module:

1. **Data Cleaning** (`data_cleaning.py`) — Load raw CSVs, fix quality issues, produce clean DataFrames.
2. **Database** (`database.py`) — Design a relational schema, insert clean data, write SQL queries.
3. **Analysis** (`analysis.py`) — Use plain Python loops and conditionals to derive business insights.
4. **Visualisation** (`visualize.py`) — Turn analysis results into labelled charts saved as PNG files.
5. **Security** (`security.py`) — Gate the reports behind a SHA-256 hashed password.

## Pattern Recognition (What I Expect to Find Messy)

- **products.csv**: one missing `product_name`, two missing `unit_price` values, inconsistent category capitalisation (`beverages` vs `Beverages`), one duplicate row (P003 appears twice).
- **sales.csv**: dates in at least four formats (`YYYY-MM-DD`, `DD/MM/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY`), missing `sale_date`, missing `quantity`, missing `payment_method`, rows referencing non-existent product `P099`, one duplicate row (S0011).
- The ambiguous date `05-01-2026` could be 5 Jan or 1 May — I will standardise on **DD-MM-YYYY** for `DD-MM-YYYY` style strings (day first), consistent with South African date convention.

## Abstraction (What to Ignore / Simplify)

- `customer_type` is optional context — missing values will be left as-is (filled with `"Unknown"`) rather than dropped, because they don't affect revenue calculations.
- `in_stock` is a flag, not a quantity — the low-stock alert will flag any product where `in_stock == False`.
- No need to build a web interface; `main.py` running in the terminal is sufficient.

## Algorithm (Order of Execution)

```
START
  1. Load raw CSVs                          → data_cleaning.load_raw_data()
  2. Clean products                         → data_cleaning.clean_products()
  3. Clean sales (using valid product IDs)  → data_cleaning.clean_sales()
  4. Create SQLite DB & tables              → database.create_tables()
  5. Insert clean data                      → database.insert_products/sales()
  6. Run SQL queries                        → database.query_*()
  7. Run Python analysis                    → analysis.*()
  8. Generate charts                        → visualize.*()
  9. Security gate (password check)         → security.login_gate()
END
```

## Module Order

I will complete the modules in this order:
`data_cleaning.py` → `database.py` → `analysis.py` → `visualize.py` → `security.py` → `README.md`
