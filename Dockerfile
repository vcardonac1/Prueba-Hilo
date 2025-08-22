# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Evita bytecode y habilita logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

WORKDIR /app

# Dependencias del sistema (scikit-learn necesita libgomp1)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo requirements primero (mejor cache)
COPY ingest/requirements.txt ingest/requirements.txt
COPY model/requirements.txt model/requirements.txt
COPY analytics/requirements.txt analytics/requirements.txt

# Instalación por etapas (si comparten libs, pip resolverá)
RUN pip install --upgrade pip \
 && pip install -r ingest/requirements.txt \
 && pip install -r model/requirements.txt \
 && pip install -r analytics/requirements.txt

# Copiamos el resto del código
COPY . .

# Creamos carpetas de salida por si no existen
RUN mkdir -p data/raw data/processed data/model analytics/outputs report/figures

# Script por defecto (puedes sobrescribir con docker run/compose)
CMD ["/bin/bash"]

