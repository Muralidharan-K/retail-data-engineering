import csv
from pathlib import Path
from collections import Counter


# =========================================================
# Project paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "test_data"
    / "orders_bad_data.csv"
)

CUSTOMERS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers.csv"
)

STORES_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "stores.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

REJECTED_FILE = OUTPUT_DIR / "orders_rejected.csv"
REPORT_FILE = OUTPUT_DIR / "orders_dq_report.txt"


# =========================================================
# Business rules
# =========================================================

VALID_STATUSES = {
    "COMPLETED",
    "PENDING",
    "CANCELLED",
    "SHIPPED",
    "PROCESSING",
}


# =========================================================
# Helper function
# =========================================================

def load_ids(file_path, column_name):

    ids = set()

    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            value = row[column_name].strip()

            if value:
                ids.add(int(value))

    return ids


# =========================================================
# Main DQ validation
# =========================================================

def validate_orders():

    print("=" * 65)
    print("Retail Orders - Data Quality Validation")
    print("=" * 65)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # Check input file
    # -----------------------------------------------------

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    # -----------------------------------------------------
    # Load reference IDs
    # -----------------------------------------------------

    print("Loading reference data...")

    customer_ids = load_ids(
        CUSTOMERS_FILE,
        "customer_id"
    )

    store_ids = load_ids(
        STORES_FILE,
        "store_id"
    )

    print(f"Valid customers : {len(customer_ids):,}")
    print(f"Valid stores    : {len(store_ids):,}")

    # -----------------------------------------------------
    # Read test data
    # -----------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "order_id",
            "customer_id",
            "store_id",
            "order_date",
            "order_status",
            "payment_method",
        }

        missing_columns = (
            required_columns
            - set(reader.fieldnames or [])
        )

        if missing_columns:
            raise ValueError(
                f"Missing columns: {sorted(missing_columns)}"
            )

        rows = list(reader)

    total_rows = len(rows)

    # -----------------------------------------------------
    # Tracking
    # -----------------------------------------------------

    order_id_counts = Counter()

    for row in rows:

        order_id = row["order_id"].strip()

        if order_id:
            order_id_counts[int(order_id)] += 1

    duplicate_order_ids = {
        order_id
        for order_id, count in order_id_counts.items()
        if count > 1
    }

    duplicate_row_count = sum(
        count - 1
        for order_id, count in order_id_counts.items()
        if count > 1
    )

    null_customer_count = 0
    invalid_customer_count = 0
    invalid_store_count = 0
    invalid_status_count = 0

    rejected_rows = []

    # -----------------------------------------------------
    # Validate every row
    # -----------------------------------------------------

    for row in rows:

        reasons = []

        # ---------------------------------------------
        # Customer NULL
        # ---------------------------------------------

        customer_value = row["customer_id"].strip()

        if not customer_value:
            null_customer_count += 1
            reasons.append("NULL_CUSTOMER_ID")

        else:

            customer_id = int(customer_value)

            if customer_id not in customer_ids:
                invalid_customer_count += 1
                reasons.append("INVALID_CUSTOMER_ID")

        # ---------------------------------------------
        # Store validation
        # ---------------------------------------------

        store_value = row["store_id"].strip()

        if store_value:

            store_id = int(store_value)

            if store_id not in store_ids:
                invalid_store_count += 1
                reasons.append("INVALID_STORE_ID")

        else:

            reasons.append("NULL_STORE_ID")

        # ---------------------------------------------
        # Status validation
        # ---------------------------------------------

        status = row["order_status"].strip().upper()

        if status not in VALID_STATUSES:

            invalid_status_count += 1
            reasons.append("INVALID_ORDER_STATUS")

        # ---------------------------------------------
        # Duplicate order
        # ---------------------------------------------

        order_id_value = row["order_id"].strip()

        if order_id_value:

            order_id = int(order_id_value)

            if order_id in duplicate_order_ids:
                reasons.append("DUPLICATE_ORDER_ID")

        # ---------------------------------------------
        # Rejected row
        # ---------------------------------------------

        if reasons:

            rejected_row = dict(row)
            rejected_row["dq_reason"] = "|".join(reasons)

            rejected_rows.append(rejected_row)

    # -----------------------------------------------------
    # Write rejected records
    # -----------------------------------------------------

    if rejected_rows:

        output_fields = list(rejected_rows[0].keys())

        with open(
            REJECTED_FILE,
            "w",
            encoding="utf-8",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=output_fields
            )

            writer.writeheader()
            writer.writerows(rejected_rows)

    # -----------------------------------------------------
    # Determine DQ status
    # -----------------------------------------------------

    dq_failed = (
        duplicate_row_count > 0
        or null_customer_count > 0
        or invalid_customer_count > 0
        or invalid_store_count > 0
        or invalid_status_count > 0
    )

    dq_status = "FAILED" if dq_failed else "PASSED"

    # -----------------------------------------------------
    # Write report
    # -----------------------------------------------------

    report_lines = [
        "Retail Orders Data Quality Report",
        "=" * 45,
        "",
        f"Input file              : {INPUT_FILE}",
        f"Total records           : {total_rows:,}",
        "",
        f"Extra duplicate rows    : {duplicate_row_count:,}",
        f"NULL customer IDs       : {null_customer_count:,}",
        f"Invalid customer IDs    : {invalid_customer_count:,}",
        f"Invalid store IDs       : {invalid_store_count:,}",
        f"Invalid order statuses  : {invalid_status_count:,}",
        "",
        f"Rejected records        : {len(rejected_rows):,}",
        f"DQ STATUS               : {dq_status}",
        "",
    ]

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report_lines))

    # -----------------------------------------------------
    # Console output
    # -----------------------------------------------------

    print()
    print("Data Quality Results")
    print("-" * 65)

    print(f"Total records          : {total_rows:,}")
    print(f"Extra duplicate rows   : {duplicate_row_count:,}")
    print(f"NULL customer IDs      : {null_customer_count:,}")
    print(f"Invalid customer IDs   : {invalid_customer_count:,}")
    print(f"Invalid store IDs      : {invalid_store_count:,}")
    print(f"Invalid statuses       : {invalid_status_count:,}")
    print(f"Rejected records       : {len(rejected_rows):,}")

    print()
    print(f"DQ STATUS              : {dq_status}")

    print()
    print(f"Rejected file          : {REJECTED_FILE}")
    print(f"DQ report              : {REPORT_FILE}")

    print("=" * 65)


if __name__ == "__main__":
    validate_orders()