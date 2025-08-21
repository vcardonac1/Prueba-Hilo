import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from utils_analytics import join_datasets

# Directorios
MODEL_DIR = "../data/model"
OUTPUT_DIR = "./outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    # --- 1. Cargar modelo estrella ---
    fact_sales = pd.read_parquet(os.path.join(MODEL_DIR, "fact_sales.parquet"))
    dim_employees = pd.read_parquet(os.path.join(MODEL_DIR, "dim_employees.parquet"))
    dim_products = pd.read_parquet(os.path.join(MODEL_DIR, "dim_products.parquet"))
    dim_warehouses = pd.read_parquet(os.path.join(MODEL_DIR, "dim_warehouses.parquet"))

    # --- 2. Crear dataset de features ---
    features_df = join_datasets(fact_sales, dim_employees, dim_products, dim_warehouses)
    features_df = features_df.fillna(0)

    # --- 3. Escalar datos ---
    numeric_cols = features_df.select_dtypes(include="number").columns
    X = features_df[numeric_cols]
    X_scaled = StandardScaler().fit_transform(X)

    # --- 4. PCA ---
    pca = PCA(n_components=5)
    components = pca.fit_transform(X_scaled)
    explained_var = pca.explained_variance_ratio_

    # --- 5. Guardar componentes ---
    comp_df = pd.DataFrame(
        components,
        columns=[f"PC{i+1}" for i in range(components.shape[1])]
    )
    comp_df.to_parquet(os.path.join(OUTPUT_DIR, "pca_components.parquet"), index=False)

    # --- 6. Gráfico de varianza explicada ---
    plt.figure(figsize=(8,5))
    plt.plot(range(1, len(explained_var)+1), explained_var.cumsum(), marker="o")
    plt.title("Varianza explicada acumulada")
    plt.xlabel("Número de componentes principales")
    plt.ylabel("Varianza explicada acumulada")
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, "pca_variance.png"))

    # --- 7. Heatmap de correlaciones (loadings) ---
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f"PC{i+1}" for i in range(pca.n_components_)],
        index=numeric_cols
    )

    plt.figure(figsize=(10,8))
    sns.heatmap(loadings, annot=True, cmap="coolwarm", center=0)
    plt.title("Matriz de cargas PCA (loadings)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "pca_loadings_heatmap.png"))

    # Guardar también en tabla
    loadings.to_csv(os.path.join(OUTPUT_DIR, "pca_loadings.csv"))

    print("✅ PCA ejecutado. Resultados en /analytics/outputs")

if __name__ == "__main__":
    main()
