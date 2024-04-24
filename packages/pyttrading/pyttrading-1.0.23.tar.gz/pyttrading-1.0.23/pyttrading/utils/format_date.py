from datetime import datetime
import pytz

def format_date_str(date :str = None):

    timezone = pytz.timezone("America/New_York")
    
    if date is None:
        date = datetime.now(tz=timezone)
    else:
        date = timezone.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

    return date