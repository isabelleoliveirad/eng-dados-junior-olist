-- Pergunta: quais estados concentram maior proporção de atrasos?
-- Grão: 1 linha por UF do cliente (incluindo UF nula para reconciliar).
SELECT customer_state AS uf, COUNT(*) AS entregas_analisadas,
       SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS entregas_atrasadas,
       ROUND(100.0 * SUM(CASE WHEN is_late THEN 1 ELSE 0 END) / COUNT(*), 2)
           AS pct_atraso,
       ROUND(AVG(delivery_days), 2) AS prazo_medio_dias
FROM refined.order_analysis
WHERE order_status = 'delivered' AND is_late IS NOT NULL
GROUP BY customer_state
ORDER BY entregas_analisadas DESC;
