import polars as pl
import sqlite3
import os


def get_budget_entry_view(
    fiscal_year: str, proposed_fiscal_year: str, business_unit_id: str
) -> list | None:
    # establish initial connection which is not concurrent with db app manager
    db_uri = os.getenv("DB_PATH")

    with sqlite3.connect(db_uri) as conn:
        # Enable foreign key constraint
        conn.execute("PRAGMA foreign_keys = ON;")

        def get_sub_totaled_dataframe(**kwargs) -> pl.DataFrame | None:
            table_name = kwargs["table_name"]
            fiscal_year = kwargs["fiscal_year"]
            column_name = kwargs["column_name"]
            business_unit_id = kwargs["business_unit_id"]

            query = """
                SELECT * FROM BudgetEntryAdminView;
            """
            ba = pl.read_database(query, conn, infer_schema_length=None)

            # first get the accounts
            query = f"""
                SELECT *
                FROM {table_name}
            """
            accounts = pl.read_database(query, conn, infer_schema_length=None)
            accounts = accounts.with_columns(
                [
                    pl.col("AccountNo").cast(pl.Utf8).fill_null(""),
                    pl.col("FiscalYear").cast(pl.Utf8).fill_null(""),
                    pl.col("BusinessUnitId")
                    .cast(pl.Utf8)
                    .fill_null("")
                    .str.replace(".0", ""),
                ]
            )
            accounts = accounts.filter(
                (pl.col("FiscalYear") == fiscal_year)
                & (pl.col("BusinessUnitId") == business_unit_id)
            )

            account_group = accounts.group_by("AccountNo").agg(
                pl.sum("Amount").alias("Amount")
            )
            accounts = ba.join(account_group, on="AccountNo", how="left")
            accounts = accounts.filter(pl.col("RAD").is_null())

            # next get the rads
            query = f"""
                SELECT
                    master.FiscalYear,
                    master.BusinessUnitId,
                    master.AccountNo,
                    master.Amount,
                    r.RAD
                FROM {table_name} master
                JOIN {table_name}_Rad master_rad ON master_rad.{table_name}Id = master.Id
                JOIN RAD r ON r.RadId = master_rad.RADID
            """
            rads = pl.read_database(query, conn, infer_schema_length=None)
            rads = rads.with_columns(
                rads["FiscalYear"].cast(pl.String),
                rads["BusinessUnitId"].cast(pl.String),
            )
            rads = rads.filter(
                (pl.col("FiscalYear") == fiscal_year)
                & (pl.col("BusinessUnitId") == business_unit_id)
            )
            rads_group = rads.group_by("RAD").agg(pl.sum("Amount").alias("Amount"))
            rads = ba.join(rads_group, on="RAD", how="left").filter(
                pl.col("RAD").is_not_null()
            )

            # union together
            master = pl.concat([rads, accounts])
            master = master.rename({"Amount": f"{column_name}Total"})

            return master

        # get the two tables actuals and budget
        budgets = get_sub_totaled_dataframe(
            table_name="Budget",
            column_name="Budgets",
            fiscal_year=fiscal_year,
            business_unit_id=business_unit_id,
        )

        actuals = get_sub_totaled_dataframe(
            table_name="JournalEntry",
            column_name="Actuals",
            fiscal_year=fiscal_year,
            business_unit_id=business_unit_id,
        )

        # combine actuals and budget
        merge_cols = [
            "Id",
            "DisplayOrder",
            "AccountNo",
            "Account",
            "RAD",
            "ForecastMultiplier",
            "ForecastComments",
        ]
        actual_to_budget = actuals.join(budgets, on=merge_cols, how="left")

        query = f"""
            SELECT * FROM ProposedBudget
            WHERE FiscalYear = '{proposed_fiscal_year}'
            AND BusinessUnitId = '{business_unit_id}';
        """
        proposed_budget = pl.read_database(query, conn, infer_schema_length=None)
        proposed_budget = proposed_budget.rename({"Id": "ProposedBudgetId"})

        # Step 1: Fill null values in the RAD column before concatenation
        proposed_budget = proposed_budget.with_columns(
            pl.col("RAD")
            .fill_null("NO RAD")
            .alias("RAD_filled")  # Fill nulls in RAD and rename
        )
        actual_to_budget = actual_to_budget.with_columns(
            pl.col("RAD")
            .fill_null("NO RAD")
            .alias("RAD_filled")  # Fill nulls in RAD and rename
        )

        # Step 2: Create the Merge column based on the filled RAD column
        proposed_budget = proposed_budget.with_columns(
            pl.concat_str(["AccountNo", "RAD_filled"], separator=" ").alias("MergeCol")
        )
        actual_to_budget = actual_to_budget.with_columns(
            pl.concat_str(["AccountNo", "RAD_filled"], separator=" ").alias("MergeCol")
        )

        # Final merge operation for forecast, actuals, and budget
        totals = actual_to_budget.join(proposed_budget, on="MergeCol", how="left")
        totals = totals.with_columns(pl.col("DisplayOrder").cast(pl.Float64))
        totals = totals.with_columns(pl.lit(0).alias("IsSubTotal"))

        # get subtotals display order by minimum of each
        counted_accounts = totals.group_by("AccountNo").agg(pl.count().alias("Count"))
        filtered_accounts = counted_accounts.filter(pl.col("Count") >= 2)
        subtotals_display_order = (
            totals.join(
                filtered_accounts.select("AccountNo"), on="AccountNo", how="right"
            )
            .group_by("AccountNo")
            .agg(pl.col("DisplayOrder").min())
            .with_columns((pl.col("DisplayOrder") - 0.1).alias("DisplayOrder"))
        )
        subtotals = (
            totals.filter(
                pl.col("AccountNo").is_in(subtotals_display_order["AccountNo"])
            )
            .group_by(["AccountNo"])
            .agg(
                [
                    pl.sum("ActualsTotal").alias("ActualsTotal"),
                    pl.sum("BudgetsTotal").alias("BudgetsTotal"),
                    pl.sum("ProposedBudget").alias("ProposedBudget"),
                    pl.sum("BusinessCaseAmount").alias("BusinessCaseAmount"),
                    pl.sum("TotalBudget").alias("TotalBudget"),
                ]
            )
        )
        subtotals = subtotals.join(
            subtotals_display_order.select(["AccountNo", "DisplayOrder"]),
            on="AccountNo",
            how="left",
        ).with_columns(
            [
                (pl.col("AccountNo") + pl.lit(" Subtotal")).alias("AccountNo"),
                pl.lit(1).alias("IsSubTotal"),
            ]
        )

        # union merge and subtotal dataframe and create meta data columns
        master = pl.concat([subtotals, totals], how="diagonal").sort("DisplayOrder")
        float_cols = [
            "ActualsTotal",
            "BudgetsTotal",
            "ProposedBudget",
            "BusinessCaseAmount",
        ]
        master = master.with_columns(
            [pl.col(col).fill_null(0).cast(pl.Float64).alias(col) for col in float_cols]
        )

        master = master.with_columns(
            [
                (pl.col("BudgetsTotal") - pl.col("ActualsTotal")).alias("Variance"),
                (pl.col("ActualsTotal") * pl.col("ForecastMultiplier"))
                .fill_null(0)
                .alias("ForecastAmount"),
                (pl.col("BusinessCaseAmount") + pl.col("ProposedBudget")).alias(
                    "TotalBudget"
                ),
                pl.lit(proposed_fiscal_year).alias("FiscalYear"),
                pl.lit(business_unit_id).alias("BusinessUnitId"),
            ]
        )

        cols_to_keep = [
            "IsSubTotal",
            "DisplayOrder",
            "BusinessUnitId",
            "FiscalYear",
            "AccountNo",
            "Account",
            "RAD",
            "ActualsTotal",
            "BudgetsTotal",
            "Variance",
            "ForecastAmount",
            "ProposedBudgetId",
            "ProposedBudget",
            "BusinessCaseName",
            "BusinessCaseAmount",
            "Comments",
            "TotalBudget",
        ]

        master = master.select(cols_to_keep)
        data = master.to_dicts()

        return data


queries = {
    "fetch_all_regular_user_business_unit_ids": lambda user_id: f"""
        SELECT DISTINCT b.BusinessUnitId, b.BusinessUnit
        FROM BusinessUnit b JOIN User_BusinessUnit ub ON ub.BusinessUnitId = b.BusinessUnitId
        WHERE ub.UserId = {user_id} ORDER BY b.BusinessUnitId;
    """,
    "fetch_all_business_unit_ids": """
        SELECT DISTINCT BusinessUnitId, BusinessUnit 
        FROM BusinessUnit ORDER BY BusinessUnitId;
    """,
    "fetch_all_historical_fiscal_years": "SELECT DISTINCT FiscalYear FROM JournalEntry ORDER BY FiscalYear DESC;",
    "fetch_all_proposed_fiscal_years": """
        SELECT DISTINCT 
            'FY' || (CAST(SUBSTR(FiscalYear, 3) AS INTEGER) + 1) AS FiscalYear
        FROM 
            JournalEntry 
        UNION
        SELECT DISTINCT FiscalYear
        FROM "JournalEntry"
        ORDER BY 
            FiscalYear DESC 
    """,
    "fetch_default_historical_fiscal_year": """
        SELECT DISTINCT 
            FiscalYear 
        FROM 
            JournalEntry 
        ORDER BY 
            FiscalYear DESC 
        LIMIT 1;
    """,
    "fetch_all_default_proposed_fiscal_year": """
        SELECT DISTINCT 
            'FY' || (CAST(SUBSTR(FiscalYear, 3) AS INTEGER) + 1) AS FiscalYear
        FROM 
            JournalEntry 
        ORDER BY 
            FiscalYear DESC 
        LIMIT 1;
    """,
    "fetch_all_business_units": "SELECT DISTINCT BusinessUnitId, BusinessUnit FROM BusinessUnit ORDER BY BusinessUnit ASC;",
    "account_actuals_timeline": """
        SELECT 
            j."AccountNo",
            a."Account",
            j."AccountingDate",
            SUM(j."Amount") AS ActualTotal
        FROM "JournalEntry" j JOIN "Account" a ON a."AccountNo" = j."AccountNo"
        WHERE
            "Amount" != 0
        GROUP BY 
            j."AccountNo",
            j."AccountingDate"
    """,
    "budget_pie_chart": """
        SELECT 
            "BusinessUnit",
            SUM(ABS(b."Amount")) AS TotalBudgetByDepartment
        FROM "Budget" b JOIN "BusinessUnit" bu ON bu."BusinessUnitId" = b."BusinessUnitId"
        WHERE "FiscalYear" = 'FY24'
        GROUP BY 
            bu."BusinessUnit"
    """,
    "user_business_units": lambda user_id: f"""
        SELECT
            (
                SELECT ub.Id
                FROM "MasterEmail" me
                JOIN "User_BusinessUnit" ub ON me."Id" = ub."UserId"
                WHERE
                    bu."BusinessUnitId" = ub."BusinessUnitId"
                    AND "UserId" = {user_id}
            ) AS Id,
            bu."BusinessUnitId",
            bu."BusinessUnit",
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM "MasterEmail" me
                    JOIN "User_BusinessUnit" ub ON me."Id" = ub."UserId"
                    WHERE
                        bu."BusinessUnitId" = ub."BusinessUnitId"
                        AND "UserId" = {user_id}
                )
                THEN 1
                ELSE 0
            END AS IsSelected
        FROM "BusinessUnit" bu;
    """,
    "multiview_download": """
        SELECT 
            pb."BusinessUnitId", 
            pb."AccountNo", 
            rt."RADTypeId", 
            r."RADId", 
            '' AS FILLERCOL1,
            pb."Comments",
            '' AS FILLERCOL2,
            '' AS FILLERCOL3,
            pb."ProposedBudget",
            0 AS FILLERCOL3,
            0 AS FILLERCOL4,
            0 AS FILLERCOL5,
            0 AS FILLERCOL6,
            0 AS FILLERCOL7,
            0 AS FILLERCOL8,
            0 AS FILLERCOL9,
            0 AS FILLERCOL10,
            0 AS FILLERCOL11,
            0 AS FILLERCOL12,
            0 AS FILLERCOL13
        FROM
            "ProposedBudget" pb
            JOIN "Rad" r ON r."RAD" = pb."RAD"
            JOIN "RadType" rt ON rt."RADTypeId" = r."RADTypeId"
        WHERE
            "FiscalYear" = :proposed_fy
    """,
    "budget_entry_view": get_budget_entry_view,
    "fetch_all_accounts": """
        SELECT DISTINCT Account
        FROM Account
        WHERE Account NOT IN (SELECT Account FROM BudgetEntryAdminView)
        ORDER BY Account ASC;
    """,
    "fetch_all_rads": """
        SELECT DISTINCT RAD FROM RAD ORDER BY RAD ASC;
    """,
    "fetch_accounts_for_budget_admin_view": """
        SELECT DISTINCT
            vw."Account"
        FROM 
            "vwAccount_RadType_Rad" vw
        WHERE 
            (vw.AccountNo || ' ' || COALESCE(vw.RAD, '')) NOT IN (
                SELECT 
                    ba.AccountNo || ' ' || COALESCE(ba.RAD, '')
                FROM 
                    "BudgetEntryAdminView" ba
            )
            AND vw."AccountNo" IS NOT NULL
        UNION    
        SELECT DISTINCT  "Account"
        FROM "Account"
        WHERE "Account" IS NOT NULL
        ORDER BY vw."Account" ASC;
    """,
    "fetch_rads_by_account": lambda account_no: f"""
        SELECT DISTINCT
            "RAD"
        FROM 
            "vwAccount_RadType_Rad"
        WHERE 
            (AccountNo || ' ' || COALESCE(RAD, '')) NOT IN (
                SELECT 
                    AccountNo || ' ' || COALESCE(RAD, '')
                FROM 
                    "BudgetEntryAdminView"
            )
            AND "Account" IS NOT NULL
            AND "Account" = '{account_no}'
        ORDER BY "RAD" ASC;
    """,
    "validate_budget_entry_admin_view_row": lambda account_rad: f"""
        SELECT DISTINCT
           AccountNo || ' ' || COALESCE(RAD, '') AS Compare
        FROM BudgetEntryAdminView
        WHERE 
            AccountNo || ' ' || COALESCE(RAD, '') = '{account_rad}'
    """,
}
