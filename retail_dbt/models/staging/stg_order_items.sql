SELECT
    ORDER_ITEM_ID,
    ORDER_ID,
    PRODUCT_ID,
    QUANTITY,
    UNIT_PRICE,
    DISCOUNT,
    LINE_AMOUNT
FROM {{ source('raw', 'order_items') }}