# Snowflake Incremental Processing

## Objective

Implement incremental data processing in Snowflake using:

- Snowflake Stage
- RAW table
- Snowflake Stream
- Snowflake Task
- Incremental target table

## Architecture

CSV
  ↓
Snowflake Internal Stage
  ↓
RAW_SALES_INCREMENTAL
  ↓
SALES_INCREMENTAL_STREAM
  ↓
LOAD_INCREMENTAL_SALES_TASK
  ↓
FACT_SALES_INCREMENTAL

## Source Files

Incremental files used:

- sales_2026_09_26.csv
- sales_2026_09_27.csv
- sales_2026_09_28.csv
- sales_2026_09_26.csv was reloaded to demonstrate another incremental batch

Each file contains 1,000 records.

## RAW Table

Table:

RETAIL_DB.RAW.RAW_SALES_INCREMENTAL

Columns:

- ORDER_ID
- CUSTOMER_ID
- PRODUCT_ID
- STORE_ID
- ORDER_DATE
- QUANTITY
- UNIT_PRICE
- DISCOUNT
- GROSS_AMOUNT
- NET_AMOUNT
- SOURCE_FILE

## Stream

Stream:

RETAIL_DB.RAW.SALES_INCREMENTAL_STREAM

Purpose:

Tracks changes made to RAW_SALES_INCREMENTAL after the Stream's offset.

## Task

Task:

RETAIL_DB.CORE.LOAD_INCREMENTAL_SALES_TASK

Warehouse:

COMPUTE_WH

Schedule:

1 MINUTE

Condition:

SYSTEM$STREAM_HAS_DATA()

The Task processes only when the Stream contains changes.

## Incremental Target

Table:

RETAIL_DB.CORE.FACT_SALES_INCREMENTAL

Validation results:

- RAW_SALES_INCREMENTAL: 4,000 rows
- FACT_SALES_INCREMENTAL: 3,000 rows
- SALES_INCREMENTAL_STREAM: 0 rows after processing

## Validation

Manual Task execution successfully processed 1,000 Stream records.

Scheduled Task execution also successfully processed a new 1,000-row batch without manually executing the Task.

This demonstrated Snowflake incremental ELT using Streams and Tasks.