"""
==========================================================
FinHealth AI
Layer 8 - Accounting Logic Validation
==========================================================

Input:
    data/processor/financial_statement_normalized.csv

Output:
    data/processor/data_quality_report.csv

Author:
    FinHealth AI
==========================================================
"""

import pandas as pd
from pathlib import Path

from source_code.check_rules import CHECK_RULES

# ==========================================================
# CONFIG
# ==========================================================

INPUT_FILE = Path("data/processor/financial_statement_normalized.csv")

OUTPUT_FILE = Path("data/processor/data_quality_report.csv")


# ==========================================================
# LOAD DATA
# ==========================================================


def load_data():

    df = pd.read_csv(INPUT_FILE)

    required_columns = ["ticker", "fiscal_year", "item_id", "value_processor"]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:

        raise ValueError(f"Missing columns: {missing_columns}")

    df = df.copy()

    df["ticker"] = df["ticker"].astype(str).str.strip()

    df["fiscal_year"] = (
        pd.to_numeric(df["fiscal_year"], errors="coerce").fillna(0).astype(int)
    )

    df["item_id"] = df["item_id"].astype(str).str.strip()

    df["value_processor"] = pd.to_numeric(df["value_processor"], errors="coerce")

    return df


# ==========================================================
# BUILD LOOKUP
# ==========================================================


def build_lookup(df):

    lookup = {}

    grouped = df.groupby(["ticker", "fiscal_year"])

    for (ticker, year), group in grouped:

        values = {}

        for _, row in group.iterrows():

            values[row["item_id"]] = row["value_processor"]

        lookup[(ticker, year)] = values

    return lookup


# ==========================================================
# GET ITEM VALUE
# ==========================================================


def get_value(values, item_id):

    if item_id not in values:

        return None

    value = values[item_id]

    if pd.isna(value):

        return None

    return float(value)


# ==========================================================
# EXECUTE ONE RULE
# ==========================================================


def execute_rule(ticker, year, values, rule):
    """
    Execute one accounting rule

    difference = left - sum(right)
    equation_scale = max(abs(left), sum(abs(right)))
    allowed_error = max(abs_tolerance, equation_scale * relative_tolerance)

    PASS if abs(difference) <= allowed_error
    """

    # -------------------------
    # Left value
    # -------------------------
    left_value = get_value(values, rule["left"])

    if left_value is None:
        return {
            "ticker": ticker,
            "year": year,
            "check_name": rule["name"],
            "left_value": None,
            "right_value": None,
            "difference": None,
            "allowed_error": None,
            "abs_tolerance": rule.get("abs_tolerance"),
            "relative_tolerance": rule.get("relative_tolerance"),
            "equation_scale": None,
            "status": "fail",
        }

    # -------------------------
    # Right values & validation
    # -------------------------
    # Thu thập tất cả giá trị vế phải
    right_components = [get_value(values, item) for item in rule["right"]]

    # Nếu có bất kỳ mục nào bị thiếu (None), đánh dấu FAIL
    if any(val is None for val in right_components):
        return {
            "ticker": ticker,
            "year": year,
            "check_name": rule["name"],
            "left_value": left_value,
            "right_value": None,
            "difference": None,
            "allowed_error": None,
            "abs_tolerance": rule.get("abs_tolerance"),
            "relative_tolerance": rule.get("relative_tolerance"),
            "equation_scale": None,
            "status": "fail",
        }

    right_value = sum(right_components)

    # -------------------------
    # Difference
    # -------------------------
    difference = round(left_value - right_value, 6)

    # ----------------------------------
    # Dynamic tolerance (Áp dụng đúng như ảnh)
    # ----------------------------------
    abs_tolerance = rule["abs_tolerance"]
    relative_tolerance = rule["relative_tolerance"]

    # 1. Quy mô phương trình
    equation_scale = max(abs(left_value), sum(abs(val) for val in right_components))

    # 2. Ngưỡng sai số cho phép
    allowed_error = max(abs_tolerance, equation_scale * relative_tolerance)

    status = "pass" if abs(difference) <= allowed_error else "fail"

    return {
        "ticker": ticker,
        "year": year,
        "check_name": rule["name"],
        "left_value": left_value,
        "right_value": right_value,
        "difference": difference,
        "allowed_error": allowed_error,
        "abs_tolerance": abs_tolerance,
        "relative_tolerance": relative_tolerance,
        "equation_scale": equation_scale,  # Lưu lại để audit / debug khi cần
        "status": status,
    }


# ==========================================================
# EXECUTE ALL RULES
# ==========================================================


def execute_all_rules(df):

    lookup = build_lookup(df)

    report = []

    for (ticker, year), values in lookup.items():

        for rule in CHECK_RULES:

            result = execute_rule(ticker, year, values, rule)

            report.append(result)

    report = pd.DataFrame(report)

    return report


# ==========================================================
# EXPORT REPORT
# ==========================================================


def export_report(report):

    report = report[
        [
            "ticker",
            "year",
            "check_name",
            "left_value",
            "right_value",
            "difference",
            "allowed_error",
            "status",
        ]
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    return report


# ==========================================================
# PRINT SUMMARY
# ==========================================================


def print_summary(report):

    total = len(report)

    total_pass = (report["status"] == "pass").sum()

    total_fail = (report["status"] == "fail").sum()

    print("\n" + "=" * 60)

    print("Layer 8 - Accounting Logic Validation")

    print("=" * 60)

    print(f"Total Rules : {total}")

    print(f"PASS        : {total_pass}")

    print(f"FAIL        : {total_fail}")

    if total > 0:

        print(f"Pass Rate   : {100 * total_pass / total:.2f}%")

    print("=" * 60)

    print("\nOutput:")

    print(OUTPUT_FILE)

    print()


# ==========================================================
# MAIN
# ==========================================================


def main():

    print("=" * 60)

    print("Loading Layer 7 output...")

    df = load_data()

    print(f"Loaded {len(df):,} rows.")

    report = execute_all_rules(df)

    report = export_report(report)

    print_summary(report)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()
