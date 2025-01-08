import re
from datetime import datetime
from logger import get_logger

log = get_logger()

# Get today in 28.12.2024 format
today = datetime.now().strftime("%d.%m.%Y")

# Get current year and next year for the "zg 2024/25" part
current_year = datetime.now().year
next_year = (current_year + 1) % 100  # Get the last two digits of the next year

def get_year_pattern():
    # If current month is between jan and jun then the year pattern should be the previous year
    if datetime.now().month < 7:
        return f"zg {current_year - 1}/{current_year % 100:02d}"
    return f"zg {current_year}/{next_year:02d}"

def check_titles(titles):
    year_pattern = get_year_pattern()

    # Capture the date part as a group
    pattern = rf"(?i)^zvezde granda - cela emisija \d+ - {year_pattern} - (\d{{2}}\.\d{{2}}\.\d{{4}})\.$"

    results = []
    for title in titles:
        stripped_title = title.strip()
        match = re.match(pattern, stripped_title, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            log.debug(f"Matched title date: {date_str}")
            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                within_two_days = abs((date_obj - datetime.now()).days) <= 3
                if within_two_days:
                    results.append(f"✅ Match within 2 days: {stripped_title}")
                else:
                    results.append(f"⛔ Date not within 2 days: {stripped_title}")
            except ValueError:
                results.append(f"⛔ Invalid date format: {stripped_title}")
        else:
            log.debug(f"No match for: {stripped_title}")
            results.append(f"⛔ No match: {stripped_title}")

    return results