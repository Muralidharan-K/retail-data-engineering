create database if not exists RETAIL_DB;
use database retail_db;
create schema if not exists RAW;
create schema if not exists STAGING;
create schema if not exists core;
create schema if not exists ANALYTICS;
show schemas in database retail_db;

--To create customers table
create or replace table retail_db.raw.customers(
    customer_id number,
    customer_name varchar(200),
    email varchar(200),
    phone number(30),
    city varchar(100),
    state varchar(100),
    country varchar (100),
    registration_date date 
);

desc table retail_db.raw.customers;

select current_user(), current_role();

use role accountadmin;

--To create products table
CREATE OR REPLACE TABLE RETAIL_DB.RAW.PRODUCTS (
    PRODUCT_ID NUMBER,
    PRODUCT_NAME VARCHAR(200),
    CATEGORY VARCHAR(100),
    SUBCATEGORY VARCHAR(100),
    BRAND VARCHAR(100),
    UNIT_PRICE NUMBER(18,2)
);

--To create Stores table
CREATE OR REPLACE TABLE RETAIL_DB.RAW.STORES (
    STORE_ID NUMBER,
    STORE_NAME VARCHAR(200),
    CITY VARCHAR(100),
    STATE VARCHAR(100),
    REGION VARCHAR(100),
    STORE_TYPE VARCHAR(50)
);

-- To create orders table
CREATE OR REPLACE TABLE RETAIL_DB.RAW.ORDERS (
    ORDER_ID NUMBER,
    CUSTOMER_ID NUMBER,
    STORE_ID NUMBER,
    ORDER_DATE TIMESTAMP_NTZ,
    ORDER_STATUS VARCHAR(50),
    PAYMENT_METHOD VARCHAR(50)
);

--To create order_items table
CREATE OR REPLACE TABLE RETAIL_DB.RAW.ORDER_ITEMS (
    ORDER_ITEM_ID NUMBER,
    ORDER_ID NUMBER,
    PRODUCT_ID NUMBER,
    QUANTITY NUMBER,
    UNIT_PRICE NUMBER(18,2),
    DISCOUNT NUMBER(18,2),
    LINE_AMOUNT NUMBER(18,2)
);

--To create payments table
CREATE OR REPLACE TABLE RETAIL_DB.RAW.PAYMENTS (
    PAYMENT_ID NUMBER,
    ORDER_ID NUMBER,
    PAYMENT_DATE TIMESTAMP_NTZ,
    PAYMENT_METHOD VARCHAR(50),
    PAYMENT_AMOUNT NUMBER(18,2),
    PAYMENT_STATUS VARCHAR(50)
);