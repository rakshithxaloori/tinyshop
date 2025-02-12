from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.price.enum import RecurringTypeEnum


def calculate_current_period_end(
    current_period_start: int, interval: RecurringTypeEnum, interval_count: int
) -> int:
    # Convert current_period_start to datetime
    start_datetime = datetime.fromtimestamp(current_period_start)

    if interval == "day":
        end_datetime = start_datetime + timedelta(days=interval_count)
    elif interval == "week":
        end_datetime = start_datetime + timedelta(weeks=interval_count)
    elif interval == "month":
        end_datetime = start_datetime + relativedelta(months=interval_count)
    elif interval == "quarter":
        end_datetime = start_datetime + relativedelta(months=3 * interval_count)
    elif interval == "year":
        end_datetime = start_datetime + relativedelta(years=interval_count)
    else:
        raise ValueError(
            "Invalid interval. Must be 'day', 'week', 'month', 'quarter', or 'year'."
        )

    # Convert the result back to a timestamp (integer)
    return int(end_datetime.timestamp())
