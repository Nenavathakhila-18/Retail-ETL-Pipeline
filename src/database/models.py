"""
SQLAlchemy ORM models for the retail ETL pipeline.

Mirrors the retail data model (customers, products, orders) as
proper relational tables with primary/foreign keys and relationships,
instead of the flat pandas DataFrames used by the CSV-based stages.
"""

from datetime import date

from sqlalchemy import String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from src.database.db import engine


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer {self.customer_id}: {self.customer_name} ({self.city})>"


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"<Product {self.product_id}: {self.product_name} ({self.category})>"


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    customer_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("customers.customer_id"), nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("products.product_id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    sales_amount: Mapped[float] = mapped_column(Float, nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order {self.order_id}: qty={self.quantity} amount={self.sales_amount}>"


def create_tables():
    """Create all ORM-backed tables if they do not already exist."""
    Base.metadata.create_all(engine)
