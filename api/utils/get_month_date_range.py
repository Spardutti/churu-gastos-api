from datetime import datetime, timedelta

def get_month_date_range(year: int, month: int):
    """
    Given a year and month, return the start and end date of that month.
    """
    start_date = datetime(int(year), int(month), 1)
    # Calculate the first day of the next month
    next_month = start_date.replace(day=28) + timedelta(days=4)
    end_date = next_month.replace(day=1)
    return start_date, end_date
