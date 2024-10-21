from datetime import datetime

def get_fiscal_year() -> str:
    today = datetime.today()
    current_year = today.year

    # Check if today's date is before or after October 1st
    fiscal_year_start = datetime(current_year, 10, 1)
    
    # Determine the fiscal year
    if today < fiscal_year_start:
        fiscal_year = current_year - 1
    else:
        fiscal_year = current_year

    # Get the last two digits of the fiscal year and return in 'FYXX' format
    return f"FY{str(fiscal_year + 1)[-2:]}"