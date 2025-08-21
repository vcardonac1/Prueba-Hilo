import pandas as pd

def build_date_dim(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Construye una tabla de dimensión de fechas.
    """
    dates = pd.to_datetime(df[date_col].dropna().unique())
    dim_date = pd.DataFrame({"date": dates})
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["weekday"] = dim_date["date"].dt.weekday
    dim_date["weekday_name"] = dim_date["date"].dt.day_name()
    return dim_date.sort_values("date").reset_index(drop=True)
