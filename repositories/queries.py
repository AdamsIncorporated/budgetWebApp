import pandas as pd
import sqlite3
import os


def get_budget_entry_view(
    fiscal_year: str, proposed_fiscal_year: str, business_unit_id: str
) -> dict | None:
    # establish initial connection which is not concurrent with db app manager
    db_uri = os.getenv("DB_PATH")

    with sqlite3.connect(db_uri) as conn:
        # Enable foreign key constraint
        conn.execute("PRAGMA foreign_keys = ON;")

        def get_sub_totaled_dataframe(**kwargs) -> pd.DataFrame() | None:
            table_name = kwargs["table_name"]
            fiscal_year = kwargs["fiscal_year"]
            column_name = kwargs["column_name"]
            business_unit_id = kwargs["business_unit_id"]

            query = """
                SELECT * FROM BudgetEntryAdminView WHERE IsActiveTemplate = 1 
            """
            ba = pd.read_sql(query, conn)

            # first get the accounts
            query = f"""
                SELECT * 
                FROM {table_name} 
            """
            accounts = pd.read_sql(
                query,
                conn,
                dtype={"AccountNo": str, "FiscalYear": str, "BusinessUnitId": str},
            )
            accounts["AccountNo"] = accounts["AccountNo"].fillna("").astype(str)
            accounts["FiscalYear"] = accounts["FiscalYear"].fillna("").astype(str)
            accounts["BusinessUnitId"] = (
                accounts["BusinessUnitId"].fillna("").astype(str)
            )
            accounts["BusinessUnitId"] = accounts["BusinessUnitId"].str.replace(
                ".0", ""
            )
            accounts = accounts[
                (accounts["FiscalYear"] == fiscal_year)
                & (accounts["BusinessUnitId"] == business_unit_id)
            ]
            account_group = (
                accounts.groupby(["AccountNo"])["Amount"].sum().reset_index()
            )
            accounts = pd.merge(ba, account_group, on=["AccountNo"], how="left")
            accounts = accounts[~pd.notna(accounts["RAD"])]

            # next get the rads
            query = f"""
                SELECT * 
                FROM {table_name} master 
                JOIN {table_name}_Rad master_rad ON master_rad.{table_name}Id = master.Id
                JOIN RAD r ON r.RadId = master_rad.RADID
            """
            rads = pd.read_sql(query, conn)
            rads = rads[
                (rads["FiscalYear"] == fiscal_year)
                & (rads["BusinessUnitId"] == business_unit_id)
            ]
            rads_group = rads.groupby(["RAD"])["Amount"].sum().reset_index()
            rads = pd.merge(ba, rads_group, on="RAD", how="left")
            rads = rads.dropna(subset="RAD")

            # union together
            master = pd.concat([rads, accounts])
            master.rename(columns={"Amount": f"{column_name}Total"}, inplace=True)

            return master

        # get the two tables actuals and budget
        kwargs = {
            "table_name": "Budget",
            "column_name": "Budgets",
            "fiscal_year": fiscal_year,
            "business_unit_id": business_unit_id,
        }
        budgets = get_sub_totaled_dataframe(**kwargs)

        kwargs = {
            "table_name": "JournalEntry",
            "column_name": "Actuals",
            "fiscal_year": fiscal_year,
            "business_unit_id": business_unit_id,
        }
        actuals = get_sub_totaled_dataframe(**kwargs)

        # combine actuals and budget
        merge_cols = ["DisplayOrder", "AccountNo", "Account", "RAD"]
        actual_to_budget = pd.merge(actuals, budgets, on=merge_cols, how="left")
        

        query = f"SELECT * FROM ProposedBudget WHERE FiscalYear = '{proposed_fiscal_year}' AND BusinessUnitId = '{business_unit_id}';"

        # get proposed budget data
        proposed_budget = pd.read_sql(query, conn)
        proposed_budget.rename(columns={"Id": "ProposedBudgetId"}, inplace=True)

        # get forecast data
        budget_admin_view = pd.read_sql(
            "SELECT * FROM BudgetEntryAdminView WHERE IsActiveTemplate = 1", conn
        )
        forecast = budget_admin_view[
            ["AccountNo", "RAD", "ForecastMultiplier", "ForecastComments"]
        ].copy()

        # final merge operation for forecast, actuals and budget
        pre_merge = pd.merge(
            actual_to_budget,
            proposed_budget,
            on=["AccountNo", "RAD"],
            how="left",
        )
        merge = pd.merge(pre_merge, forecast, on=["AccountNo", "RAD"], how="left")

        # Filter to get only AccountNo with two or more entries
        subtotal = (
            merge.groupby(["AccountNo", "DisplayOrder"])[
                [
                    "ActualsTotal",
                    "BudgetsTotal",
                    "ProposedBudget",
                    "BusinessCaseAmount",
                    "TotalBudget",
                ]
            ]
            .sum()
            .reset_index()
        )

        account_counts = merge["AccountNo"].value_counts()
        valid_accounts = account_counts[account_counts >= 2].index

        # Get subtotal for valid rows that have a two or more RADs
        subtotal_filtered = subtotal[subtotal["AccountNo"].isin(valid_accounts)]
        min_display_order = (
            subtotal.groupby("AccountNo")["DisplayOrder"].min().reset_index()
        )
        subtotal_filtered = subtotal_filtered.merge(
            min_display_order, on="AccountNo", how="left", suffixes=("", "_min")
        )
        subtotal_filtered = subtotal_filtered.reset_index()
        subtotal_filtered["AccountNo"] = (
            subtotal_filtered["AccountNo"].astype(str) + " SubTotal"
        )
        subtotal_filtered = (
            subtotal_filtered.groupby(["AccountNo", "DisplayOrder_min"])[
                [
                    "ActualsTotal",
                    "BudgetsTotal",
                    "ProposedBudget",
                    "BusinessCaseAmount",
                    "TotalBudget",
                ]
            ]
            .sum()
            .reset_index()
        )
        subtotal_filtered["IsSubTotal"] = 1
        subtotal_filtered["DisplayOrder_min"] = (
            subtotal_filtered["DisplayOrder_min"] - 0.1
        )
        subtotal_filtered.rename(
            columns={"DisplayOrder_min": "DisplayOrder"}, inplace=True
        )

        # union merge and subtotal dataframe and create meta data columns
        master = pd.concat([subtotal_filtered, merge])
        master = master.sort_values(by="DisplayOrder")
        float_cols = [
            "ActualsTotal",
            "BudgetsTotal",
            "ProposedBudget",
            "BusinessCaseAmount",
        ]
        master[float_cols] = master[float_cols].fillna(0).astype(float)
        master["Variance"] = (
            master["BudgetsTotal"] - master["ActualsTotal"]
        )
        master["ForecastAmount"] = master["ActualsTotal"] * master["ForecastMultiplier"]
        master["ForecastAmount"] = master["ForecastAmount"].fillna(0).astype(float)
        master["IsSubTotal"] = master["IsSubTotal"].fillna(0).astype(int)
        master["TotalBudget"] = master["BusinessCaseAmount"] + master["ProposedBudget"]
        master["FiscalYear"] = proposed_fiscal_year
        master["BusinessUnitId"] = business_unit_id

        # data presentation for frontend
        cols_to_format = [
            "ActualsTotal",
            "BudgetsTotal",
            "Variance",
            "ForecastAmount",
            "ProposedBudget",
            "BusinessCaseAmount",
            "TotalBudget",
        ]

        def format_number(x):
            if isinstance(x, (int, float)):
                return f"{x:,.2f}"
            return x

        master[cols_to_format] = master[cols_to_format].applymap(format_number)

        cols_to_format = [
            "BusinessCaseName",
            "Comments",
        ]
        master[cols_to_format] = master[cols_to_format].fillna("")

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

        master = master[cols_to_keep]
        master['ProposedBudgetId'].fillna(
            value=-1,
            method=None,
            axis=None,
            inplace=False,
            limit=None,
            downcast=None,
        )

        data = master.to_dict(orient="records")

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
}
