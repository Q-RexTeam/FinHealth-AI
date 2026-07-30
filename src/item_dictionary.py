from pathlib import Path
import pandas as pd

# =====================================================
# Đường dẫn
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "financial_statement_long.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "financial_item_dictionary.csv"
)

CONFLICT_FILE = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "financial_item_conflicts.csv"
)

# =====================================================
# Đọc dữ liệu
# =====================================================

df = pd.read_csv(INPUT_FILE)

# =====================================================
# Kiểm tra dữ liệu bất nhất
# =====================================================

conflicts = (
    df.groupby("item_id")
      .agg(
          statement_type=("statement_type", "first"),
          name_count=("item_name_vi", "nunique"),
          names=("item_name_vi", lambda x: " | ".join(sorted(set(x))))
      )
      .reset_index()
)

conflicts = conflicts[conflicts["name_count"] > 1]

# =====================================================
# Xuất báo cáo lỗi nếu có
# =====================================================

if not conflicts.empty:
    conflicts.to_csv(
        CONFLICT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"⚠ Phát hiện {len(conflicts)} item_id có nhiều tên khác nhau.")
    print(f"Đã lưu: {CONFLICT_FILE}")

# =====================================================
# Tạo từ điển chỉ tiêu
# =====================================================

financial_item_dictionary = (
    df[
        [
            "item_id",
            "statement_type",
            "item_name_vi",
        ]
    ]
    .drop_duplicates()
    .sort_values(
        by=[
            "statement_type",
            "item_id",
        ]
    )
)

# Nếu có nhiều tên cho cùng item_id thì chỉ giữ bản ghi đầu tiên
financial_item_dictionary = (
    financial_item_dictionary
    .drop_duplicates(subset=["item_id"], keep="first")
    .reset_index(drop=True)
)

# =====================================================
# Xuất file
# =====================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

financial_item_dictionary.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

print("=" * 60)
print("Hoàn thành!")
print(f"Số chỉ tiêu: {len(financial_item_dictionary)}")
print(f"Lưu tại: {OUTPUT_FILE}")
print("=" * 60)