"""Waylay Alarms: apis."""

# import apis into api package
from .about_api import AboutApi
from .alarm_events_api import AlarmEventsApi
from .alarms_api import AlarmsApi
from .alarms_batch_operations_api import AlarmsBatchOperationsApi

__all__ = [
    "AboutApi",
    "AlarmEventsApi",
    "AlarmsApi",
    "AlarmsBatchOperationsApi",
]
