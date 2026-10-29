from pipeline.ingestao import ingestir, sha256


def test_raw_preserva_linhas_e_tipos(pasta_ficticia):
    import duckdb
    con = duckdb.connect(":memory:")
    contagens = ingestir(con, pasta_ficticia)
    assert contagens == {"orders": 4, "customers": 3, "items": 4, "reviews": 4}
    campos = con.execute("DESCRIBE raw.orders").fetchall()
    assert all(campo[1] == "VARCHAR" for campo in campos)
    assert con.execute("SELECT COUNT(*) FROM raw.orders WHERE order_id='O1'").fetchone()[0] == 2
    con.close()


def test_sha256_tem_64_digitos(pasta_ficticia):
    assert len(sha256(pasta_ficticia / 'olist_orders_dataset.csv.gz')) == 64
