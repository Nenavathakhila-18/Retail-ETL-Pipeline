import pandas as pd

from src.transform.transform import transform_orders


def test_transform_orders():

    orders = pd.DataFrame({
        "order_id": [1001, 1002],
        "order_date": [
            "2026-09-01",
            "2026-09-02"
        ],
        "customer_id": [
            "C001",
            "C002"
        ],
        "product_id": [
            "P001",
            "P002"
        ],
        "quantity": [
            2,
            3
        ],
        "price": [
            50000,
            700
        ]
    })

    customers = pd.DataFrame({
        "customer_id": [
            "C001",
            "C002"
        ],
        "customer_name": [
            "Amulya",
            "Rahul"
        ],
        "city": [
            "Hyderabad",
            "Chennai"
        ]
    })

    products = pd.DataFrame({
        "product_id": [
            "P001",
            "P002"
        ],
        "product_name": [
            "Laptop",
            "Mouse"
        ],
        "category": [
            "Electronics",
            "Accessories"
        ]
    })

    result = transform_orders(
        orders,
        customers,
        products
    )

    # Check number of rows
    assert len(result) == 2

    # Check customer information
    assert result.iloc[0]["customer_name"] == "Amulya"
    assert result.iloc[0]["city"] == "Hyderabad"

    # Check product information
    assert result.iloc[0]["product_name"] == "Laptop"
    assert result.iloc[0]["category"] == "Electronics"

    # Check sales calculation
    assert result.iloc[0]["sales_amount"] == 100000
    assert result.iloc[1]["sales_amount"] == 2100

    # Check date conversion
    assert pd.api.types.is_datetime64_any_dtype(
        result["order_date"]
    )

    # Check expected columns
    expected_columns = [
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

    assert list(result.columns) == expected_columns
