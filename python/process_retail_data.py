import csv
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "orders.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "orders_processed.csv"


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "store_id",
    "order_date",
    "order_status",
    "payment_method",
]

VALID_STATUSES = {
    "COMPLETED",
    "PENDING",
    "CANCELLED",
    "SHIPPED",
    "PROCESSING",
}
# ---------------------------------------------------------
# Main ETL
# ---------------------------------------------------------

def process_orders():

    print("=" * 60)
    print("Retail Orders ETL")
    print("=" * 60)

    # Create processed directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # Extract
    # -----------------------------------------------------

    print(f"Input file : {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    with open(INPUT_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        # Validate source columns
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        processed_rows = []

        # -------------------------------------------------
        # Transform
        # -------------------------------------------------

        for row in reader:

            # Clean whitespace
            order_status = row["order_status"].strip().upper()
            payment_method = row["payment_method"].strip().upper()

            # Convert order date
            order_datetime = datetime.strptime(
                row["order_date"].strip(),
                "%Y-%m-%d %H:%M:%S"
            )

            # Derive date attributes
            order_date = order_datetime.date().isoformat()
            order_year = order_datetime.year
            order_month = order_datetime.month
            order_day = order_datetime.day

            processed_rows.append({
                "order_id": int(row["order_id"]),
                "customer_id": int(row["customer_id"]),
                "store_id": int(row["store_id"]),
                "order_date": order_date,
                "order_year": order_year,
                "order_month": order_month,
                "order_day": order_day,
                "order_status": order_status,
                "payment_method": payment_method,
            })

    # -----------------------------------------------------
    # Validate transformed data
    # -----------------------------------------------------

    invalid_statuses = sorted({
        row["order_status"]
        for row in processed_rows
        if row["order_status"] not in VALID_STATUSES
    })

    if invalid_statuses:
        raise ValueError(
            f"Invalid order statuses found: {invalid_statuses}"
        )

    duplicate_order_ids = set()
    seen_order_ids = set()

    for row in processed_rows:

        order_id = row["order_id"]

        if order_id in seen_order_ids:
            duplicate_order_ids.add(order_id)

        seen_order_ids.add(order_id)

    if duplicate_order_ids:
        raise ValueError(
            f"Duplicate order IDs found. "
            f"Count: {len(duplicate_order_ids)}"
        )

    # -----------------------------------------------------
    # Load
    # -----------------------------------------------------

    fieldnames = [
        "order_id",
        "customer_id",
        "store_id",
        "order_date",
        "order_year",
        "order_month",
        "order_day",
        "order_status",
        "payment_method",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(processed_rows)

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print()
    print("ETL completed successfully.")
    print(f"Input rows     : {len(processed_rows):,}")
    print(f"Output rows    : {len(processed_rows):,}")
    print(f"Output file    : {OUTPUT_FILE}")
    print()
    print("Validation:")
    print(f"Duplicate IDs  : {len(duplicate_order_ids)}")
    print(f"Invalid status : {len(invalid_statuses)}")
    print("=" * 60)


if __name__ == "__main__":
    process_orders()