"""Dados artificiais mínimos para testar o pipeline sem acessar a Olist real."""
import csv
import gzip
from pathlib import Path

import duckdb
import pytest

from pipeline.config import ARQUIVOS
from pipeline.ingestao import ingestir
from pipeline.transformacao import transformar

ROWS = {
    "orders": [
        ["order_id", "customer_id", "order_status", "order_purchase_timestamp",
         "order_delivered_customer_date", "order_estimated_delivery_date"],
        ["O1", "C1", "delivered", "2023-01-01", "2023-01-10", "2023-01-08"],
        ["O2", "C2", "delivered", "2023-01-02", "2023-01-05", "2023-01-07"],
        ["O3", "C3", "canceled", "2023-01-03", "", "2023-01-09"],
        ["O1", "C1", "delivered", "2023-01-01", "2023-01-10", "2023-01-08"],
    ],
    "customers": [
        ["customer_id", "customer_state", "customer_city"],
        ["C1", "sp", "Campinas"], ["C2", "RJ", "Rio de Janeiro"],
        ["C3", "SP", "Santos"],
    ],
    "items": [
        ["order_id", "order_item_id", "price", "freight_value"],
        ["O1", "1", "100.00", "10.00"], ["O1", "2", "50.00", "5.00"],
        ["O2", "1", "80.00", "8.00"], ["O3", "1", "20.00", "2.00"],
    ],
    "reviews": [
        ["review_id", "order_id", "review_score", "review_creation_date"],
        ["R1", "O1", "1", "2023-01-11"],
        ["R2", "O1", "2", "2023-01-12"],
        ["R3", "O2", "5", "2023-01-06"],
        ["R4", "O3", "x", "2023-01-06"],
    ],
}


@pytest.fixture
def pasta_ficticia(tmp_path: Path) -> Path:
    for tabela, conteudo in ROWS.items():
        with gzip.open(tmp_path / ARQUIVOS[tabela], "wt", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(conteudo)
    return tmp_path


@pytest.fixture
def raw(pasta_ficticia):
    con = duckdb.connect(":memory:")
    ingestir(con, pasta_ficticia)
    yield con
    con.close()


@pytest.fixture
def refined(raw):
    transformar(raw)
    return raw
