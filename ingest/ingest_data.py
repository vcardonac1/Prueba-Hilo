import os
import pandas as pd
from utils_ingest import clean_dataframe

# Directorios
RAW_DIR = "../data/raw"
PROCESSED_DIR = "../data/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Archivos Excel locales
files = [
    "sales_sample.xlsx",
    "inventory_sample.xlsx",
    "hr_sample.xlsx"
]

def process_excels():
    for fname in files:
        fpath = os.path.join(RAW_DIR, fname)
        if not os.path.exists(fpath):
            print(f"Archivo no encontrado: {fpath}")
            continue

        print(f"\nProcesando {fname} ...")

        # Leer todas las hojas del Excel
        sheets = pd.read_excel(fpath, sheet_name=None, dtype=str, engine="openpyxl")

        for sheet_name, df in sheets.items():
            print(f"   Hoja: {sheet_name}, filas: {len(df)}")

            df_clean = clean_dataframe(df)

            # Nombre de salida parquet
            out_name = f"{fname.replace('.xlsx','')}_{sheet_name}.parquet"
            out_path = os.path.join(PROCESSED_DIR, out_name)

            df_clean.to_parquet(out_path, index=False)
            print(f"   Guardado: {out_name}")

def main():
    process_excels()
    print("\nIngesta completada.")

if __name__ == "__main__":
    main()
