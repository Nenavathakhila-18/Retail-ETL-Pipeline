from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"


# Input files
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"


# Output files
VALID_ORDERS_FILE = OUTPUT_DIR / "valid_orders.csv"
REJECTED_ORDERS_FILE = OUTPUT_DIR / "rejected_orders.csv"

CUSTOMER_SUMMARY_FILE = OUTPUT_DIR / "customer_summary.csv"
PRODUCT_SUMMARY_FILE = OUTPUT_DIR / "product_summary.csv"
CITY_SUMMARY_FILE = OUTPUT_DIR / "city_summary.csv"
CATEGORY_SUMMARY_FILE = OUTPUT_DIR / "category_summary.csv"
DAILY_SALES_FILE = OUTPUT_DIR / "daily_sales.csv"


# Log file
LOG_FILE = LOG_DIR / "retail_etl.log"
