"""Camada REFINED: normalização, tipos, deduplicação e grão explícito."""
import duckdb

SQL = {
    "orders": """
        CREATE OR REPLACE TABLE refined.orders AS
        WITH ordenados AS (
            SELECT
                NULLIF(TRIM(order_id), '') AS order_id,
                NULLIF(TRIM(customer_id), '') AS customer_id,
                LOWER(NULLIF(TRIM(order_status), '')) AS order_status,
                TRY_CAST(order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
                TRY_CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_at,
                TRY_CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_at,
                ROW_NUMBER() OVER (
                    PARTITION BY NULLIF(TRIM(order_id), '')
                    ORDER BY TRY_CAST(order_purchase_timestamp AS TIMESTAMP) DESC NULLS LAST,
                             customer_id ASC NULLS LAST
                ) AS posicao
            FROM raw.orders
            WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
        )
        SELECT order_id, customer_id, order_status, purchased_at, delivered_at,
               estimated_at,
               CASE WHEN order_status = 'delivered'
                         AND delivered_at IS NOT NULL AND estimated_at IS NOT NULL
                    THEN CAST(delivered_at AS DATE) > CAST(estimated_at AS DATE)
                    ELSE NULL END AS is_late,
               CASE WHEN order_status = 'delivered'
                         AND delivered_at IS NOT NULL AND purchased_at IS NOT NULL
                    THEN DATE_DIFF('day', CAST(purchased_at AS DATE), CAST(delivered_at AS DATE))
                    ELSE NULL END AS delivery_days
        FROM ordenados WHERE posicao = 1
    """,
    "customers": """
        CREATE OR REPLACE TABLE refined.customers AS
        WITH selecionados AS (
            SELECT NULLIF(TRIM(customer_id), '') AS customer_id,
                   NULLIF(UPPER(TRIM(customer_state)), '') AS customer_state,
                   NULLIF(LOWER(TRIM(customer_city)), '') AS customer_city,
                   ROW_NUMBER() OVER (
                       PARTITION BY NULLIF(TRIM(customer_id), '')
                       ORDER BY customer_state ASC NULLS LAST,
                                customer_city ASC NULLS LAST
                   ) AS posicao
            FROM raw.customers
            WHERE NULLIF(TRIM(customer_id), '') IS NOT NULL
        )
        SELECT customer_id, customer_state, customer_city
        FROM selecionados WHERE posicao = 1
    """,
    "items": """
        CREATE OR REPLACE TABLE refined.items AS
        WITH selecionados AS (
            SELECT NULLIF(TRIM(order_id), '') AS order_id,
                   TRY_CAST(order_item_id AS INTEGER) AS order_item_id,
                   TRY_CAST(price AS DECIMAL(14,2)) AS price,
                   TRY_CAST(freight_value AS DECIMAL(14,2)) AS freight_value,
                   ROW_NUMBER() OVER (
                       PARTITION BY NULLIF(TRIM(order_id), ''),
                                    TRY_CAST(order_item_id AS INTEGER)
                       ORDER BY price ASC NULLS LAST, freight_value ASC NULLS LAST
                   ) AS posicao
            FROM raw.items
            WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
              AND TRY_CAST(order_item_id AS INTEGER) > 0
        )
        SELECT order_id, order_item_id, price, freight_value
        FROM selecionados WHERE posicao = 1
    """,
    "reviews": """
        CREATE OR REPLACE TABLE refined.reviews AS
        WITH selecionados AS (
            SELECT NULLIF(TRIM(order_id), '') AS order_id,
                   NULLIF(TRIM(review_id), '') AS review_id,
                   TRY_CAST(review_score AS INTEGER) AS score_bruto,
                   TRY_CAST(review_creation_date AS TIMESTAMP) AS created_at,
                   ROW_NUMBER() OVER (
                       PARTITION BY NULLIF(TRIM(order_id), '')
                       ORDER BY TRY_CAST(review_creation_date AS TIMESTAMP)
                                    DESC NULLS LAST,
                                review_id ASC NULLS LAST
                   ) AS posicao
            FROM raw.reviews
            WHERE NULLIF(TRIM(order_id), '') IS NOT NULL
        )
        SELECT order_id, review_id,
               CASE WHEN score_bruto BETWEEN 1 AND 5 THEN score_bruto ELSE NULL END
                   AS review_score,
               created_at
        FROM selecionados WHERE posicao = 1
    """,
    "order_financials": """
        CREATE OR REPLACE TABLE refined.order_financials AS
        SELECT order_id, COUNT(*) AS item_count,
               SUM(price) AS total_items_value,
               SUM(freight_value) AS total_freight_value
        FROM refined.items GROUP BY order_id
    """,
    "order_analysis": """
        CREATE OR REPLACE TABLE refined.order_analysis AS
        SELECT o.order_id, o.customer_id, o.order_status,
               o.purchased_at, o.delivered_at, o.estimated_at,
               o.is_late, o.delivery_days,
               c.customer_state, c.customer_city,
               COALESCE(f.item_count, 0) AS item_count,
               f.total_items_value, f.total_freight_value,
               r.review_score
        FROM refined.orders o
        LEFT JOIN refined.customers c USING (customer_id)
        LEFT JOIN refined.order_financials f USING (order_id)
        LEFT JOIN refined.reviews r USING (order_id)
    """,
}


def transformar(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    con.execute("CREATE SCHEMA IF NOT EXISTS refined")
    contagens = {}
    for tabela, sql in SQL.items():
        con.execute(sql)
        n = con.execute(f"SELECT COUNT(*) FROM refined.{tabela}").fetchone()[0]
        print(f"[REFINED] {tabela}: {n:,} linhas")
        contagens[tabela] = n
    return contagens
