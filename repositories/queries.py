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
    """
}
