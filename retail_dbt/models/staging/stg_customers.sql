SELECT
    CUSTOMER_ID,
    CUSTOMER_NAME,
    EMAIL,
    PHONE,
    CITY,
    STATE,
    COUNTRY,
    REGISTRATION_DATE
FROM {{ source('raw', 'customers') }}