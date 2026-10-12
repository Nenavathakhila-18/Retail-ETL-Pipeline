import pandas as pd

from src.extract.extract import extract_data
from src.validate.validate import validate_orders


def transform_orders(orders, customers, products):
    """
    Transform valid orders by joining customer and product
    information and calculating sales amount.
    """

    # Make a copy so the original data is not modified.
    transformed_orders = orders.copy()

    # -------------------------------------------------
    # 1. Convert order_date to datetime
    # -------------------------------------------------

    transformed_orders["order_date"] = pd.to_datetime(
        transformed_orders["order_date"]
    )

    # -------------------------------------------------
    # 2. Join orders with customer information
    # -------------------------------------------------

    transformed_orders = transformed_orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # -------------------------------------------------
    # 3. Join orders with product information
    # -------------------------------------------------

    transformed_orders = transformed_orders.merge(
        products,
        on="product_id",
        how="left"
    )

    # -------------------------------------------------
    # 4. Calculate sales amount
    # -------------------------------------------------

    transformed_orders["sales_amount"] = (
        transformed_orders["quantity"]
        * transformed_orders["price"]
    )

    # -------------------------------------------------
    # 5. Select columns in the desired order
    # -------------------------------------------------

    transformed_orders = transformed_orders[
        [
            "order_id",
            "order_date",
            "customer_id",
            "customer_name",
            "city",
            "product_id",
            "product_name",
            "category",
            "quantity",
            "price",
            "sales_amount"
        ]
    ]

    return transformed_orders


if __name__ == "__main__":

    # Extract data
    customers, products, orders = extract_data()

    # Validate orders
    valid_orders, rejected_orders = validate_orders(
        orders,
        customers,
        products
    )

    # Transform valid orders
    transformed_orders = transform_orders(
        valid_orders,
        customers,
        products
    )

    print("\n==============================")
    print("TRANSFORMED ORDERS")
    print("==============================")

    print(transformed_orders)

    print("\nTotal transformed orders:")
    print(len(transformed_orders))
