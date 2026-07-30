"""
===========================================================
FinHealth AI
Layer 9 - Company Year Feature Engineering

Step 1 : Load normalized data
Step 2 : Mapping item_id -> financial_variable

Theo tài liệu Layer 9
===========================================================
"""

import os
import pandas as pd

from feature_mapping import ITEM_MAP

# ==========================================================
# PATH
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    PROJECT_ROOT, "data", "processor", "financial_statement_normalized.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "data", "processor", "company_year_features.csv"
)

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "ticker",
    "fiscal_year",
    "statement_type",
    "item_id",
    "value_processor",
]

# ==========================================================
# LOAD DATA
# ==========================================================


def load_data():

    print("=" * 60)
    print("STEP 1 - LOAD DATA")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Thiếu cột:\n{missing}")

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    return df


# ==========================================================
# MAP FINANCIAL VARIABLES
# ==========================================================


def map_financial_variable(df):

    print("\n" + "=" * 60)
    print("STEP 2 - MAP FINANCIAL VARIABLES")
    print("=" * 60)

    reverse_map = {v: k for k, v in ITEM_MAP.items()}

    df["financial_variable"] = df["item_id"].map(reverse_map)

    # Chỉ giữ các biến tài chính cốt lõi
    df = df[df["financial_variable"].notna()].copy()

    print(f"Số dòng sau mapping : {len(df):,}")

    print(f"Số biến tài chính   : {df['financial_variable'].nunique()}")

    print("\nCác biến tài chính:")

    print(sorted(df["financial_variable"].unique()))

    return df


# ==========================================================
# PIVOT COMPANY YEAR
# ==========================================================


def pivot_company_year(df):

    print("\n" + "=" * 60)
    print("STEP 3 - PIVOT COMPANY YEAR")
    print("=" * 60)

    company_df = df.pivot_table(
        index=["ticker", "fiscal_year"],
        columns="financial_variable",
        values="value_processor",
        aggfunc="first",
    ).reset_index()

    company_df.columns.name = None

    print(f"Số dòng : {len(company_df)}")
    print(f"Số cột  : {len(company_df.columns)}")

    print("\nDanh sách cột:")
    print(company_df.columns.tolist())

    print("\n5 dòng đầu:")
    print(company_df.head())

    return company_df


# ==========================================================
# INTERMEDIATE VARIABLES
# ==========================================================


def add_intermediate_variables(df):

    print("\n" + "=" * 60)
    print("STEP 4 - INTERMEDIATE VARIABLES")
    print("=" * 60)

    required_columns = [
        "short_term_borrowings",
        "long_term_borrowings",
        "cash_and_cash_equivalents",
        "short_term_investments",
        "current_assets",
        "current_liabilities",
        "net_cash_from_operating_activities",
        "capital_expenditure",
        "profit_before_tax",
        "interest_expense",
        "depreciation_and_amortization",
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = 0.0

    # -----------------------------
    # Absolute values
    # -----------------------------

    df["interest_expense_abs"] = df["interest_expense"].abs()

    # -----------------------------
    # Intermediate variables
    # -----------------------------

    df["total_borrowings"] = df["short_term_borrowings"].fillna(0) + df[
        "long_term_borrowings"
    ].fillna(0)

    df["net_debt"] = (
        df["total_borrowings"]
        - df["cash_and_cash_equivalents"].fillna(0)
        - df["short_term_investments"].fillna(0)
    )

    df["working_capital"] = df["current_assets"] - df["current_liabilities"]

    # CAPEX đã mang dấu âm
    df["free_cash_flow"] = df["net_cash_from_operating_activities"].fillna(0) + df[
        "capital_expenditure"
    ].fillna(0)

    df["EBIT_proxy"] = df["profit_before_tax"].fillna(0) + df[
        "interest_expense_abs"
    ].fillna(0)

    df["EBITDA_proxy"] = df["EBIT_proxy"] + df["depreciation_and_amortization"].fillna(
        0
    )

    created = [
        "interest_expense_abs",
        "total_borrowings",
        "net_debt",
        "working_capital",
        "free_cash_flow",
        "EBIT_proxy",
        "EBITDA_proxy",
    ]

    print("Created variables:")

    for col in created:
        print(f"  ✓ {col}")

    return df


# ==========================================================
# LIQUIDITY RATIOS
# ==========================================================


def add_liquidity_ratios(df):

    print("\n" + "=" * 60)
    print("STEP 5 - LIQUIDITY RATIOS")
    print("=" * 60)

    current_liabilities = df["current_liabilities"].replace(0, pd.NA)
    total_assets = df["total_assets"].replace(0, pd.NA)

    df["current_ratio"] = df["current_assets"] / current_liabilities
    df["current_ratio_below_1_flag"] = (df["current_ratio"] < 1).astype(int)
    df["current_ratio_below_1_flag"] = (df["current_ratio"] < 1).astype(int)

    df["quick_ratio"] = (
        df["current_assets"] - df["net_inventory"]
    ) / current_liabilities

    df["cash_ratio"] = (
        df["cash_and_cash_equivalents"] + df["short_term_investments"]
    ) / current_liabilities

    df["working_capital_to_assets"] = df["working_capital"] / total_assets

    df["cfo_to_current_liabilities"] = (
        df["net_cash_from_operating_activities"] / current_liabilities
    )

    print("Created liquidity ratios")

    return df


# ==========================================================
# LEVERAGE & SOLVENCY RATIOS
# ==========================================================


def add_leverage_ratios(df):

    print("\n" + "=" * 60)
    print("STEP 6 - LEVERAGE & SOLVENCY RATIOS")
    print("=" * 60)

    total_assets = df["total_assets"].replace(0, pd.NA)
    equity = df["equity"].replace(0, pd.NA)
    total_borrowings = df["total_borrowings"].replace(0, pd.NA)
    interest_expense = df["interest_expense_abs"].replace(0, pd.NA)
    ebitda = df["EBITDA_proxy"].replace(0, pd.NA)

    # -------------------------------------------------
    # Flags
    # -------------------------------------------------

    df["negative_equity_flag"] = (df["equity"] <= 0).astype(int)

    df["negative_ebitda_flag"] = (df["EBITDA_proxy"] <= 0).astype(int)

    # -------------------------------------------------
    # Ratios
    # -------------------------------------------------

    df["liabilities_to_assets"] = df["total_liabilities"] / total_assets

    df["equity_to_assets"] = df["equity"] / total_assets

    df["debt_to_equity"] = df["total_liabilities"] / equity

    df.loc[df["negative_equity_flag"] == 1, "debt_to_equity"] = pd.NA

    df["borrowings_to_assets"] = df["total_borrowings"] / total_assets

    df["net_debt_to_assets"] = df["net_debt"] / total_assets

    df["short_term_borrowings_share"] = df["short_term_borrowings"] / total_borrowings

    df["interest_coverage"] = df["EBIT_proxy"] / interest_expense

    df["net_debt_to_ebitda"] = df["net_debt"] / ebitda

    df.loc[df["negative_ebitda_flag"] == 1, "net_debt_to_ebitda"] = pd.NA

    print("Created leverage ratios")

    return df


# ==========================================================
# PROFITABILITY RATIOS
# ==========================================================


def add_profitability_ratios(df):

    print("\n" + "=" * 60)
    print("STEP 7 - PROFITABILITY RATIOS")
    print("=" * 60)

    average_total_assets = df["average_total_assets"].replace(0, pd.NA)
    average_equity = df["average_equity"].replace(0, pd.NA)
    revenue = df["net_revenue"].replace(0, pd.NA)

    df["gross_margin"] = df["gross_profit"] / revenue

    df["operating_margin"] = df["operating_profit"] / revenue

    df["net_margin"] = df["net_income_after_tax"] / revenue
    df["negative_net_income_flag"] = (df["net_income_after_tax"] < 0).astype(int)
    df["negative_net_income_flag"] = (df["net_income_after_tax"] < 0).astype(int)

    df["roa"] = df["net_income_after_tax"] / average_total_assets

    df["roe"] = df["net_income_after_tax"] / average_equity

    print("Created profitability ratios")

    return df


# ==========================================================
# OPERATIONAL EFFICIENCY RATIOS
# ==========================================================


def add_efficiency_ratios(df):

    print("\n" + "=" * 60)
    print("STEP 8 - OPERATIONAL EFFICIENCY RATIOS")
    print("=" * 60)

    average_total_assets = df["average_total_assets"].replace(0, pd.NA)

    average_inventory = df["average_inventory"].replace(0, pd.NA)

    average_trade_receivables = df["average_trade_receivables"].replace(0, pd.NA)

    average_trade_payables = df["average_trade_payables"].replace(0, pd.NA)

    cost_of_goods_sold = df["cost_of_goods_sold"].abs()

    df["asset_turnover"] = df["net_revenue"] / average_total_assets

    df["inventory_turnover"] = cost_of_goods_sold / average_inventory

    df["receivables_turnover"] = df["net_revenue"] / average_trade_receivables

    df["payables_turnover"] = cost_of_goods_sold / average_trade_payables

    df["inventory_days"] = 365 / df["inventory_turnover"]

    df["receivable_days"] = 365 / df["receivables_turnover"]

    df["payable_days"] = 365 / df["payables_turnover"]

    df["cash_conversion_cycle"] = (
        df["inventory_days"] + df["receivable_days"] - df["payable_days"]
    )

    print("Created operational efficiency ratios")

    return df


# ==========================================================
# CASH FLOW QUALITY RATIOS
# ==========================================================


def add_cashflow_ratios(df):

    print("\n" + "=" * 60)
    print("STEP 9 - CASH FLOW QUALITY RATIOS")
    print("=" * 60)

    revenue = df["net_revenue"].replace(0, pd.NA)
    average_total_assets = df["average_total_assets"].replace(0, pd.NA)
    total_liabilities = df["total_liabilities"].replace(0, pd.NA)

    cfo = df["net_cash_from_operating_activities"]
    net_income = df["net_income_after_tax"]

    df["cfo_margin"] = cfo / revenue

    df["cfo_to_assets"] = cfo / average_total_assets

    df["cfo_to_liabilities"] = cfo / total_liabilities

    df["fcf_to_assets"] = df["free_cash_flow"] / average_total_assets

    df["accruals_to_assets"] = (net_income - cfo) / average_total_assets

    df["negative_cfo_flag"] = (cfo < 0).astype(int)

    df["cfo_profit_divergence_flag"] = ((net_income > 0) & (cfo < 0)).astype(int)

    print("Created cash flow quality ratios")

    return df


# ==========================================================
# TEMPORAL FEATURES
# ==========================================================

# ==========================================================
# TEMPORAL FEATURES
# ==========================================================


def add_temporal_features(df):

    print("\n" + "=" * 60)
    print("STEP 10A - TEMPORAL FEATURES")
    print("=" * 60)

    df = df.sort_values(["ticker", "fiscal_year"]).copy()

    # ======================================================
    # Previous-year values
    # ======================================================

    df["net_revenue_prev"] = df.groupby("ticker")["net_revenue"].shift(1)

    df["total_assets_prev"] = df.groupby("ticker")["total_assets"].shift(1)

    df["total_liabilities_prev"] = df.groupby("ticker")["total_liabilities"].shift(1)

    df["equity_prev"] = df.groupby("ticker")["equity"].shift(1)

    df["net_income_prev"] = df.groupby("ticker")["net_income_after_tax"].shift(1)

    df["net_inventory_prev"] = df.groupby("ticker")["net_inventory"].shift(1)

    df["trade_receivables_prev"] = df.groupby("ticker")["trade_receivables"].shift(1)

    df["trade_payables_prev"] = df.groupby("ticker")["trade_payables"].shift(1)

    df["liabilities_to_assets_prev"] = df.groupby("ticker")[
        "liabilities_to_assets"
    ].shift(1)

    # Net Margin hiện tại (không phụ thuộc Step 7)

    revenue = df["net_revenue"].replace(0, pd.NA)

    df["net_margin_current"] = df["net_income_after_tax"] / revenue

    df["net_margin_prev"] = df.groupby("ticker")["net_margin_current"].shift(1)

    # ======================================================
    # Average values
    # ======================================================

    df["average_total_assets"] = (df["total_assets"] + df["total_assets_prev"]) / 2

    df["average_equity"] = (df["equity"] + df["equity_prev"]) / 2

    df["average_inventory"] = (df["net_inventory"] + df["net_inventory_prev"]) / 2

    df["average_trade_receivables"] = (
        df["trade_receivables"] + df["trade_receivables_prev"]
    ) / 2

    df["average_trade_payables"] = (
        df["trade_payables"] + df["trade_payables_prev"]
    ) / 2

    print("Created temporal features")

    return df


# ==========================================================
# GROWTH & TREND FEATURES
# ==========================================================


def add_growth_features(df):

    print("\n" + "=" * 60)
    print("STEP 10B - GROWTH & TREND FEATURES")
    print("=" * 60)

    revenue_prev = df["net_revenue_prev"].replace(0, pd.NA)
    assets_prev = df["total_assets_prev"].replace(0, pd.NA)
    liabilities_prev = df["total_liabilities_prev"].replace(0, pd.NA)

    average_assets = df["average_total_assets"].replace(0, pd.NA)

    df["net_revenue_growth_yoy"] = (df["net_revenue"] - revenue_prev) / revenue_prev

    df["total_assets_growth_yoy"] = (df["total_assets"] - assets_prev) / assets_prev

    df["total_liabilities_growth_yoy"] = (
        df["total_liabilities"] - liabilities_prev
    ) / liabilities_prev

    df["net_income_change_to_assets"] = (
        df["net_income_after_tax"] - df["net_income_prev"]
    ) / average_assets

    df["net_margin_change"] = df["net_margin"] - df["net_margin_prev"]

    df["liabilities_to_assets_change"] = (
        df["liabilities_to_assets"] - df["liabilities_to_assets_prev"]
    )

    print("Created growth & trend features")

    return df


# ==========================================================
# STEP 11 - DATA QUALITY FEATURES
# ==========================================================


def add_data_quality_features(df):

    print("\n" + "=" * 60)
    print("STEP 11 - DATA QUALITY FEATURES")
    print("=" * 60)

    # ------------------------------------------------------
    # 1. Number of mapped financial items
    # ------------------------------------------------------
    financial_columns = [
        "capital_expenditure",
        "cash_and_cash_equivalents",
        "cash_and_cash_equivalents_ending",
        "cost_of_goods_sold",
        "current_assets",
        "current_liabilities",
        "depreciation_and_amortization",
        "equity",
        "financial_expenses",
        "financial_income",
        "fixed_assets",
        "general_and_administrative_expenses",
        "gross_profit",
        "income_tax_expense",
        "interest_expense",
        "long_term_borrowings",
        "net_cash_from_financing_activities",
        "net_cash_from_investing_activities",
        "net_cash_from_operating_activities",
        "net_change_in_cash",
        "net_income_after_tax",
        "net_inventory",
        "net_revenue",
        "non_current_assets",
        "non_current_liabilities",
        "operating_profit",
        "operating_profit_before_working_capital_changes",
        "profit_before_tax",
        "receivables",
        "retained_earnings",
        "selling_expenses",
        "short_term_borrowings",
        "short_term_investments",
        "total_assets",
        "total_liabilities",
        "trade_payables",
        "trade_receivables",
    ]

    df["normalized_item_count"] = df[financial_columns].notna().sum(axis=1)

    # ------------------------------------------------------
    # 2. Core Financial Items
    # ------------------------------------------------------
    core_columns = [
        "current_assets",
        "current_liabilities",
        "total_assets",
        "total_liabilities",
        "equity",
        "net_revenue",
        "net_income_after_tax",
        "net_cash_from_operating_activities",
    ]

    df["core_item_count"] = df[core_columns].notna().sum(axis=1)

    df["core_item_coverage_pct"] = df["core_item_count"] / len(core_columns)

    # ------------------------------------------------------
    # 3. Temporal Feature Availability
    # ------------------------------------------------------
    temporal_columns = [
        "average_total_assets",
        "average_equity",
        "average_inventory",
        "average_trade_receivables",
        "average_trade_payables",
        "net_revenue_prev",
        "total_assets_prev",
        "total_liabilities_prev",
        "net_income_prev",
        "net_margin_prev",
        "liabilities_to_assets_prev",
    ]

    df["temporal_features_available_flag"] = (
        df[temporal_columns].notna().all(axis=1).astype(int)
    )

    # ------------------------------------------------------
    # 4. Feature Version
    # ------------------------------------------------------
    df["feature_version"] = "v1.0"

    print("Created data quality features")

    return df


# ==========================================================
# MAIN
# ==========================================================


def main():

    # ------------------------------------------------------
    # STEP 1: Load normalized financial statement
    # ------------------------------------------------------
    df = load_data()

    # ------------------------------------------------------
    # STEP 2: Map item_id -> financial_variable
    # ------------------------------------------------------
    df = map_financial_variable(df)

    # ------------------------------------------------------
    # STEP 3: Company-Year Pivot
    # ------------------------------------------------------
    company_df = pivot_company_year(df)

    # ------------------------------------------------------
    # STEP 4: Intermediate Variables
    # ------------------------------------------------------
    company_df = add_intermediate_variables(company_df)

    # ------------------------------------------------------
    # STEP 5: Liquidity Ratios
    # ------------------------------------------------------
    company_df = add_liquidity_ratios(company_df)

    # ------------------------------------------------------
    # STEP 6: Leverage & Solvency Ratios
    # ------------------------------------------------------
    company_df = add_leverage_ratios(company_df)

    # ------------------------------------------------------
    # STEP 7: Previous-Year & Average Features
    # ------------------------------------------------------
    company_df = add_temporal_features(company_df)

    # ------------------------------------------------------
    # STEP 8: Profitability Ratios
    # ------------------------------------------------------
    company_df = add_profitability_ratios(company_df)

    # ------------------------------------------------------
    # STEP 9: Operational Efficiency Ratios
    # ------------------------------------------------------
    company_df = add_efficiency_ratios(company_df)

    # ------------------------------------------------------
    # STEP 10: Cash Flow Quality Ratios
    # ------------------------------------------------------
    company_df = add_cashflow_ratios(company_df)

    # ------------------------------------------------------
    # STEP 11: Growth & Trend Features
    # ------------------------------------------------------
    company_df = add_growth_features(company_df)

    # ------------------------------------------------------
    # STEP 12: Data Quality Features
    # ------------------------------------------------------
    company_df = add_data_quality_features(company_df)

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------
    print("\n" + "=" * 60)
    print("LAYER 9 COMPLETED")
    print("=" * 60)

    print(
        company_df[
            [
                "ticker",
                "fiscal_year",
                "net_revenue_growth_yoy",
                "total_assets_growth_yoy",
                "total_liabilities_growth_yoy",
                "net_income_change_to_assets",
                "net_margin_change",
                "liabilities_to_assets_change",
            ]
        ].head()
    )

    print("\n" + "=" * 60)
    print("OUTPUT COLUMN CHECK")
    print("=" * 60)

    print(f"Rows: {len(company_df)}")
    print(f"Columns: {len(company_df.columns)}")

    print(
        f"Rows with complete temporal features: "
        f"{company_df['temporal_features_available_flag'].sum()}"
    )

    company_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
