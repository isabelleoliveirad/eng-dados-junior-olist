"""Download e carga RAW. Não edita os arquivos CSV de origem."""
import gzip
import hashlib
from pathlib import Path

import duckdb
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pipeline.config import ARQUIVOS, BASE_URL


def baixar_fontes(destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    sessao = requests.Session()
    sessao.mount("https://", HTTPAdapter(max_retries=Retry(
        total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
    )))
    for arquivo in ARQUIVOS.values():
        caminho = destino / arquivo
        if caminho.is_file() and caminho.stat().st_size > 0:
            print(f"[DOWNLOAD] Já existe: {arquivo}")
            continue
        url = f"{BASE_URL}/{arquivo}"
        print(f"[DOWNLOAD] {url}")
        tmp = destino / (arquivo + ".parcial")
        try:
            with sessao.get(url, stream=True, timeout=90) as r:
                r.raise_for_status()
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            with gzip.open(tmp, "rb") as gz:
                if not gz.read(200):
                    raise ValueError(f"Arquivo vazio: {arquivo}")
            tmp.replace(caminho)
        finally:
            tmp.unlink(missing_ok=True)


def ingestir(con: duckdb.DuckDBPyConnection, origem: Path) -> dict[str, int]:
    """Importa CSVs como VARCHAR e devolve contagens; sem casts ou filtros."""
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    contagens = {}
    for tabela, filename in ARQUIVOS.items():
        arq = origem / filename
        if not arq.exists():
            raise FileNotFoundError(f"Fonte não encontrada: {arq}")
        # Nome da tabela é fixo no código; caminho escapa aspas simples SQL.
        caminho_sql = str(arq.resolve()).replace("'", "''")
        con.execute(f"""
            CREATE OR REPLACE TABLE raw.{tabela} AS
            SELECT * FROM read_csv('{caminho_sql}',
                                   header=true, all_varchar=true)
        """)
        contagens[tabela] = con.execute(f"SELECT COUNT(*) FROM raw.{tabela}").fetchone()[0]
        print(f"[RAW] {tabela}: {contagens[tabela]:,} linhas (VARCHAR)")
    return contagens


def sha256(arquivo: Path) -> str:
    h = hashlib.sha256()
    with arquivo.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
