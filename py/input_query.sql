WITH orders_with_details AS (
    SELECT order_id, order_date, customer_id
    FROM orders
    WHERE order_date > '2023-01-01'
)
SELECT o.order_id, o.customer_id, u.active
FROM orders_with_details o
JOIN users u ON o.customer_id = u.id
WHERE u.active = 1;
