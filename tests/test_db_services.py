import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import src.database.db as db
from src.database import models
import src.database.db_services as db_services

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.extract.extract import extract_data
from src.validate.validate import validate_orders
from src.transform.transform import transform_orders


def _use_in_memory_db(monkeypatch):
    """Point db.SessionLocal / models at a throwaway in-memory SQLite DB."""

    test_engine = create_engine("sqlite:///:memory:")
    test_session = sessionmaker(bind=test_engine, expire_on_commit=False)

    monkeypatch.setattr(db, "engine", test_engine)
    monkeypatch.setattr(db, "SessionLocal", test_session)
    monkeypatch.setattr(models, "engine", test_engine)
    monkeypatch.setattr(db_services, "SessionLocal", test_session)

    return test_engine


def test_load_and_report_round_trip(monkeypatch):
    _use_in_memory_db(monkeypatch)

    customers, products, orders = extract_data()
    valid_orders, _ = validate_orders(orders, customers, products)
    transformed_orders = transform_orders(valid_orders, customers, products)

    db_services.load_transformed_data(customers, products, transformed_orders)

    customer_summary = db_services.get_customer_summary()
    product_summary = db_services.get_product_summary()

    assert len(customer_summary) > 0
    assert len(product_summary) > 0

    total_sales_from_db = sum(row.total_sales for row in customer_summary)
    total_sales_from_df = transformed_orders["sales_amount"].sum()

    assert round(total_sales_from_db, 2) == round(total_sales_from_df, 2)
