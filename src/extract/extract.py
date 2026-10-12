import pandas as pd
from pathlib import Path


def read_csv_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)

        print(f"Successfully read: {file_path}")
        print(f"Rows: {len(df)}")

        return df

    except Exception as e:
        raise RuntimeError(
            f"Error reading {file_path}: {e}"
        )


def validate_required_columns(df, required_columns, file_name):

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing required columns: "
            f"{missing_columns}"
        )

    print(f"Required columns verified for {file_name}")


def extract_data():

    customers = read_csv_file("data/customers.csv")
    products = read_csv_file("data/products.csv")
    orders = read_csv_file("data/orders.csv")

    validate_required_columns(
        customers,
        ["customer_id", "customer_name", "city"],
        "customers.csv"
    )

    validate_required_columns(
        products,
        ["product_id", "product_name", "category"],
        "products.csv"
    )

    validate_required_columns(
        orders,
        [
            "order_id",
            "order_date",
            "customer_id",
            "product_id",
            "quantity",
            "price"
        ],
        "orders.csv"
    )

    return customers, products, orders