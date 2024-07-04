import enum


class PriceTypeEnum(str, enum.Enum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class RecurringTypeEnum(str, enum.Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
