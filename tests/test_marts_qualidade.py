from pipeline.config import MARTS_DIR
from pipeline.marts import construir_marts
from pipeline.qualidade import verificar_qualidade


def test_cinco_marts_com_cte_e_janela(refined):
    saida = construir_marts(refined, MARTS_DIR)
    assert len(saida) == 5
    assert set(saida) == {
        'entregas_por_estado', 'entregas_por_mes', 'avaliacoes_por_atraso',
        'frete_por_estado', 'ranking_estados'
    }
    soma = refined.execute('SELECT SUM(entregas_analisadas) FROM marts.entregas_por_mes').fetchone()[0]
    assert soma == 2
    assert saida['ranking_estados'] == 0  # menos de 30 entregas por UF no dado inventado


def test_qualidade_sem_violações(refined):
    construir_marts(refined, MARTS_DIR)
    assert verificar_qualidade(refined) == {
        'unicidade_pedidos': 0,
        'dominio_avaliacoes': 0,
        'reconciliacao_estados_meses': 0,
    }


def test_qualidade_detecta_duplicata(refined):
    construir_marts(refined, MARTS_DIR)
    refined.execute("INSERT INTO refined.order_analysis SELECT * FROM refined.order_analysis WHERE order_id='O1'")
    assert verificar_qualidade(refined)['unicidade_pedidos'] == 1


def test_qualidade_detecta_desconciliacao(refined):
    construir_marts(refined, MARTS_DIR)
    refined.execute('DELETE FROM marts.entregas_por_mes')
    assert verificar_qualidade(refined)['reconciliacao_estados_meses'] == 1
