# Retail ETL Pipeline

## 1. Project Overview

The **Retail ETL Pipeline** is an end-to-end data engineering project built using Python and Pandas. It extracts retail data from CSV files, validates the data quality, separates valid and rejected records, transforms the valid data by joining customer and product information, calculates sales amounts, loads the processed data into output CSV files **and a relational database via a SQLAlchemy ORM layer**, and generates analytical reports (both from Pandas and directly from the ORM).

The project follows a modular ETL architecture with separate components for extraction, validation, transformation, CSV loading, database loading (ORM), reporting, logging, and testing.

---

## 2. Project Objectives

The main objectives of this project are:

* Extract retail data from CSV files.
* Verify required files and columns.
* Perform data quality validation.
* Identify missing values and duplicate records.
* Detect invalid dates.
* Detect negative quantities and prices.
* Identify unknown customer and product IDs.
* Separate valid and rejected orders.
* Join orders with customer and product information.
* Calculate sales amount.
* Generate business reports.
* Save processed data and reports as CSV files.
* Persist customers, products, and orders into a relational database via an ORM (SQLAlchemy).
* Query the same business reports directly from the database using ORM aggregation.
* Maintain execution logs.
* Automate testing using Pytest.

---

## 3. Technologies Used

* **Python 3**
* **Pandas**
* **SQLAlchemy (ORM)**
* **SQLite** (default database; MySQL/Postgres supported by changing one URL)
* **Pytest**
* **Logging**
* **CSV**
* **Git / GitHub**

---

## 4. Project Structure

```text
retail_etl/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── output/
│   ├── valid_orders.csv
│   ├── rejected_orders.csv
│   ├── customer_summary.csv
│   ├── product_summary.csv
│   ├── city_summary.csv
│   ├── category_summary.csv
│   └── daily_sales.csv
│
├── logs/
│   └── retail_etl.log
│
├── tests/
│   ├── __init__.py
│   ├── test_validate.py
│   ├── test_transform.py
│   ├── test_reports.py
│   └── test_db_services.py
│
├── main.py
├── config.py
├── extract.py
├── validate.py
├── transform.py
├── load.py
├── db.py             # SQLAlchemy engine + session (ORM connection)
├── models.py          # SQLAlchemy ORM models: Customer, Product, Order
├── db_services.py      # ORM load (upsert) + ORM report queries
├── reports.py
├── retail_etl.db       # SQLite database file (created on first run)
├── README.md
└── requirements.txt
```

---

## 5. ETL Architecture

```text
                 CSV DATA SOURCES
                       │
                       ▼
                  ┌─────────┐
                  │ EXTRACT │
                  └────┬────┘
                       │
                       ▼
                 ┌──────────┐
                 │ VALIDATE │
                 └────┬─────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Valid Orders      Rejected Orders
             │                 │
             ▼                 │
       ┌───────────┐            │
       │ TRANSFORM │            │
       └─────┬─────┘            │
             │                  │
             ▼                  │
        ┌────────┐              │
        │  LOAD  │◄─────────────┘
        │ (CSV)  │
        └────┬───┘
             │
             ▼
      ┌───────────────┐
      │ LOAD (ORM/DB)  │   SQLAlchemy models → Customer / Product / Order
      └───────┬────────┘
              │
              ▼
        ┌──────────┐
        │ REPORTS  │   (Pandas groupby  +  ORM aggregation queries)
        └──────────┘
```

---

## 6. Input Data

The pipeline uses three CSV files.

### Customers

Contains:

* `customer_id`
* `customer_name`
* `city`

### Products

Contains:

* `product_id`
* `product_name`
* `category`

### Orders

Contains:

* `order_id`
* `order_date`
* `customer_id`
* `product_id`
* `quantity`
* `price`

---

## 7. Data Validation

The pipeline performs the following data quality checks:

### Missing Values

Records containing NULL or missing values are rejected.

### Duplicate Orders

Duplicate `order_id` values are detected and rejected.

### Invalid Dates

Invalid order dates are detected using Pandas date conversion.

### Negative Quantity

Orders containing negative quantities are rejected.

### Negative Price

Orders containing negative prices are rejected.

### Unknown Customer

Orders containing customer IDs that do not exist in `customers.csv` are rejected.

### Unknown Product

Orders containing product IDs that do not exist in `products.csv` are rejected.

---

## 8. Data Transformation

Only valid orders are passed to the transformation stage.

The transformation performs:

### Customer Join

Orders are joined with customer data using:

```text
customer_id
```

This adds:

```text
customer_name
city
```

### Product Join

Orders are joined with product data using:

```text
product_id
```

This adds:

```text
product_name
category
```

### Sales Calculation

The pipeline calculates:

```text
sales_amount = quantity × price
```

### Date Standardization

The `order_date` column is converted into a proper datetime format.

---

## 8b. Database Load (ORM)

After the CSV load step, the pipeline persists the same data into a
relational database using a SQLAlchemy ORM layer (`db.py`, `models.py`,
`db_services.py`), mirroring the pattern used in the standalone
`sql_orm` reference project.

### Models (`models.py`)

Three declarative ORM models, normalized with primary/foreign keys:

* `Customer(customer_id PK, customer_name, city)`
* `Product(product_id PK, product_name, category)`
* `Order(order_id PK, order_date, customer_id FK, product_id FK, quantity, price, sales_amount)`

`create_tables()` creates these tables (`Base.metadata.create_all`) if
they don't already exist.

### Connection (`db.py`)

```python
DATABASE_URL = f"sqlite:///{BASE_DIR / 'retail_etl.db'}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
```

Defaults to a local SQLite file so the pipeline runs with zero setup.
To use MySQL or Postgres instead (as in the `sql_orm` project), just
change `DATABASE_URL`, e.g.:

```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/retail_etl"
```

### Load & Query (`db_services.py`)

* `upsert_customers` / `upsert_products` / `upsert_orders` — insert-or-update
  rows from the pandas DataFrames using `session.get()` + `session.add()`.
* `load_transformed_data(customers, products, transformed_orders)` — runs
  `create_tables()` then upserts customers → products → orders in that
  order, so foreign keys resolve.
* `get_customer_summary` / `get_product_summary` / `get_city_summary` /
  `get_category_summary` / `get_daily_sales` — the same five business
  reports as `reports.py`, computed with ORM queries (`select(...).join(...).group_by(...)`
  and `func.count` / `func.sum`) instead of `pandas.groupby`, useful for
  querying the warehouse directly without re-running the CSV pipeline.

`main.py` calls `load_transformed_data()` right after the CSV load step,
so every pipeline run keeps the database in sync with the CSV output.

---

## 9. Reports Generated

The pipeline generates five analytical reports.

### Customer Summary

Provides:

* Total orders per customer
* Total sales per customer

### Product Summary

Provides:

* Total quantity sold
* Total sales per product

### City Summary

Provides:

* Total orders per city
* Total sales per city

### Category Summary

Provides:

* Total quantity sold per category
* Total sales per category

### Daily Sales

Provides:

* Total orders per day
* Total sales per day

---

## 10. Current Pipeline Results

For the current sample dataset:

```text
Total input orders     : 20
Valid orders           : 12
Rejected orders        : 8
Transformed orders     : 12
```

Generated reports:

```text
Customer summary       : 10 rows
Product summary        : 10 rows
City summary           : 8 rows
Category summary       : 5 rows
Daily sales            : 6 rows
```

---

## 11. Logging

The project uses Python's built-in `logging` module.

Logs are stored in:

```text
logs/retail_etl.log
```

The log records important pipeline events such as:

* Pipeline start
* Extraction
* Validation
* Transformation
* Loading
* Report generation
* Pipeline completion
* Errors

---

## 12. Testing

The project uses **Pytest** for automated testing.

Current test structure:

```text
tests/
├── test_validate.py
├── test_transform.py
└── test_reports.py
```

The test suite currently contains:

```text
Validation tests      : 8
Transformation tests  : 1
Reporting tests       : 5
--------------------------------
Total tests           : 14
```

All tests currently pass:

```text
14 passed
```

---

## 13. Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project:

```bash
cd retail_etl
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 14. Running the Pipeline

Run the complete ETL pipeline using:

```bash
python main.py
```

The pipeline will:

```text
Extract
   ↓
Validate
   ↓
Transform
   ↓
Load
   ↓
Generate Reports
```

---

## 15. Running Tests

Run all automated tests:

```bash
pytest
```

Expected result:

```text
14 passed
```

---

## 16. Output Files

After successful execution, the `output/` directory contains:

```text
valid_orders.csv
rejected_orders.csv
customer_summary.csv
product_summary.csv
city_summary.csv
category_summary.csv
daily_sales.csv
```

---

## 17. Error Handling

The pipeline uses exception handling to prevent silent failures.

If an error occurs during pipeline execution:

* The error is logged.
* The error message is displayed.
* The pipeline reports failure.
* The exception is raised for further debugging.

---

## 18. Future Enhancements

Possible improvements include:

* Point the existing ORM layer at PostgreSQL or MySQL for production use.
* Alembic migrations for schema versioning.
* Airflow workflow orchestration.
* Configuration using JSON or YAML.
* Advanced data quality reports.
* Retry mechanisms.
* Command-line arguments.
* Docker containerization.
* Cloud storage integration.
* Data visualization dashboards.
* CI/CD integration using GitHub Actions.

---

## 19. Conclusion

The Retail ETL Pipeline demonstrates a complete data engineering workflow using Python and Pandas. It follows a modular architecture and includes extraction, data quality validation, transformation, loading, reporting, logging, and automated testing. The project can be extended further with databases, Airflow, Docker, cloud platforms, and visualization tools.
