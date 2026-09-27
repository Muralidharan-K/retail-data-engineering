import csv
import random
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
TEST_DIR = BASE_DIR / "data" / "test_data"

TEST_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(filename):
    with (RAW_DIR / filename).open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def write_csv(filename, fieldnames, rows):
    filepath = TEST_DIR / filename

    with filepath.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows):,} rows")


def create_bad_orders():

    orders = read_csv("orders.csv")

    bad_orders = []

    # --------------------------------------------------------
    # 1. Keep original records
    # --------------------------------------------------------

    bad_orders.extend(orders)

    # --------------------------------------------------------
    # 2. Duplicate records
    # --------------------------------------------------------

    duplicate_records = random.sample(
        orders,
        100
    )

    bad_orders.extend(duplicate_records)

    # --------------------------------------------------------
    # 3. NULL customer IDs
    # --------------------------------------------------------

    null_customer_records = random.sample(
        orders,
        50
    )

    for record in null_customer_records:
        record = record.copy()
        record["customer_id"] = ""
        bad_orders.append(record)

    # --------------------------------------------------------
    # 4. Invalid customer IDs
    # --------------------------------------------------------

    invalid_customer_records = random.sample(
        orders,
        50
    )

    for record in invalid_customer_records:
        record = record.copy()
        record["customer_id"] = "999999"
        bad_orders.append(record)

    # --------------------------------------------------------
    # 5. Invalid store IDs
    #
    # Note:
    # orders.csv normally contains valid store IDs.
    # We intentionally use an invalid value here.
    # --------------------------------------------------------

    invalid_store_records = random.sample(
        orders,
        50
    )

    for record in invalid_store_records:
        record = record.copy()
        record["store_id"] = "9999"
        bad_orders.append(record)

    # --------------------------------------------------------
    # 6. Invalid order status
    # --------------------------------------------------------

    invalid_status_records = random.sample(
        orders,
        50
    )

    for record in invalid_status_records:
        record = record.copy()
        record["order_status"] = "UNKNOWN_STATUS"
        bad_orders.append(record)

    # --------------------------------------------------------
    # Write test dataset
    # --------------------------------------------------------

    write_csv(
        "orders_bad_data.csv",
        [
            "order_id",
            "customer_id",
            "store_id",
            "order_date",
            "order_status",
            "payment_method"
        ],
        bad_orders
    )


def main():

    print("=" * 60)
    print("Retail Data Quality Test Data Generator")
    print("=" * 60)

    create_bad_orders()

    print("=" * 60)
    print("Test data generation completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()