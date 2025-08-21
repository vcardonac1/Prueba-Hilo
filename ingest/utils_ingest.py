import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Normalizar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    
    # 2. Quitar duplicados
    df = df.drop_duplicates()
    
    # 3. Convertir columnas con "date" en datetime
    for col in df.columns:
        if "date" in col:
            try:
                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce",   # si no se puede parsear → NaT
                )
            except Exception as e:
                print(f"⚠️ No se pudo convertir {col} a fecha: {e}")

    # 4. Manejar decimales con coma → convertir a punto
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(",", ".", regex=False)
            # Intentar convertir a número
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass
    
    # 5. Manejar nulos
    df = df.fillna("NA")
    
    return df
