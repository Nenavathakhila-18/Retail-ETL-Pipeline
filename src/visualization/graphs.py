import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path("output")
GRAPH_DIR = OUTPUT_DIR / "graphs"

GRAPH_DIR.mkdir(parents=True, exist_ok=True)


def create_graphs():
    print("\n[6] VISUALIZATION")

    # --------------------------------------------------
    # 1. Daily Sales Trend
    # --------------------------------------------------
    daily_sales = pd.read_csv(OUTPUT_DIR / "daily_sales.csv")

    # Automatically identify date and sales columns
    date_col = daily_sales.columns[0]
    sales_col = daily_sales.columns[-1]

    plt.figure(figsize=(10, 5))
    plt.plot(
        daily_sales[date_col],
        daily_sales[sales_col],
        marker="o"
    )
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "daily_sales.png")
    plt.close()

    # --------------------------------------------------
    # 2. Category Sales
    # --------------------------------------------------
    category = pd.read_csv(OUTPUT_DIR / "category_summary.csv")

    category_col = category.columns[0]
    category_sales_col = category.columns[-1]

    plt.figure(figsize=(9, 5))
    plt.bar(
        category[category_col],
        category[category_sales_col]
    )
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "category_sales.png")
    plt.close()

    # --------------------------------------------------
    # 3. City Sales
    # --------------------------------------------------
    city = pd.read_csv(OUTPUT_DIR / "city_summary.csv")

    city_col = city.columns[0]
    city_sales_col = city.columns[-1]

    plt.figure(figsize=(10, 5))
    plt.bar(
        city[city_col],
        city[city_sales_col]
    )
    plt.title("Sales by City")
    plt.xlabel("City")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "city_sales.png")
    plt.close()

    # --------------------------------------------------
    # 4. Product Sales
    # --------------------------------------------------
    product = pd.read_csv(OUTPUT_DIR / "product_summary.csv")

    product_col = product.columns[0]
    product_sales_col = product.columns[-1]

    plt.figure(figsize=(10, 5))
    plt.bar(
        product[product_col],
        product[product_sales_col]
    )
    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "product_sales.png")
    plt.close()

    # --------------------------------------------------
    # 5. Customer Sales
    # --------------------------------------------------
    customer = pd.read_csv(OUTPUT_DIR / "customer_summary.csv")

    customer_col = customer.columns[0]
    customer_sales_col = customer.columns[-1]

    plt.figure(figsize=(10, 5))
    plt.bar(
        customer[customer_col],
        customer[customer_sales_col]
    )
    plt.title("Sales by Customer")
    plt.xlabel("Customer")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "customer_sales.png")
    plt.close()

    print("Graphs generated successfully.")