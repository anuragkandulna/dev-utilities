"""
Timezone utility functions for consistent datetime handling across the application.

All timestamps are stored as timezone-aware UTC and rounded to seconds for consistency.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional


def utc_now() -> datetime:
    """
    Get current UTC time as timezone-aware datetime, rounded to seconds.
    
    Returns:
        datetime: Current UTC time with timezone info, rounded to seconds
    """
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_datetime(dt: Optional[datetime] = None) -> datetime:
    """
    Convert a datetime to timezone-aware UTC, rounded to seconds.
    
    Args:
        dt: Datetime to convert. If None, returns current UTC time.
        
    Returns:
        datetime: Timezone-aware UTC datetime rounded to seconds
    """
    if dt is None:
        return utc_now()
    
    # If already timezone-aware, convert to UTC
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    else:
        # Assume naive datetime is UTC
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Round to seconds for consistency
    return dt.replace(microsecond=0)


def utc_from_timestamp(timestamp: float) -> datetime:
    """
    Create timezone-aware UTC datetime from timestamp.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        datetime: Timezone-aware UTC datetime rounded to seconds
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0)


def add_time(dt: datetime, **kwargs) -> datetime:
    """
    Add time to a datetime while maintaining timezone awareness.
    
    Args:
        dt: Base datetime
        **kwargs: Time delta arguments (days, hours, minutes, seconds, etc.)
        
    Returns:
        datetime: New datetime with added time, rounded to seconds
    """
    result = dt + timedelta(**kwargs)
    return result.replace(microsecond=0)


def utc_date_only(dt: Optional[datetime] = None) -> datetime:
    """
    Get a UTC datetime with only date components (year, month, day).
    Time is set to 00:00:00 UTC.
    
    Args:
        dt: Datetime to convert. If None, uses current UTC time.
        
    Returns:
        datetime: UTC datetime with time set to 00:00:00
    """
    if dt is None:
        dt = utc_now()
    
    # Convert to UTC if needed
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    else:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Return date only with time set to 00:00:00
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
