import logging
from src.extract.extract import extract_data
from src.validate.validate import validate_orders
from src.transform.transform import transform_orders
from src.load.load import save_to_csv

from src.reports.reports import (
    create_customer_summary,
    create_product_summary,
    create_city_summary,
    create_category_summary,
    create_daily_sales
)

from src.visualization.graphs import create_graphs


# -------------------------------------------------
# LOGGING CONFIGURATION
# -------------------------------------------------

logging.basicConfig(
    filename="logs/retail_etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """
    Run the complete retail ETL pipeline.
    """

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

        logger.info(
            "Extraction completed successfully. "
            "Customers: %d, Products: %d, Orders: %d",
            len(customers),
            len(products),
            len(orders)
        )

        print("Extraction completed successfully.")

        # -------------------------------------------------
        # 2. VALIDATE
        # -------------------------------------------------

        print("\n[2] VALIDATE")
        logger.info("Starting validation")

        valid_orders, rejected_orders = validate_orders(
            orders,
            customers,
            products
        )

        logger.info(
            "Validation completed. "
            "Total: %d, Valid: %d, Rejected: %d",
            len(orders),
            len(valid_orders),
            len(rejected_orders)
        )

        print(f"Total orders: {len(orders)}")
        print(f"Valid orders: {len(valid_orders)}")
        print(f"Rejected orders: {len(rejected_orders)}")

        # -------------------------------------------------
        # 3. TRANSFORM
        # -------------------------------------------------

        print("\n[3] TRANSFORM")
        logger.info("Starting transformation")

        transformed_orders = transform_orders(
            valid_orders,
            customers,
            products
        )

        logger.info(
            "Transformation completed. Rows: %d",
            len(transformed_orders)
        )

        print(
            f"Transformation completed. "
            f"Rows: {len(transformed_orders)}"
        )

        # -------------------------------------------------
        # 4. LOAD
        # -------------------------------------------------

        print("\n[4] LOAD")
        logger.info("Starting data loading")

        save_to_csv(
            transformed_orders,
            "output/valid_orders.csv"
        )

        save_to_csv(
            rejected_orders,
            "output/rejected_orders.csv"
        )

        logger.info("Valid and rejected orders saved successfully")

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
        logger.info("Saving generated reports")

        save_to_csv(
            customer_summary,
            "output/customer_summary.csv"
        )

        save_to_csv(
            product_summary,
            "output/product_summary.csv"
        )

        save_to_csv(
            city_summary,
            "output/city_summary.csv"
        )

        save_to_csv(
            category_summary,
            "output/category_summary.csv"
        )

        save_to_csv(
            daily_sales,
            "output/daily_sales.csv"
        )

        logger.info("All reports generated successfully")

        # -------------------------------------------------
        # 7. VISUALIZATION
        # -------------------------------------------------

        print("\n[7] VISUALIZATION")
        logger.info("Starting visualization")

        create_graphs()

        logger.info("Graphs generated successfully")

        print("Graphs generated successfully.")

        # -------------------------------------------------
        # PIPELINE COMPLETED
        # -------------------------------------------------

        print("\n==============================")
        print("ETL PIPELINE COMPLETED")
        print("==============================")

        logger.info(
            "Retail ETL pipeline completed successfully"
        )

    except Exception as e:

        logger.error(
            "ETL pipeline failed: %s",
            e,
            exc_info=True
        )

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