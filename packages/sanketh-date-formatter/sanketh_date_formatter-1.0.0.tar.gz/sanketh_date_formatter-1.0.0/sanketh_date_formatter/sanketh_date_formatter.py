from datetime import datetime

def format_date(date_str):
    try:
        # Parsing input date string into datetime object
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d')  # Example format: YYYY-MM-DD
    except ValueError:
        try:
            parsed_date = datetime.strptime(date_str, '%d/%m/%Y')  # Example format: DD/MM/YYYY
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_str, '%m/%d/%Y')  # Example format: MM/DD/YYYY
            except ValueError:
                return "Invalid date format. Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY"
    
    # Mapping month numbers to English words
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    
    # Extracting day, month, and year components
    day = parsed_date.day
    month = months[parsed_date.month]
    year = parsed_date.year
    
    # Handling ordinal numbers for days
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Constructing the English date string
    formatted_date = f"{day}{suffix} of {month} {year}"
    
    return formatted_date

# Example usage:
date_str = "2024-04-12"
formatted_date = format_date(date_str)
print(formatted_date)  # Output: 12th of April 2024
