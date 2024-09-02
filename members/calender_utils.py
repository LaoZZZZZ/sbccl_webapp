import datetime

# Find the current active shcool year based on current time.
# if it's the first half of the year, then the current school year should be
# current_year -1, current_year. Otherwise, the current school year should be
# current_year, current_year + 1
def find_current_school_year():
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    # For next academic year.
    if current_month >= 7:
        return (current_year, current_year + 1)
    else:
        return (current_year - 1, current_year)