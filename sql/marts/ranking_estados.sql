-- Pergunta: quais UFs têm as maiores taxas de atraso em amostra >= 30?
-- Grão: UF. CTE calcula taxa; janela DENSE_RANK ordena as posições.
WITH taxas AS (
    SELECT customer_state AS uf,
           COUNT(*) AS entregas_analisadas,
           SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS entregas_atrasadas,
           ROUND(100.0 * SUM(CASE WHEN is_late THEN 1 ELSE 0 END) / COUNT(*), 2)
               AS pct_atraso
    FROM refined.order_analysis
    WHERE order_status = 'delivered' AND is_late IS NOT NULL
      AND customer_state IS NOT NULL
    GROUP BY customer_state
    HAVING COUNT(*) >= 30
)
SELECT DENSE_RANK() OVER (ORDER BY pct_atraso DESC) AS posicao,
       uf, entregas_analisadas, entregas_atrasadas, pct_atraso
FROM taxas
ORDER BY posicao, uf;
