"""Fonte e arquivos esperados do conjunto público de dados Olist."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "source"
DB_PATH = ROOT / "data" / "olist.duckdb"
MARTS_DIR = ROOT / "sql" / "marts"
REPORT_PATH = ROOT / "reports" / "resultado_execucao.md"

BASE_URL = "https://raw.githubusercontent.com/ckoliveiraa/pipeline-olist/main/raw"
ARQUIVOS = {
    "orders": "olist_orders_dataset.csv.gz",
    "customers": "olist_customers_dataset.csv.gz",
    "items": "olist_order_items_dataset.csv.gz",
    "reviews": "olist_order_reviews_dataset.csv.gz",
}
# Valores publicados pelo mantenedor da cópia de origem; servem para auditar
# o download integral. Não são metas de indicadores de negócio.
CONTAGENS_REFERENCIA = {"orders": 99441, "customers": 99441, "items": 112650, "reviews": 99224}
