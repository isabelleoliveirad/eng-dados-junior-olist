-- Pergunta: a taxa de atrasos mudou entre os meses de compra?
-- Grão: 1 linha por mês de compra (inclusive NULL, para reconciliação).
SELECT CAST(DATE_TRUNC('month', purchased_at) AS DATE) AS mes_compra,
       COUNT(*) AS entregas_analisadas,
       SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS entregas_atrasadas,
       ROUND(100.0 * SUM(CASE WHEN is_late THEN 1 ELSE 0 END) / COUNT(*), 2)
           AS pct_atraso
FROM refined.order_analysis
WHERE order_status = 'delivered' AND is_late IS NOT NULL
GROUP BY 1
ORDER BY 1;
