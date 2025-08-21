import pandas as pd

def join_datasets(fact_sales, dim_employees, dim_products, dim_warehouses):
    """
    Integra hechos de ventas con empleados, productos e inventarios.
    """
    df = fact_sales.copy()

    # Join con empleados (performance, salario, etc.)
    if "employee_id" in df.columns and "EmployeeID" in dim_employees.columns:
        df = df.merge(
            dim_employees,
            left_on="employee_id",
            right_on="EmployeeID",
            how="left"
        )

    # Join con productos (categorías, costos, etc.)
    if "product_id" in df.columns and "ProductID" in dim_products.columns:
        df = df.merge(
            dim_products,
            left_on="product_id",
            right_on="ProductID",
            how="left"
        )

    # Join con almacenes (stock, capacidad, etc.)
    if "store_id" in df.columns and "WarehouseID" in dim_warehouses.columns:
        df = df.merge(
            dim_warehouses,
            left_on="store_id",
            right_on="WarehouseID",
            how="left"
        )

    return df
