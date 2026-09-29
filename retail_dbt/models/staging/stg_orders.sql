SELECT
    ORDER_ID,
    CUSTOMER_ID,
    STORE_ID,
    ORDER_DATE,
    ORDER_STATUS,
    PAYMENT_METHOD
FROM {{ source('raw', 'orders') }}