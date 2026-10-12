"""
Database engine and session setup for the retail ETL pipeline.

Follows the same engine / sessionmaker pattern as the sql_orm
reference project, but defaults to a local SQLite file so the
pipeline runs out of the box with no external database required.

To point the pipeline at MySQL/Postgres instead, just change
DATABASE_URL (e.g. "mysql+pymysql://user:password@localhost:3306/retail_etl").
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import BASE_DIR

DATABASE_URL = "mysql+pymysql://root:akhila%40180305@localhost:3306/retail_etl"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)