import logging
from pathlib import Path

from src.extract.extract import extract_data
from src.validate.validate import validate_orders
from src.transform.transform import transform_orders
from src.load.load import save_to_csv

from src.database.db_services import load_transformed_data

from src.reports.reports import (
    create_customer_summary,
    create_product_summary,
    create_city_summary,
    create_category_summary,
    create_daily_sales,
)

from src.visualization.graphs import create_graphs


# -------------------------------------------------
# PATHS AND LOGGING CONFIGURATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "retail_etl.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """Run the complete Retail ETL pipeline."""

    print("\n==============================")
    print("STARTING RETAIL ETL PIPELINE")
    print("==============================")

    logger.info("Retail ETL pipeline started")

    try:
        # -------------------------------------------------
        # 1. EXTRACT
        # -------------------------------------------------

        print("\n[1] EXTRACT")
        logger.info("Starting extraction")

        customers, products, orders = extract_data()

        print(f"Customers extracted: {len(customers)}")
        print(f"Products extracted: {len(products)}")
        print(f"Orders extracted: {len(orders)}")

        logger.info(
            "Extraction completed. Customers: %d, Products: %d, Orders: %d",
            len(customers),
            len(products),
            len(orders),
        )

        # -------------------------------------------------
        # 2. VALIDATE
        # -------------------------------------------------

        print("\n[2] VALIDATE")
        logger.info("Starting validation")

        valid_orders, rejected_orders = validate_orders(
            orders,
            customers,
            products,
        )

        print(f"Total orders: {len(orders)}")
        print(f"Valid orders: {len(valid_orders)}")
        print(f"Rejected orders: {len(rejected_orders)}")

        logger.info(
            "Validation completed. Total: %d, Valid: %d, Rejected: %d",
            len(orders),
            len(valid_orders),
            len(rejected_orders),
        )

        # -------------------------------------------------
        # 3. TRANSFORM
        # -------------------------------------------------

        print("\n[3] TRANSFORM")
        logger.info("Starting transformation")

        transformed_orders = transform_orders(
            valid_orders,
            customers,
            products,
        )

        print(f"Transformed orders: {len(transformed_orders)}")

        logger.info(
            "Transformation completed. Rows: %d",
            len(transformed_orders),
        )

        # -------------------------------------------------
        # 4. LOAD
        # -------------------------------------------------

        print("\n[4] LOAD")
        logger.info("Starting CSV and database loading")

        # Save valid and rejected orders as CSV files.
        save_to_csv(
            transformed_orders,
            str(OUTPUT_DIR / "valid_orders.csv"),
        )

        save_to_csv(
            rejected_orders,
            str(OUTPUT_DIR / "rejected_orders.csv"),
        )

        print("Valid and rejected orders saved to CSV.")

        # Insert/update database records using SQLAlchemy ORM.
        # Customers and products are loaded before orders
        # because orders reference them through foreign keys.
        load_transformed_data(
            customers,
            products,
            transformed_orders,
        )

        print("Customers loaded into the database.")
        print("Products loaded into the database.")
        print("Orders loaded into the database.")

        logger.info("Database loading completed successfully")

        # -------------------------------------------------
        # 5. REPORTING
        # -------------------------------------------------

        print("\n[5] REPORTING")
        logger.info("Starting report generation")

        customer_summary = create_customer_summary(
            transformed_orders
        )

        product_summary = create_product_summary(
            transformed_orders
        )

        city_summary = create_city_summary(
            transformed_orders
        )

        category_summary = create_category_summary(
            transformed_orders
        )

        daily_sales = create_daily_sales(
            transformed_orders
        )

        # -------------------------------------------------
        # 6. SAVE REPORTS
        # -------------------------------------------------

        print("\n[6] SAVE REPORTS")
        logger.info("Saving reports")

        save_to_csv(
            customer_summary,
            str(OUTPUT_DIR / "customer_summary.csv"),
        )

        save_to_csv(
            product_summary,
            str(OUTPUT_DIR / "product_summary.csv"),
        )

        save_to_csv(
            city_summary,
            str(OUTPUT_DIR / "city_summary.csv"),
        )

        save_to_csv(
            category_summary,
            str(OUTPUT_DIR / "category_summary.csv"),
        )

        save_to_csv(
            daily_sales,
            str(OUTPUT_DIR / "daily_sales.csv"),
        )

        print("All reports saved successfully.")

        # -------------------------------------------------
        # 7. VISUALIZATION
        # -------------------------------------------------

        print("\n[7] VISUALIZATION")
        logger.info("Starting visualization")

        create_graphs()

        print("Graphs generated successfully.")
        logger.info("Graphs generated successfully")

        # -------------------------------------------------
        # PIPELINE COMPLETED
        # -------------------------------------------------

        print("\n==============================")
        print("ETL PIPELINE COMPLETED")
        print("==============================")

        logger.info("Retail ETL pipeline completed successfully")

    except Exception as e:
        logger.exception("Retail ETL pipeline failed: %s", e)

        print("\n==============================")
        print("ETL PIPELINE FAILED")
        print("==============================")
        print(f"Error: {e}")

        raise


# -------------------------------------------------
# MAIN
# -------------------------------------------------

if __name__ == "__main__":
    run_pipeline()