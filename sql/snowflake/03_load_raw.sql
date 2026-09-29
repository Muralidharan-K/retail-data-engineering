USE DATABASE RETAIL_DB;
USE SCHEMA RAW;

-- =====================================================
-- Load CUSTOMERS
-- =====================================================
COPY INTO RETAIL_DB.RAW.CUSTOMERS
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('customers.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- =====================================================
-- Load PRODUCTS
-- =====================================================
COPY INTO RETAIL_DB.RAW.PRODUCTS
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('products.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- =====================================================
-- Load STORES
-- =====================================================
COPY INTO RETAIL_DB.RAW.STORES
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('stores.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- =====================================================
-- Load ORDERS
-- =====================================================
COPY INTO RETAIL_DB.RAW.ORDERS
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('orders.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- =====================================================
-- Load ORDER_ITEMS
-- =====================================================
COPY INTO RETAIL_DB.RAW.ORDER_ITEMS
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('order_items.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- =====================================================
-- Load PAYMENTS
-- =====================================================
COPY INTO RETAIL_DB.RAW.PAYMENTS
FROM @RETAIL_DB.RAW.RETAIL_RAW_STAGE
FILES = ('payments.csv')
FILE_FORMAT = (
    FORMAT_NAME = 'RETAIL_DB.RAW.RETAIL_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';