from pathlib import Path
import pandas as pd

# ==========================================================
# Đường dẫn
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

METADATA_FOLDER = PROJECT_ROOT / "data" / "metadata"
PROCESSOR_FOLDER = PROJECT_ROOT / "data" / "processor"

NORMALIZED_FILE = (
    PROCESSOR_FOLDER /
    "financial_statement_normalized.csv"
)

DICTIONARY_FILE = (
    METADATA_FOLDER /
    "financial_item_dictionary.csv"
)

OUTPUT_FILE = (
    PROCESSOR_FOLDER /
    "financial_statement_normalized.csv"
)

# ==========================================================
# Đọc dữ liệu
# ==========================================================

financial_statement = pd.read_csv(NORMALIZED_FILE)

dictionary = pd.read_csv(DICTIONARY_FILE)

# ==========================================================
# Chỉ lấy 2 cột cần merge
# ==========================================================

dictionary = dictionary[
    [
        "item_id",
        "sign_rule"
    ]
].drop_duplicates(
    subset="item_id"
)

# ==========================================================
# Merge sign_rule theo item_id
# ==========================================================

financial_statement = financial_statement.merge(
    dictionary,
    how="left",
    on="item_id"
)

# ==========================================================
# Lưu lại
# ==========================================================

financial_statement.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 60)
print("Merge sign_rule hoàn thành")
print(f"Số dòng: {len(financial_statement):,}")
print("=" * 60)