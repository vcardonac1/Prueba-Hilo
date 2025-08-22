import os
import pandas as pd
from utils_model import build_date_dim

# Directorios
PROCESSED_DIR = "../data/processed"
MODEL_DIR = "../data/model"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_tables():
    """Carga los .parquet de processed en dataframes."""
    tables = {}
    for f in os.listdir(PROCESSED_DIR):
        if f.endswith(".parquet"):
            name = f.replace(".parquet", "")
            tables[name] = pd.read_parquet(os.path.join(PROCESSED_DIR, f))
    return tables

def build_star_schema(tables):
    """Construye el esquema estrella a partir de las tablas de ingest."""
    # --- Dimensiones ---
    dim_customers = tables["sales_sample_Customers"].drop_duplicates().reset_index(drop=True)
    dim_products = tables["sales_sample_Products"].drop_duplicates().reset_index(drop=True)
    dim_stores = tables["sales_sample_Stores"].drop_duplicates().reset_index(drop=True)
    dim_employees = tables["hr_sample_Employee_Performance"].drop_duplicates().reset_index(drop=True)
    dim_departments = tables["hr_sample_Departments"].drop_duplicates().reset_index(drop=True)
    dim_warehouses = tables["inventory_sample_Warehouses"].drop_duplicates().reset_index(drop=True)
    dim_categories = tables["inventory_sample_Categories"].drop_duplicates().reset_index(drop=True)

    # --- Fact ventas ---
    fact_sales = tables["sales_sample_Sales_Transactions"].copy()

    # Normalizamos nombres de columnas
    fact_sales = fact_sales.rename(columns={
        "TransactionID": "sale_id",
        "TransactionDate": "sale_date",
        "ProductID": "product_id",
        "CustomerID": "customer_id",
        "StoreID": "store_id",
        "EmployeeID": "employee_id",
        "Quantity": "quantity",
        "UnitPrice": "unit_price",
        "DiscountPercent": "discount_percent"
    })

    # Calcular métricas
    fact_sales["sales_amount"] = fact_sales["quantity"] * fact_sales["unit_price"] * (1 - fact_sales["discount_percent"]/100)
    fact_sales["profit_margin"] = fact_sales["sales_amount"] * 0.2  # suposición de 20%

    # --- Dim fecha ---
    dim_date = build_date_dim(fact_sales, date_col="sale_date")

    # Guardar todo
    dim_customers.to_parquet(os.path.join(MODEL_DIR, "dim_customers.parquet"), index=False)
    dim_products.to_parquet(os.path.join(MODEL_DIR, "dim_products.parquet"), index=False)
    dim_stores.to_parquet(os.path.join(MODEL_DIR, "dim_stores.parquet"), index=False)
    dim_employees.to_parquet(os.path.join(MODEL_DIR, "dim_employees.parquet"), index=False)
    dim_departments.to_parquet(os.path.join(MODEL_DIR, "dim_departments.parquet"), index=False)
    dim_warehouses.to_parquet(os.path.join(MODEL_DIR, "dim_warehouses.parquet"), index=False)
    dim_categories.to_parquet(os.path.join(MODEL_DIR, "dim_categories.parquet"), index=False)
    dim_date.to_parquet(os.path.join(MODEL_DIR, "dim_date.parquet"), index=False)
    fact_sales.to_parquet(os.path.join(MODEL_DIR, "fact_sales.parquet"), index=False)

    print("Esquema estrella creado en /data/model")

def main():
    tables = load_tables()
    build_star_schema(tables)

if __name__ == "__main__":
    main()
