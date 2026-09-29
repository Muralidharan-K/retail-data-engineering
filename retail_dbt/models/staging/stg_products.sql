SELECT
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUBCATEGORY,
    BRAND,
    UNIT_PRICE
FROM {{ source('raw', 'products') }}