import pandas as pd

from src.extract.extract import extract_data


def find_null_records(df):
    """
    Find records that contain NULL/missing values.
    """

    null_mask = df.isnull().any(axis=1)

    null_records = df[null_mask]

    return null_records


def find_duplicate_records(df, subset=None):
    """
    Find duplicate records in a DataFrame.
    """

    duplicate_mask = df.duplicated(
        subset=subset,
        keep="first"
    )

    duplicate_records = df[duplicate_mask]

    return duplicate_records


def check_data_types(df):
    """
    Display the data types of each column.
    """

    print("\nData types:")
    print(df.dtypes)

    return df.dtypes


def find_invalid_dates(df, column):
    """
    Find records with invalid dates.
    """

    converted_dates = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    invalid_mask = converted_dates.isna()

    invalid_records = df[invalid_mask]

    return invalid_records


def find_negative_quantity_records(df):
    """
    Find orders with negative quantities.
    """

    negative_quantity_mask = df["quantity"] < 0

    return df[negative_quantity_mask]


def find_negative_price_records(df):
    """
    Find orders with negative prices.
    """

    negative_price_mask = df["price"] < 0

    return df[negative_price_mask]


def find_unknown_customer_records(orders, customers):
    """
    Find orders that reference unknown customer IDs.
    """

    valid_customer_ids = set(
        customers["customer_id"]
    )

    unknown_customer_mask = ~orders["customer_id"].isin(
        valid_customer_ids
    )

    return orders[unknown_customer_mask]


def find_unknown_product_records(orders, products):
    """
    Find orders that reference unknown product IDs.
    """

    valid_product_ids = set(
        products["product_id"]
    )

    unknown_product_mask = ~orders["product_id"].isin(
        valid_product_ids
    )

    return orders[unknown_product_mask]


def validate_orders(orders, customers, products):
    """
    Validate all orders and separate them into
    valid and rejected records.
    """

    # Create a copy so that the original DataFrame
    # is not modified.
    orders = orders.copy()

    # Create a column to store rejection reasons.
    orders["rejection_reason"] = ""

    # -------------------------------------------------
    # 1. Check NULL values
    # -------------------------------------------------

    null_mask = orders.isnull().any(axis=1)

    orders.loc[
        null_mask,
        "rejection_reason"
    ] = "Missing value"

    # -------------------------------------------------
    # 2. Check duplicate orders
    # -------------------------------------------------

    duplicate_mask = orders.duplicated(
        subset=["order_id"],
        keep="first"
    )

    orders.loc[
        duplicate_mask,
        "rejection_reason"
    ] = "Duplicate order"

    # -------------------------------------------------
    # 3. Check invalid dates
    # -------------------------------------------------

    converted_dates = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    invalid_date_mask = converted_dates.isna()

    orders.loc[
        invalid_date_mask,
        "rejection_reason"
    ] = "Invalid date"

    # -------------------------------------------------
    # 4. Check negative quantity
    # -------------------------------------------------

    negative_quantity_mask = orders["quantity"] < 0

    orders.loc[
        negative_quantity_mask,
        "rejection_reason"
    ] = "Negative quantity"

    # -------------------------------------------------
    # 5. Check negative price
    # -------------------------------------------------

    negative_price_mask = orders["price"] < 0

    orders.loc[
        negative_price_mask,
        "rejection_reason"
    ] = "Negative price"

    # -------------------------------------------------
    # 6. Check unknown customer IDs
    # -------------------------------------------------

    valid_customer_ids = set(
        customers["customer_id"]
    )

    unknown_customer_mask = ~orders["customer_id"].isin(
        valid_customer_ids
    )

    orders.loc[
        unknown_customer_mask,
        "rejection_reason"
    ] = "Unknown customer ID"

    # -------------------------------------------------
    # 7. Check unknown product IDs
    # -------------------------------------------------

    valid_product_ids = set(
        products["product_id"]
    )

    unknown_product_mask = ~orders["product_id"].isin(
        valid_product_ids
    )

    orders.loc[
        unknown_product_mask,
        "rejection_reason"
    ] = "Unknown product ID"

    # -------------------------------------------------
    # Separate valid and rejected orders
    # -------------------------------------------------

    rejected_mask = orders["rejection_reason"] != ""

    rejected_orders = orders[rejected_mask].copy()

    valid_orders = orders[~rejected_mask].copy()

    # Remove rejection_reason from valid orders.
    valid_orders = valid_orders.drop(
        columns=["rejection_reason"]
    )

    return valid_orders, rejected_orders


if __name__ == "__main__":

    # Extract data
    customers, products, orders = extract_data()

    # -------------------------------------------------
    # Individual validation checks
    # -------------------------------------------------

    null_orders = find_null_records(orders)

    print("\nOrders containing NULL values:")
    print(null_orders)

    duplicate_orders = find_duplicate_records(
        orders,
        subset=["order_id"]
    )

    print("\nDuplicate orders:")
    print(duplicate_orders)

    check_data_types(orders)

    invalid_dates = find_invalid_dates(
        orders,
        "order_date"
    )

    print("\nOrders containing invalid dates:")
    print(invalid_dates)

    negative_quantity_orders = find_negative_quantity_records(
        orders
    )

    print("\nOrders with negative quantity:")
    print(negative_quantity_orders)

    negative_price_orders = find_negative_price_records(
        orders
    )

    print("\nOrders with negative price:")
    print(negative_price_orders)

    unknown_customer_orders = find_unknown_customer_records(
        orders,
        customers
    )

    print("\nOrders with unknown customer IDs:")
    print(unknown_customer_orders)

    unknown_product_orders = find_unknown_product_records(
        orders,
        products
    )

    print("\nOrders with unknown product IDs:")
    print(unknown_product_orders)

    # -------------------------------------------------
    # Final validation
    # -------------------------------------------------

    valid_orders, rejected_orders = validate_orders(
        orders,
        customers,
        products
    )

    print("\n==============================")
    print("FINAL VALIDATION RESULT")
    print("==============================")

    print("\nTotal orders:", len(orders))
    print("Valid orders:", len(valid_orders))
    print("Rejected orders:", len(rejected_orders))

    print("\nRejected Orders:")
    print(rejected_orders)

    print("\nValid Orders:")
    print(valid_orders)
