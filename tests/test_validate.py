import pandas as pd

from src.validate.validate import (
    find_null_records,
    find_duplicate_records,
    find_invalid_dates,
    find_negative_quantity_records,
    find_negative_price_records,
    find_unknown_customer_records,
    find_unknown_product_records,
    validate_orders
)


def test_find_null_records():

    df = pd.DataFrame({
        "order_id": [1001, 1002],
        "quantity": [2, None]
    })

    result = find_null_records(df)

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 1002


def test_find_duplicate_records():

    df = pd.DataFrame({
        "order_id": [1001, 1002, 1002]
    })

    result = find_duplicate_records(
        df,
        subset=["order_id"]
    )

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 1002


def test_find_invalid_dates():

    df = pd.DataFrame({
        "order_date": [
            "2026-09-01",
            "invalid-date"
        ]
    })

    result = find_invalid_dates(
        df,
        "order_date"
    )

    assert len(result) == 1


def test_find_negative_quantity_records():

    df = pd.DataFrame({
        "quantity": [2, -1, 3]
    })

    result = find_negative_quantity_records(df)

    assert len(result) == 1
    assert result.iloc[0]["quantity"] == -1


def test_find_negative_price_records():

    df = pd.DataFrame({
        "price": [500, -100, 1000]
    })

    result = find_negative_price_records(df)

    assert len(result) == 1
    assert result.iloc[0]["price"] == -100


def test_find_unknown_customer_records():

    orders = pd.DataFrame({
        "customer_id": ["C001", "C999"]
    })

    customers = pd.DataFrame({
        "customer_id": ["C001", "C002"]
    })

    result = find_unknown_customer_records(
        orders,
        customers
    )

    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == "C999"


def test_find_unknown_product_records():

    orders = pd.DataFrame({
        "product_id": ["P001", "P999"]
    })

    products = pd.DataFrame({
        "product_id": ["P001", "P002"]
    })

    result = find_unknown_product_records(
        orders,
        products
    )

    assert len(result) == 1
    assert result.iloc[0]["product_id"] == "P999"


def test_validate_orders():

    customers = pd.DataFrame({
        "customer_id": ["C001"]
    })

    products = pd.DataFrame({
        "product_id": ["P001"]
    })

    orders = pd.DataFrame({
        "order_id": [1001, 1002, 1003],
        "order_date": [
            "2026-09-01",
            "2026-09-01",
            "invalid-date"
        ],
        "customer_id": [
            "C001",
            "C001",
            "C001"
        ],
        "product_id": [
            "P001",
            "P001",
            "P001"
        ],
        "quantity": [
            2,
            -1,
            1
        ],
        "price": [
            500,
            500,
            500
        ]
    })

    valid_orders, rejected_orders = validate_orders(
        orders,
        customers,
        products
    )

    assert len(valid_orders) == 1
    assert len(rejected_orders) == 2
