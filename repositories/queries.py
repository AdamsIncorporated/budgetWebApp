import pandas as pd
import sqlite3
import os


def get_budget_entry_view(
    fiscal_year: str, proposed_fiscal_year: str, business_unit_id: str
) -> dict | None:
    def get_sub_totaled_dataframe(
        table_name: str, column_name: str, fiscal_year: str, business_unit_id: str
    ) -> pd.DataFrame() | None:
        db_uri = os.getenv('DB_PATH')
        conn = sqlite3.connect(db_uri)

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
        accounts["BusinessUnitId"] = accounts["BusinessUnitId"].fillna("").astype(str)
        accounts["BusinessUnitId"] = accounts["BusinessUnitId"].str.replace(".0", "")
        accounts = accounts[
            (accounts["FiscalYear"] == fiscal_year)
            & (accounts["BusinessUnitId"] == business_unit_id)
        ]
        account_group = accounts.groupby(["AccountNo"])["Amount"].sum().reset_index()
        accounts = pd.merge(ba, account_group, on="AccountNo", how="left")
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

        # Filter to get only AccountNo with two or more entries
        subtotal = (
            rads.groupby(["AccountNo", "DisplayOrder"])["Amount"].sum().reset_index()
        )
        account_counts = rads["AccountNo"].value_counts()
        valid_accounts = account_counts[account_counts >= 2].index

        # Get subtotal for valid rows that have a two or more RADs
        subtotal_filtered = subtotal[subtotal["AccountNo"].isin(valid_accounts)]
        max_display_order = (
            subtotal.groupby("AccountNo")["DisplayOrder"].max().reset_index()
        )
        subtotal_filtered = subtotal_filtered.merge(
            max_display_order, on="AccountNo", how="left", suffixes=("", "_max")
        )
        subtotal_filtered = subtotal_filtered.reset_index()
        subtotal_filtered["AccountNo"] = (
            subtotal_filtered["AccountNo"].astype(str) + " SubTotal"
        )
        subtotal_filtered = subtotal_filtered.groupby(
            ["AccountNo", "DisplayOrder_max"]
        )["Amount"].sum()
        subtotal_filtered = subtotal_filtered.reset_index()
        subtotal_filtered["IsSubTotal"] = 1

        # set display order of subtotal row
        subtotal_filtered["DisplayOrder_max"] = (
            subtotal_filtered["DisplayOrder_max"] + 0.1
        )
        subtotal_filtered.rename(
            columns={"DisplayOrder_max": "DisplayOrder"}, inplace=True
        )

        # combine rad and subtotal dataframe
        sub_total_rads = pd.concat([subtotal_filtered, rads])
        sub_total_rads = sub_total_rads.sort_values(by="DisplayOrder")

        # finally combine with the accounts dataframe
        master = pd.concat([sub_total_rads, accounts])
        master = master.sort_values(by="DisplayOrder")
        master = master[
            ["IsSubTotal", "DisplayOrder", "AccountNo", "Account", "RAD", "Amount"]
        ]
        master["IsSubTotal"] = master["IsSubTotal"].fillna(0)
        master.rename(columns={"Amount": f"{column_name}Total"}, inplace=True)

        return master

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
    actual_to_budget = pd.merge(actuals, budgets, on="DisplayOrder", how="left")
    actual_to_budget = actual_to_budget[
        [
            "IsSubTotal_x",
            "DisplayOrder",
            "AccountNo_x",
            "Account_x",
            "RAD_x",
            "ActualsTotal",
            "BudgetsTotal",
        ]
    ]
    actual_to_budget.columns = actual_to_budget.columns.str.replace(
        "_x", "", regex=False
    )
    actual_to_budget["Variance"] = (
        actual_to_budget["BudgetsTotal"] - actual_to_budget["ActualsTotal"]
    )

    query = f"SELECT * FROM ProposedBudget WHERE FiscalYear = '{proposed_fiscal_year}' AND BusinessUnitId = '{business_unit_id}';"
    
    # get proposed budget data
    db_uri = os.getenv('DB_PATH')
    conn = sqlite3.connect(db_uri)
    proposed_budget = pd.read_sql(query, conn)
    proposed_budget.rename(columns={"Id": "ProposedBudgetId"}, inplace=True)

    # combine results into a merge view 
    budget_admin_view = pd.read_sql(
        "SELECT * FROM BudgetEntryAdminView WHERE IsActiveTemplate = 1", conn
    )
    forecast = budget_admin_view[
        ["AccountNo", "RAD", "ForecastMultiplier", "ForecastComments"]
    ].copy()
    merge = pd.merge(
        actual_to_budget,
        proposed_budget,
        on=["AccountNo", "RAD", "IsSubTotal"],
        how="left",
    )
    merge = pd.merge(merge, forecast, on=["AccountNo", "RAD"], how="left")
    merge["ForecastAmount"] = merge["ActualsTotal"] * merge["ForecastMultiplier"]
    merge['FiscalYear'] = proposed_fiscal_year
    merge['BusinessUnitId'] = business_unit_id
    
    def format_number(x):
        if isinstance(x, (int, float)):  # Check if x is a number
            return f"{x:,.2f}"  # Format number with commas and two decimals
        return x

    merge = merge.fillna("")
    merge = merge.applymap(format_number)
    
    data = merge.to_dict(orient='records')
    
    return data


queries = {
    "fetch_all_fiscal_years": "SELECT DISTINCT FiscalYear FROM JournalEntry ORDER BY FiscalYear ASC;",
    "fetch_all_business_units": "SELECT DISTINCT BusinessUnitId, BusinessUnit FROM BusinessUnit ORDER BY BusinessUnit ASC;",
    "budget": lambda proposed_fy, fy, business_unit_id: f"""
        WITH
            Variables AS (
                SELECT
                    '{proposed_fy}' AS ProposedFY,
                    '{fy}' AS FY,
                    '{business_unit_id}' AS BusinessUnitId
            ),
            ActualData AS (
                SELECT "AccountNo", SUM("Amount") AS Actual
                FROM "JournalEntry"
                WHERE
                    "BusinessUnitId" = (
                        SELECT BusinessUnitId
                        FROM Variables
                    )
                    AND "FiscalYear" = (
                        SELECT FY
                        FROM Variables
                    )
                    AND "Amount" != 0
                GROUP BY
                    "AccountNo"
            ),
            BudgetData AS (
                SELECT "AccountNo", SUM("Amount") AS Budget
                FROM "Budget"
                WHERE
                    "BusinessUnitId" = (
                        SELECT BusinessUnitId
                        FROM Variables
                    )
                    AND "FiscalYear" = (
                        SELECT FY
                        FROM Variables
                    )
                    AND "Amount" != 0
                GROUP BY
                    "AccountNo"
            ),
            ProposedData AS (
                SELECT
                    "Id",
                    "AccountNo",
                    "ProposedBudget",
                    "BusinessCaseName",
                    "BusinessCaseAmount",
                    "TotalBudget",
                    "Comments"
                FROM "ProposedBudget"
                WHERE
                    "FiscalYear" = (
                        SELECT ProposedFY
                        FROM Variables
                    )
            ),
            ForecastData AS (
                SELECT "ForecastAmount", "AccountNo"
                FROM "Forecast"
                WHERE
                    "BudgetId" = (
                        SELECT FY
                        FROM Variables
                    )
            )
        SELECT DISTINCT
            p."Id",
            (SELECT ProposedFy FROM Variables) AS "FiscalYear",
            (SELECT BusinessUnitId FROM Variables) AS "BusinessUnitId",
            ba."AccountNo",
            ba."Account",
            printf(
                '%,.2f',
                COALESCE(a.Actual, 0)
            ) AS Actual,
            printf(
                '%,.2f',
                COALESCE(b.Budget, 0)
            ) AS Budget,
            printf(
                '%,.2f',
                COALESCE(b.Budget, 0) - COALESCE(a.Actual, 0)
            ) AS Variance,
            printf(
                '%.2f%%',
                ROUND(
                    CASE
                        WHEN COALESCE(a.Actual, 0) = 0 THEN 0
                        ELSE (
                            (
                                COALESCE(b.Budget, 0) - COALESCE(a.Actual, 0)
                            ) / COALESCE(a.Actual, 0)
                        )
                    END * 100,
                    2
                )
            ) AS Percent,
            f."ForecastAmount",
            p."ProposedBudget",
            p."BusinessCaseName",
            p."BusinessCaseAmount",
            p."TotalBudget",
            p."Comments"
        FROM
            "Budget_Account" ba
            LEFT JOIN ActualData a ON ba."AccountNo" = a."AccountNo"
            LEFT JOIN BudgetData b ON ba."AccountNo" = b."AccountNo"
            LEFT JOIN ProposedData p ON ba."AccountNo" = p."AccountNo"
            LEFT JOIN ForecastData f ON ba."AccountNo" = f."AccountNo"
        WHERE
            ba."IsActiveTemplate" = 1
            AND ba."IsTotalAccount" = 0
        ORDER BY ba."DisplayOrder" ASC;
    """,
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
