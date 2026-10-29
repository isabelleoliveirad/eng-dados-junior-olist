"""Ponto de entrada: download -> RAW -> REFINED -> MARTS -> qualidade."""
import argparse
from pathlib import Path

import duckdb

from pipeline.config import (ARQUIVOS, CONTAGENS_REFERENCIA, DATA_DIR,
                             DB_PATH, MARTS_DIR, REPORT_PATH)
from pipeline.ingestao import baixar_fontes, ingestir, sha256
from pipeline.marts import construir_marts
from pipeline.qualidade import verificar_qualidade
from pipeline.transformacao import transformar


def montar_relatorio(contagens_raw, contagens_refined, marts, qualidade, origem):
    linhas = [
        "# Resultado da execução do pipeline Olist", "",
        "> Gerado pela execução real do pipeline; não contém números inventados.", "",
        "## RAW: conferência dos dados originais", "",
        "| Fonte | Linhas carregadas | Referência do curso | Conferência | SHA-256 do arquivo |",
        "|---|---:|---:|---|---|",
    ]
    for tabela, nome_arq in ARQUIVOS.items():
        obtida = contagens_raw[tabela]
        esperada = CONTAGENS_REFERENCIA[tabela]
        status = "OK" if obtida == esperada else "DIVERGENTE: conferir origem"
        linhas.append(f"| {tabela} | {obtida} | {esperada} | {status} | `{sha256(origem / nome_arq)}` |")
    linhas += ["", "## REFINED: contagem após transformação", "",
              "| Tabela | Linhas |", "|---|---:|"]
    linhas += [f"| {t} | {n} |" for t, n in contagens_refined.items()]
    linhas += ["", "## MARTS: indicadores gerados", "", "| Mart | Linhas |", "|---|---:|"]
    linhas += [f"| {t} | {n} |" for t, n in marts.items()]
    linhas += ["", "## Qualidade de dados", "", "| Regra | Violações | Resultado |",
              "|---|---:|---|"]
    linhas += [f"| {t} | {n} | {'APROVADO' if n == 0 else 'REPROVADO'} |"
               for t, n in qualidade.items()]
    linhas += ["", "## Reconciliação", "",
              "Os totais de entregas analisadas e atrasos dos marts por UF e por mês "
              "são comparados entre si e diretamente à camada REFINED, sem valores fixos.", ""]
    return "\n".join(linhas)


def executar(origem: Path = DATA_DIR, banco: Path = DB_PATH,
             baixar: bool = True, relatorio: Path = REPORT_PATH) -> dict[str, int]:
    if baixar:
        baixar_fontes(origem)
    banco.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(banco))
    try:
        raw = ingestir(con, origem)
        refined = transformar(con)
        marts = construir_marts(con, MARTS_DIR)
        regras = verificar_qualidade(con)
        relatorio.parent.mkdir(parents=True, exist_ok=True)
        relatorio.write_text(montar_relatorio(raw, refined, marts, regras, origem),
                            encoding="utf-8")
        print(f"[RELATÓRIO] {relatorio}")
        if any(regras.values()):
            raise RuntimeError("Regras de qualidade falharam. Confira o relatório.")
        return regras
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser(description="Pipeline Olist: dados -> indicadores")
    parser.add_argument("--sem-download", action="store_true",
                        help="Usa fontes .csv.gz já existentes em data/source")
    args = parser.parse_args()
    executar(baixar=not args.sem_download)


if __name__ == "__main__":
    main()
