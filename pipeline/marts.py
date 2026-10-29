"""Executa 5 consultas SQL de indicadores, uma tabela por pergunta."""
from pathlib import Path
import duckdb

REQUERIDAS = ["orders", "customers", "items", "reviews", "order_analysis"]


def construir_marts(con: duckdb.DuckDBPyConnection, pasta_sql: Path) -> dict[str, int]:
    existentes = {x[0] for x in con.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'refined'
    """).fetchall()}
    faltantes = set(REQUERIDAS) - existentes
    if faltantes:
        raise ValueError(f"Execute a transformação antes dos marts: {sorted(faltantes)}")
    arquivos = sorted(pasta_sql.glob("*.sql"))
    if len(arquivos) < 5:
        raise ValueError("O projeto exige os cinco arquivos SQL em sql/marts/")
    con.execute("CREATE SCHEMA IF NOT EXISTS marts")
    saida = {}
    for arq in arquivos:
        nome = arq.stem
        sql = arq.read_text(encoding="utf-8").strip().rstrip(";")
        con.execute(f"CREATE OR REPLACE TABLE marts.{nome} AS {sql}")
        n = con.execute(f"SELECT COUNT(*) FROM marts.{nome}").fetchone()[0]
        saida[nome] = n
        print(f"[MARTS] {nome}: {n:,} linhas")
    return saida
