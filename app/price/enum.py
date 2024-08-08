from enum import Enum


class PriceTypeEnum(str, Enum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class RecurringTypeEnum(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
