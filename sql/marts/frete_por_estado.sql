-- Pergunta: qual é a participação do frete no preço dos itens, por UF?
-- Grão: UF em pedidos entregues com itens registrados.
-- Valores de itens NÃO representam receita recebida.
SELECT customer_state AS uf,
       COUNT(*) AS pedidos_com_itens,
       ROUND(SUM(total_items_value), 2) AS valor_itens,
       ROUND(SUM(total_freight_value), 2) AS valor_frete,
       ROUND(100.0 * SUM(total_freight_value) /
             NULLIF(SUM(total_items_value), 0), 2) AS frete_sobre_itens_pct
FROM refined.order_analysis
WHERE order_status = 'delivered' AND is_late IS NOT NULL AND item_count > 0
GROUP BY customer_state
ORDER BY pedidos_com_itens DESC;
