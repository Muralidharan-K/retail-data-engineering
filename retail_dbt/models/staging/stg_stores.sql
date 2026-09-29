SELECT
    STORE_ID,
    STORE_NAME,
    CITY,
    STATE,
    REGION,
    STORE_TYPE
FROM {{ source('raw', 'stores') }}