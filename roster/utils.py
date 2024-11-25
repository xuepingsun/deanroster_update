# utils.py
from datetime import datetime
from django import template
register = template.Library()

# def extract_year(date_str):
#     if date_str and date_str != '0000':
#         return int(date_str[:4])
#     return None

# utils.py (continued)
from .models import DeanBasic

def extract_year(date_string):
    """
    Extracts the year from a date string in the format 'YYYY' or 'YYYY-MM'.
    Returns None if the string is invalid or missing.
    """
    try:
        if int(date_string[:4]) >=1990:
            return yr
    except:
        return None

# def get_dean_tenures():
#     dean_tenures = []
#     deans = DeanBasic.objects.all()
#     for dean in deans:
#         st_year = extract_year(dean.st_year_mon)
#         end_year = extract_year(dean.end_year_mon)
#
#         # If end_year is missing or '0000', assume current year
#         if not end_year or end_year == 0:
#             end_year = datetime.now().year
#
#         if st_year:
#             dean_tenures.append((st_year, end_year))
#     return dean_tenures

def get_missing_years(dean_tenures,tart_year=2000, end_year=2024):
    all_years = set(range(start_year, end_year + 1))
    covered_years = set()
    # dean_tenures = get_dean_tenures()

    for st_year, end_year in dean_tenures:
        covered_years.update(range(st_year, end_year + 1))

    missing_years = sorted(all_years - covered_years)
    return missing_years

# @register.simple_tag
def get_completeness_percentage(start_year=2000, end_year=2024):
    dean_tenures = []
    deans = DeanBasic.objects.all()
    for dean in deans:
        st_year = extract_year(dean.st_year_mon)
        end_year = extract_year(dean.end_year_mon)

        # If end_year is missing or '0000', assume current year
        if not end_year or end_year == 0:
            end_year = datetime.now().year

        if st_year:
            dean_tenures.append((st_year, end_year))

    total_years = end_year - start_year + 1
    missing_years = get_missing_years(dean_tenures,start_year, end_year)
    covered_years = total_years - len(missing_years)

    completeness_percentage = (covered_years / total_years) * 100
    return round(completeness_percentage, 2)
