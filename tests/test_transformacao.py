def test_dedup_e_chave_unica(refined):
    assert refined.execute('SELECT COUNT(*) FROM refined.orders').fetchone()[0] == 3
    assert refined.execute('SELECT COUNT(*) FROM refined.order_analysis').fetchone()[0] == 3
    assert refined.execute('SELECT COUNT(DISTINCT order_id) FROM refined.order_analysis').fetchone()[0] == 3


def test_atraso_apenas_entregues(refined):
    linhas = dict(refined.execute('SELECT order_id, is_late FROM refined.orders').fetchall())
    assert linhas['O1'] is True
    assert linhas['O2'] is False
    assert linhas['O3'] is None


def test_frete_agrupado_sem_multiplicar_com_review(refined):
    linha = refined.execute("""SELECT item_count, total_items_value, total_freight_value
                             FROM refined.order_analysis WHERE order_id='O1'""").fetchone()
    assert linha == (2, 150, 15)


def test_review_mais_recente_e_nota_invalida(refined):
    assert refined.execute("SELECT review_score FROM refined.reviews WHERE order_id='O1'").fetchone()[0] == 2
    assert refined.execute("SELECT review_score FROM refined.reviews WHERE order_id='O3'").fetchone()[0] is None


def test_uf_normalizada(refined):
    assert refined.execute("SELECT customer_state FROM refined.customers WHERE customer_id='C1'").fetchone()[0] == 'SP'
