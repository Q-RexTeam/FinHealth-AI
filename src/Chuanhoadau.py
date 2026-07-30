from pathlib import Path
import pandas as pd

# ==========================================================
# Đường dẫn
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

METADATA_FOLDER = PROJECT_ROOT / "data" / "metadata"

INPUT_FILE = METADATA_FOLDER / "financial_statement_long.csv"

DICTIONARY_FILE = METADATA_FOLDER / "financial_item_dictionary.csv"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processor"
    / "financial_statement_normalized.csv"
)

# ==========================================================
# Đọc dữ liệu
# ==========================================================

financial_statement = pd.read_csv(INPUT_FILE)

dictionary = pd.read_csv(DICTIONARY_FILE)

# ==========================================================
# Merge sign_rule
# ==========================================================

financial_statement = financial_statement.merge(
    dictionary[
        [
            "item_id",
            "sign_rule"
        ]
    ],
    how="left",
    on="item_id"
)

# ==========================================================
# Khởi tạo value_processor = raw_value
# ==========================================================

financial_statement["value_processor"] = financial_statement["raw_value"]

# ==========================================================
# Rule 1
# always_positive
# ==========================================================

mask = financial_statement["sign_rule"] == "always_positive"

financial_statement.loc[
    mask,
    "value_processor"
] = financial_statement.loc[
    mask,
    "raw_value"
].abs()

# ==========================================================
# Rule 2
# expense_negative
# giữ nguyên dấu
# ==========================================================

# Không làm gì

# ==========================================================
# Rule 3
# signed
# giữ nguyên dấu
# ==========================================================

# Không làm gì

# ==========================================================
# Rule 4
# contra_asset
# giữ nguyên dấu
# ==========================================================

# Không làm gì

# ==========================================================
# Xuất file
# ==========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

financial_statement.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 60)
print("Processor hoàn thành")
print(f"Số dòng: {len(financial_statement):,}")
print(f"Lưu tại: {OUTPUT_FILE}")
print("=" * 60)