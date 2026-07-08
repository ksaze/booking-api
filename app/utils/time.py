from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def ist_now() -> datetime:
    return datetime.now(IST)


def to_ist(dt: datetime) -> datetime:
    """
    Convert an aware datetime to IST.
    """
    if dt.tzinfo is None:
        raise ValueError("Datetime must include timezone information.")

    return dt.astimezone(IST)


def to_iso8601(dt: datetime) -> str:
    return dt.isoformat()
