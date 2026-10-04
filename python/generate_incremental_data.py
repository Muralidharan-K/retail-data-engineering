import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(100)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
INCREMENTAL_DIR = BASE_DIR / "data" / "incremental"

INCREMENTAL_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(filename):
    with (RAW_DIR / filename).open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def write_csv(filename, fieldnames, rows):

    filepath = INCREMENTAL_DIR / filename

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


def generate_daily_sales():

    customers = read_csv("customers.csv")
    products = read_csv("products.csv")
    stores = read_csv("stores.csv")

    customer_ids = [row["customer_id"] for row in customers]
    product_ids = [row["product_id"] for row in products]
    store_ids = [row["store_id"] for row in stores]

    start_date = datetime(2026, 10, 2)

    for day_number in range(1):

        current_date = start_date + timedelta(days=day_number)

        rows = []

        base_order_id = 200000 + (day_number * 1000)

        for i in range(1000):

            order_id = base_order_id + i

            customer_id = random.choice(customer_ids)
            product_id = random.choice(product_ids)
            store_id = random.choice(store_ids)

            quantity = random.randint(1, 5)

            unit_price = round(
                random.uniform(100, 50000),
                2
            )

            discount = round(
                random.uniform(0, unit_price * 0.15),
                2
            )

            gross_amount = round(
                quantity * unit_price,
                2
            )

            net_amount = round(
                gross_amount - discount,
                2
            )

            order_time = current_date.replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )

            rows.append({
                "order_id": order_id,
                "customer_id": customer_id,
                "product_id": product_id,
                "store_id": store_id,
                "order_date": order_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
                "gross_amount": gross_amount,
                "net_amount": net_amount,
                "source_file": (
                    f"sales_{current_date.strftime('%Y_%m_%d')}.csv"
                )
            })

        filename = (
            f"sales_{current_date.strftime('%Y_%m_%d')}.csv"
        )

        write_csv(
            filename,
            [
                "order_id",
                "customer_id",
                "product_id",
                "store_id",
                "order_date",
                "quantity",
                "unit_price",
                "discount",
                "gross_amount",
                "net_amount",
                "source_file"
            ],
            rows
        )


def main():

    print("=" * 60)
    print("Retail Incremental Data Generator")
    print("=" * 60)

    generate_daily_sales()

    print("=" * 60)
    print("Incremental data generation completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()