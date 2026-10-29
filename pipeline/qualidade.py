"""Regras de qualidade no banco: zero violações significa APROVADO."""
import duckdb

REGRAS = {
    "unicidade_pedidos": """
        SELECT COUNT(*) FROM (
            SELECT order_id FROM refined.order_analysis
            GROUP BY order_id HAVING COUNT(*) <> 1
        ) t
    """,
    "dominio_avaliacoes": """
        SELECT COUNT(*) FROM refined.reviews
        WHERE review_score IS NOT NULL AND review_score NOT BETWEEN 1 AND 5
    """,
    "reconciliacao_estados_meses": """
        SELECT CASE WHEN
            (SELECT COALESCE(SUM(entregas_analisadas), 0) FROM marts.entregas_por_estado)
             =
            (SELECT COALESCE(SUM(entregas_analisadas), 0) FROM marts.entregas_por_mes)
           AND
            (SELECT COALESCE(SUM(entregas_atrasadas), 0) FROM marts.entregas_por_estado)
             =
            (SELECT COALESCE(SUM(entregas_atrasadas), 0) FROM marts.entregas_por_mes)
           AND
            (SELECT COUNT(*) FROM refined.order_analysis
             WHERE order_status = 'delivered' AND is_late IS NOT NULL)
             =
            (SELECT COALESCE(SUM(entregas_analisadas), 0) FROM marts.entregas_por_estado)
        THEN 0 ELSE 1 END
    """,
}


def verificar_qualidade(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    resultados = {}
    for nome, sql in REGRAS.items():
        falhas = con.execute(sql).fetchone()[0]
        resultados[nome] = int(falhas)
        print(f"[QUALIDADE] {nome}: {'OK' if falhas == 0 else 'FALHOU'} ({falhas} violações)")
    return resultados
