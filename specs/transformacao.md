# Especificação autoral de transformação Olist

## Pergunta central
Como atrasos e custo do frete se relacionam à experiência de compra em diferentes UFs?

## Sete decisões (antes do código)

1. **Escopo:** quatro tabelas de origem: pedidos, clientes, itens, avaliações. Não calcular pagamentos/receita.
2. **Nomes:** inglês no modelo técnico, português nas perguntas de negócio; `order_id` é a chave de pedido.
3. **Tipos:** RAW preserva todas as colunas como `VARCHAR`; REFINED faz `TRY_CAST` de datas, notas e dinheiro.
4. **Falha na conversão:** datas ou números inválidos viram `NULL`, sem inventar zero ou outra data.
5. **Duplicatas:** um pedido por `order_id`; um cliente por `customer_id`; um item por `(order_id,order_item_id)`; para avaliações múltiplas, escolher a de `review_creation_date` mais recente, com desempate por `review_id`.
6. **Nulos:** chave vazia é descartada da REFINED e continua preservada em RAW; pedido sem review permanece no universo; `is_late` só é definido para pedido entregue e com datas válidas. Os estados e meses nulos são mantidos nos agregados para reconciliação.
7. **Saída:** imprimir linhas antes/depois, gerar 5 marts e relatório com SHA-256 e três regras SQL.

## Granularidade e termos fechados
- **Pedido:** uma linha por `order_id` em `refined.order_analysis`, sem multiplicação por itens ou reviews.
- **Entrega analisada:** pedido com `order_status='delivered'`, data entregue e data estimada válidas.
- **Atraso:** a data de entrega real é posterior à data estimada; se ocorrer no mesmo dia não conta atraso.
- **Mês:** mês da compra, não mês da entrega. Inclui agrupamento NULL se necessário para conciliação.
- **Avaliação negativa:** review mais recente do pedido, nota 1 ou 2.
- **Custo dos itens:** soma dos preços dos itens; não representa receita recebida.
- **Percentual de frete:** soma dos fretes / soma dos preços de itens, não média das razões por pedido.
- **Ranking de UF:** somente UFs com pelo menos 30 entregas analisadas.

## Decisões revistas após análise com IA
- Evitar JOIN direto entre pedidos e itens/reviews para não duplicar contagens. Agregar itens por pedido e selecionar uma review antes do JOIN.
- Uma avaliação é descritiva: a associação atraso/nota não permite concluir causalidade.
- RAW não deve ser desduplicada. Datas convertidas apenas na REFINED.
- Os dois marts de entregas usam exatamente a mesma população para reconciliar sem valores fixos.
