import pandas as pd
from pathlib import Path

from src.extract.extract import extract_data
from src.validate.validate import validate_orders
from src.transform.transform import transform_orders


def save_to_csv(df, file_path):
    """
    Save a DataFrame to a CSV file.
    """

    file_path = Path(file_path)

    # Create the parent directory if it does not exist.
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
    # 4. Save valid orders
    # -------------------------------------------------

    save_to_csv(
        transformed_orders,
        "output/valid_orders.csv"
    )

    # -------------------------------------------------
    # 5. Save rejected orders
    # -------------------------------------------------

    save_to_csv(
        rejected_orders,
        "output/rejected_orders.csv"
    )
