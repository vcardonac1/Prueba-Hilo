#!/usr/bin/env bash
set -euo pipefail

echo "📁 Preparando directorios…"
mkdir -p data/raw data/processed data/model analytics/outputs report/figures report/tables

echo "▶️  1/3 Ingesta"
cd ingest
python ingest_data.py
cd ..

echo "▶️  2/3 Modelo estrella"
cd model
python build_star_schema.py
cd ..

echo "▶️  3/3 Analytics (PCA)"
cd analytics
python run_pca.py
cd ..

echo "🗂️  Copiando artefactos a /report"
# Copia figuras
if [ -f analytics/outputs/pca_variance.png ]; then
  cp analytics/outputs/pca_variance.png report/figures/
fi
if [ -f analytics/outputs/pca_loadings_heatmap.png ]; then
  cp analytics/outputs/pca_loadings_heatmap.png report/figures/
fi

echo "✅ Pipeline completado."
echo "   - Datos procesados:        data/processed/"
echo "   - Modelo estrella:         data/model/"
echo "   - Resultados PCA:          analytics/outputs/"
echo "   - Report (figures/tables): report/"
