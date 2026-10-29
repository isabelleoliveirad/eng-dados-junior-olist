# Engenharia de Dados Júnior | Olist: atrasos, frete e satisfação

Pipeline autoral com **Python + DuckDB + SQL + Pytest**, executável no Google Colab.
Analisa a relação descritiva entre atrasos de entregas, valor do frete e avaliações de consumidores brasileiros.

## Origem dos dados e direitos de uso

Dados Olist (*Brazilian E-Commerce Public Dataset*, via Kaggle), disponibilizados em `.csv.gz` no [repositório do curso](https://github.com/ckoliveiraa/pipeline-olist/tree/main/raw).
Licença informada pela fonte: **CC BY-NC-SA 4.0**, com atribuição e uso não comercial. Dados pertencem aos titulares originais. Não são copiados neste repositório: o programa os baixa para uso local.
Veja também: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Arquivos utilizados: `olist_orders_dataset.csv.gz`, `olist_customers_dataset.csv.gz`, `olist_order_items_dataset.csv.gz`, `olist_order_reviews_dataset.csv.gz`.

## Perguntas de negócio (originais, diferentes das do curso)

1. Quais UFs têm mais atrasos proporcionais? `marts.entregas_por_estado`, grão UF.
2. Qual a evolução mensal do percentual de atrasos? `marts.entregas_por_mes`, grão mês da compra.
3. Há associação entre atraso e avaliações baixas? `marts.avaliacoes_por_atraso`, grão status de atraso.
4. Qual a participação do custo do frete no valor dos itens por UF? `marts.frete_por_estado`, grão UF.
5. Quais UFs (com pelo menos 30 entregas) têm as maiores taxas de atraso? `marts.ranking_estados`, grão UF, CTE e função de janela.

**Cuidado:** associação não indica causalidade; valores de itens não são receita nem lucro.

## Arquitetura

```text
Olist .csv.gz -> data/source/ (imutável) -> DuckDB raw (VARCHAR)
  -> refined (tipos, chave única, relações por pedido)
  -> marts (cinco consultas SQL)
  -> regras de qualidade e reports/resultado_execucao.md
```

Os dados de origem não são versionados aqui. O pipeline recria todas as tabelas do banco local ao executar, sem modificar os arquivos `.csv.gz`.

## Executar no Google Colab ou localmente

```bash
python -m pip install -r requirements.txt
python -m pytest -q --cov=pipeline --cov-report=term-missing --cov-fail-under=60
python -m pipeline.executar
```

A execução baixa cerca de quatro CSVs comprimidos, cria `data/olist.duckdb` e grava o relatório `reports/resultado_execucao.md`. Requer internet somente na ingestão inicial; pode ser repetida com `python -m pipeline.executar --sem-download`.

## Testes e validação

Os testes usam **dados fictícios** e conexões DuckDB **em memória**, sem abrir o banco real nem baixar a Olist. Exercitam integridade RAW, deduplicação, tipagem, atraso, reviews, marts e detecção de inconsistências.

Três regras SQL de qualidade são executadas sobre a base real:
- **Chave única:** nenhuma repetição de `order_id` em `refined.order_analysis`.
- **Domínio:** notas de avaliação somente entre 1 e 5 (quando presentes).
- **Reconciliação:** contagem de entregas e atrasos em `marts.entregas_por_estado` coincide com `marts.entregas_por_mes`; o total de entregas ainda é comparado à `refined.order_analysis`.

**Resultados reais:** executar o pipeline e consultar [`reports/resultado_execucao.md`](reports/resultado_execucao.md). Não inventamos resultados: o arquivo inicial é apenas um marcador e será substituído na execução.

## Uso de IA e autoria

IA auxiliou na estruturação, revisão de SQL e elaboração de testes. As perguntas, as decisões explícitas de escopo e grão, as escolhas de critérios de atraso e o histórico de execução devem ser lidos e validados pela responsável pela entrega. Não houve cópia do pipeline implementado em aula. Registros de decisões em `specs/transformacao.md`.

## Commits incrementais

O guia `GUIA_GITHUB.md` explica como fazer um commit real por etapa. **Não envie tudo em um commit**. Primeiro faça o pipeline funcionar, confira as saídas, e então registre as etapas conforme as construir em seu repositório.
