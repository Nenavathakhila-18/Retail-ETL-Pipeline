import pandas as pd

from src.reports.reports import (
    create_customer_summary,
    create_product_summary,
    create_city_summary,
    create_category_summary,
    create_daily_sales
)


def create_test_data():
    """
    Create sample transformed order data
    for testing report functions.
    """

    return pd.DataFrame({
        "order_id": [1001, 1002, 1003],
        "order_date": pd.to_datetime([
            "2026-09-01",
            "2026-09-01",
            "2026-09-02"
        ]),
        "customer_id": [
            "C001",
            "C002",
            "C001"
        ],
        "customer_name": [
            "Amulya",
            "Rahul",
            "Amulya"
        ],
        "city": [
            "Hyderabad",
            "Chennai",
            "Hyderabad"
        ],
        "product_id": [
            "P001",
            "P002",
            "P001"
        ],
        "product_name": [
            "Laptop",
            "Mouse",
            "Laptop"
        ],
        "category": [
            "Electronics",
            "Accessories",
            "Electronics"
        ],
        "quantity": [
            2,
            3,
            1
        ],
        "price": [
            50000,
            700,
            50000
        ],
        "sales_amount": [
            100000,
            2100,
            50000
        ]
    })


def test_customer_summary():

    df = create_test_data()

    result = create_customer_summary(df)

    assert len(result) == 2

    amulya = result[
        result["customer_id"] == "C001"
    ].iloc[0]

    assert amulya["total_orders"] == 2
    assert amulya["total_sales"] == 150000


def test_product_summary():

    df = create_test_data()

    result = create_product_summary(df)

    assert len(result) == 2

    laptop = result[
        result["product_id"] == "P001"
    ].iloc[0]

    assert laptop["total_quantity"] == 3
    assert laptop["total_sales"] == 150000


def test_city_summary():

    df = create_test_data()

    result = create_city_summary(df)

    assert len(result) == 2

    hyderabad = result[
        result["city"] == "Hyderabad"
    ].iloc[0]

    assert hyderabad["total_orders"] == 2
    assert hyderabad["total_sales"] == 150000


def test_category_summary():

    df = create_test_data()

    result = create_category_summary(df)

    assert len(result) == 2

    electronics = result[
        result["category"] == "Electronics"
    ].iloc[0]

    assert electronics["total_quantity"] == 3
    assert electronics["total_sales"] == 150000


def test_daily_sales():

    df = create_test_data()

    result = create_daily_sales(df)

    assert len(result) == 2

    first_day = result[
        result["order_date"]
        == pd.Timestamp("2026-09-01")
    ].iloc[0]

    assert first_day["total_orders"] == 2
    assert first_day["total_sales"] == 102100
