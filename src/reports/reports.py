import pandas as pd
from pathlib import Path

from src.extract.extract import extract_data
from src.validate.validate import validate_orders
from src.transform.transform import transform_orders

def create_customer_summary(df):
    """
    Create a summary of sales by customer.
    """

    customer_summary = (
        df.groupby(
            ["customer_id", "customer_name"]
        )
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )

    return customer_summary


def create_product_summary(df):
    """
    Create a summary of sales by product.
    """

    product_summary = (
        df.groupby(
            ["product_id", "product_name"]
        )
        .agg(
            total_quantity=("quantity", "sum"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )

    return product_summary


def create_city_summary(df):
    """
    Create a summary of sales by city.
    """

    city_summary = (
        df.groupby("city")
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )

    return city_summary


def create_category_summary(df):
    """
    Create a summary of sales by product category.
    """

    category_summary = (
        df.groupby("category")
        .agg(
            total_quantity=("quantity", "sum"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )

    return category_summary


def create_daily_sales(df):
    """
    Create a daily sales summary.
    """

    daily_sales = (
        df.groupby("order_date")
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("sales_amount", "sum")
        )
        .reset_index()
    )

    return daily_sales


def save_report(df, file_path):
    """
    Save a report DataFrame as a CSV file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False
    )

    print(f"Successfully saved: {file_path}")
    print(f"Rows saved: {len(df)}")


if __name__ == "__main__":

    # -------------------------------------------------
    # 1. Extract data
    # -------------------------------------------------

    customers, products, orders = extract_data()

    # -------------------------------------------------
    # 2. Validate orders
    # -------------------------------------------------

    valid_orders, rejected_orders = validate_orders(
        orders,
        customers,
        products
    )

    # -------------------------------------------------
    # 3. Transform valid orders
    # -------------------------------------------------

    transformed_orders = transform_orders(
        valid_orders,
        customers,
        products
    )

    # -------------------------------------------------
    # 4. Create reports
    # -------------------------------------------------

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
    # 5. Save reports
    # -------------------------------------------------

    save_report(
        customer_summary,
        "output/customer_summary.csv"
    )

    save_report(
        product_summary,
        "output/product_summary.csv"
    )

    save_report(
        city_summary,
        "output/city_summary.csv"
    )

    save_report(
        category_summary,
        "output/category_summary.csv"
    )

    save_report(
        daily_sales,
        "output/daily_sales.csv"
    )

    print("ALL REPORTS GENERATED")
