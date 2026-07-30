from pathlib import Path
import pandas as pd

# =====================================================
# Đường dẫn
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw" / "financial_statements"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "financial_statement_long.csv"
)

# =====================================================
# Mapping statement_type
# =====================================================

STATEMENT_MAPPING = {
    "balance_sheet": "balance_sheet",
    "cash_flow": "cash_flow",
    "income_statement": "income_statement",
}

records = []

# =====================================================
# Duyệt từng doanh nghiệp
# =====================================================

for company_folder in RAW_FOLDER.iterdir():

    if not company_folder.is_dir():
        continue

    # ticker = tên thư mục
    ticker = company_folder.name.upper()

    print(f"Đang xử lý {ticker}")

    # =================================================
    # Duyệt 3 báo cáo tài chính
    # =================================================

    for file in company_folder.glob("*.csv"):

        filename = file.stem.lower()

        statement_type = None

        for key in STATEMENT_MAPPING:
            if key in filename:
                statement_type = STATEMENT_MAPPING[key]
                break

        if statement_type is None:
            print(f"  Bỏ qua: {file.name}")
            continue

        # =============================================
        # Đọc dữ liệu
        # =============================================

        df = pd.read_csv(file)
        print(
            df.loc[df["item_id"] == "isa4",
                ["2022", "2023", "2024", "2025"]]
        )

        # Bỏ cột index nếu có
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # =============================================
        # Wide -> Long
        # =============================================

        year_columns = ["2022", "2023", "2024", "2025"]

        long_df = df.melt(
            id_vars=["item", "item_en", "item_id"],
            value_vars=year_columns,
            var_name="fiscal_year",
            value_name="raw_value",
        )
        print(
            long_df[
                long_df["item_id"] == "isa4"
            ]
        )        

        long_df.rename(
            columns={
                "item": "item_name_vi",
                "item_en": "item_name_en",
            },
            inplace=True,
        )

        # =============================================
        # Thêm metadata
        # =============================================

        long_df.insert(0, "ticker", ticker)
        long_df.insert(2, "statement_type", statement_type)

        # =============================================
        # Chỉ giữ các cột cần thiết
        # =============================================

        long_df = long_df[
            [
                "ticker",
                "fiscal_year",
                "statement_type",
                "item_id",
                "item_name_vi",
                "item_name_en",
                "raw_value",
            ]
        ]

        records.append(long_df)

# =====================================================
# Ghép toàn bộ dữ liệu
# =====================================================

financial_statement_long = pd.concat(records, ignore_index=True)

# =====================================================
# Sắp xếp dữ liệu
# =====================================================

financial_statement_long = financial_statement_long.sort_values(
    by=[
        "ticker",
        "fiscal_year",
        "statement_type",
        "item_id",
    ]
).reset_index(drop=True)

print(
    financial_statement_long[
        (financial_statement_long["ticker"]=="BMP")
        &
        (financial_statement_long["item_id"]=="isa4")
    ]
)

# =====================================================
# Xuất file
# =====================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

financial_statement_long.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

print("=" * 60)
print("Hoàn thành!")
print(f"Số dòng: {len(financial_statement_long):,}")
print(f"Lưu tại: {OUTPUT_FILE}")
print("=" * 60)