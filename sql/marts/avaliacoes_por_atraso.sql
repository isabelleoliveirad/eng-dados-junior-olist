-- Pergunta: clientes que receberam em atraso avaliaram pior?
-- Grão: situação de atraso entre pedidos entregues com review válida.
-- Advertência: associação descritiva, não demonstra causalidade.
SELECT CASE WHEN is_late THEN 'Atrasada' ELSE 'No prazo' END AS situacao,
       COUNT(*) AS pedidos_avaliados,
       ROUND(AVG(review_score), 2) AS nota_media,
       SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) AS avaliacoes_negativas,
       ROUND(100.0 * SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END)
             / COUNT(*), 2) AS pct_avaliacoes_negativas
FROM refined.order_analysis
WHERE order_status = 'delivered' AND is_late IS NOT NULL
  AND review_score BETWEEN 1 AND 5
GROUP BY 1
ORDER BY 1;
