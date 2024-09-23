from django.utils import timezone
import pytz

def set_timezone_aware_dates(instance, user, field=None):
    """
    Set the specified field (along with 'created_at' and 'updated_at') to timezone-aware values.
    
    Args:
        instance: The instance whose fields will be updated.
        user: The user whose timezone will be used.
        field: The name of the additional field to update (optional).
    """
    if user.timezone:
        user_timezone = pytz.timezone(user.timezone)
        current_time_in_user_tz = timezone.now().astimezone(user_timezone)
    else:
        current_time_in_user_tz = timezone.now()

    if field:
        setattr(instance, field, current_time_in_user_tz)

    if not instance.pk:  # Only set 'created_at' if this is a new instance
        instance.created_at = current_time_in_user_tz
    instance.updated_at = current_time_in_user_tz
