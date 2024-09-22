from django.utils import timezone
import pytz
from datetime import datetime

def set_timezone_aware_dates(instance, user):
    """
    Set the 'date', 'created_at', and 'updated_at' fields to timezone-aware values.
    This function expects the instance to have 'date', 'created_at', and 'updated_at' fields.
    """
    if user.timezone:
        user_timezone = pytz.timezone(user.timezone)
        current_time_in_user_tz = timezone.now().astimezone(user_timezone)
    else:
        # Fall back to UTC if no timezone is set for the user
        current_time_in_user_tz = timezone.now()

    # Set the date to the current date in the user's timezone, at midnight
    instance.date = current_time_in_user_tz

    # Set created_at and updated_at with the current time in the user's timezone
    if not instance.pk:  # Only set created_at if this is a new instance
        instance.created_at = current_time_in_user_tz
    instance.updated_at = current_time_in_user_tz
