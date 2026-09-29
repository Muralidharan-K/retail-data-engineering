USE DATABASE RETAIL_DB;
USE SCHEMA RAW;

-- ============================================================
-- Common CSV file format
-- ============================================================

CREATE OR REPLACE FILE FORMAT RETAIL_CSV_FORMAT
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    EMPTY_FIELD_AS_NULL = TRUE
    NULL_IF = ('', 'NULL', 'null')
    DATE_FORMAT = 'YYYY-MM-DD'
    TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

-- ============================================================
-- Internal Snowflake stage
-- ============================================================

CREATE OR REPLACE STAGE RETAIL_RAW_STAGE
    FILE_FORMAT = RETAIL_CSV_FORMAT;