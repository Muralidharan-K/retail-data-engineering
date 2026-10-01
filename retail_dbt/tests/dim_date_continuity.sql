WITH date_range AS (

    SELECT
        MIN(FULL_DATE) AS MIN_DATE,
        MAX(FULL_DATE) AS MAX_DATE,
        COUNT(*) AS ACTUAL_DAYS
    FROM {{ ref('dim_date') }}

),

expected AS (

    SELECT
        DATEDIFF(DAY, MIN_DATE, MAX_DATE) + 1 AS EXPECTED_DAYS,
        ACTUAL_DAYS
    FROM date_range

)

SELECT *
FROM expected
WHERE EXPECTED_DAYS <> ACTUAL_DAYS