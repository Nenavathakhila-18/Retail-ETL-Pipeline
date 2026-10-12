"""
ORM-based data access layer for the retail ETL pipeline.

This is the "SQL ORM" equivalent of load.py / reports.py: instead of
reading/writing CSVs and computing summaries with pandas.groupby, it
persists rows through SQLAlchemy models (models.py) and can compute
the same summaries with ORM queries.

Two responsibilities:

1. Loading      -> upsert_customers / upsert_products / upsert_orders
2. Reporting    -> get_customer_summary / get_product_summary / ...
"""

import logging

from sqlalchemy import select, func

from src.database.db import SessionLocal
from src.database.models import Customer, Product, Order, create_tables

logger = logging.getLogger(__name__)


# -------------------------------------------------
# LOADING (upsert from pandas DataFrames)
# -------------------------------------------------

def upsert_customers(customers_df):
    """Insert or update customer rows from the customers DataFrame."""

    with SessionLocal() as session:
        for row in customers_df.itertuples(index=False):
            customer = session.get(Customer, row.customer_id)

            if customer is None:
                customer = Customer(
                    customer_id=row.customer_id,
                    customer_name=row.customer_name,
                    city=row.city,
                )
                session.add(customer)
            else:
                customer.customer_name = row.customer_name
                customer.city = row.city

        session.commit()

    logger.info("Upserted %d customers into the database", len(customers_df))


def upsert_products(products_df):
    """Insert or update product rows from the products DataFrame."""

    with SessionLocal() as session:
        for row in products_df.itertuples(index=False):
            product = session.get(Product, row.product_id)

            if product is None:
                product = Product(
                    product_id=row.product_id,
                    product_name=row.product_name,
                    category=row.category,
                )
                session.add(product)
            else:
                product.product_name = row.product_name
                product.category = row.category

        session.commit()

    logger.info("Upserted %d products into the database", len(products_df))


def upsert_orders(transformed_orders_df):
    """
    Insert or update order rows from the transformed orders DataFrame.

    Expects the same columns produced by transform.transform_orders():
    order_id, order_date, customer_id, product_id, quantity, price,
    sales_amount (customer_name / product_name / category are ignored
    here since they live on the related Customer/Product rows).
    """

    with SessionLocal() as session:
        for row in transformed_orders_df.itertuples(index=False):
            order = session.get(Order, row.order_id)

            order_date = row.order_date
            if hasattr(order_date, "date"):
                order_date = order_date.date()

            if order is None:
                order = Order(
                    order_id=row.order_id,
                    order_date=order_date,
                    customer_id=row.customer_id,
                    product_id=row.product_id,
                    quantity=row.quantity,
                    price=row.price,
                    sales_amount=row.sales_amount,
                )
                session.add(order)
            else:
                order.order_date = order_date
                order.customer_id = row.customer_id
                order.product_id = row.product_id
                order.quantity = row.quantity
                order.price = row.price
                order.sales_amount = row.sales_amount

        session.commit()

    logger.info("Upserted %d orders into the database", len(transformed_orders_df))


def load_transformed_data(customers_df, products_df, transformed_orders_df):
    """
    Run the full ORM load step: create tables if needed, then upsert
    customers, products, and transformed orders in the correct order
    (dimensions first, so foreign keys resolve).
    """

    create_tables()

    upsert_customers(customers_df)
    upsert_products(products_df)
    upsert_orders(transformed_orders_df)


# -------------------------------------------------
# REPORTING (ORM queries, equivalent to reports.py)
# -------------------------------------------------

def get_customer_summary():
    """Total orders and total sales per customer, via ORM aggregation."""

    with SessionLocal() as session:
        stmt = (
            select(
                Customer.customer_id,
                Customer.customer_name,
                func.count(Order.order_id).label("total_orders"),
                func.sum(Order.sales_amount).label("total_sales"),
            )
            .join(Order, Order.customer_id == Customer.customer_id)
            .group_by(Customer.customer_id, Customer.customer_name)
        )

        return session.execute(stmt).all()


def get_product_summary():
    """Total quantity sold and total sales per product, via ORM aggregation."""

    with SessionLocal() as session:
        stmt = (
            select(
                Product.product_id,
                Product.product_name,
                func.sum(Order.quantity).label("total_quantity"),
                func.sum(Order.sales_amount).label("total_sales"),
            )
            .join(Order, Order.product_id == Product.product_id)
            .group_by(Product.product_id, Product.product_name)
        )

        return session.execute(stmt).all()


def get_city_summary():
    """Total orders and total sales per city, via ORM aggregation."""

    with SessionLocal() as session:
        stmt = (
            select(
                Customer.city,
                func.count(Order.order_id).label("total_orders"),
                func.sum(Order.sales_amount).label("total_sales"),
            )
            .join(Order, Order.customer_id == Customer.customer_id)
            .group_by(Customer.city)
        )

        return session.execute(stmt).all()


def get_category_summary():
    """Total quantity sold and total sales per category, via ORM aggregation."""

    with SessionLocal() as session:
        stmt = (
            select(
                Product.category,
                func.sum(Order.quantity).label("total_quantity"),
                func.sum(Order.sales_amount).label("total_sales"),
            )
            .join(Order, Order.product_id == Product.product_id)
            .group_by(Product.category)
        )

        return session.execute(stmt).all()


def get_daily_sales():
    """Total orders and total sales per day, via ORM aggregation."""

    with SessionLocal() as session:
        stmt = (
            select(
                Order.order_date,
                func.count(Order.order_id).label("total_orders"),
                func.sum(Order.sales_amount).label("total_sales"),
            )
            .group_by(Order.order_date)
            .order_by(Order.order_date)
        )

        return session.execute(stmt).all()
