"""The aggregation data (multiple entries) to show in the views."""

from .models import Weekly
from django.db.models import Avg


class Year2017:
    """Get the 2017 average on rate, time tracked & sleep."""

    weeks2017 = Weekly.objects.filter(
        week_started__year=2017).order_by('-published_date')
    query = weeks2017.aggregate(Avg('week_rate'))
    avg_rate = round(query['week_rate__avg'], 2)
    query = weeks2017.aggregate(Avg('stuff_sleeping_time'))
    avg_sleep = round(query['stuff_sleeping_time__avg'], 2)
    query = weeks2017.aggregate(Avg('time_tracked'))
    avg_timetk = round(query['time_tracked__avg'], 2)


class Year2018:
    """Get the 2018 average on rate, time tracked & sleep."""

    weeks2018 = Weekly.objects.filter(
        week_started__year=2018).order_by('-published_date')
    query = weeks2018.aggregate(Avg('week_rate'))
    avg_rate = round(query['week_rate__avg'], 2)
    query = weeks2018.aggregate(Avg('stuff_sleeping_time'))
    avg_sleep = round(query['stuff_sleeping_time__avg'], 2)
    query = weeks2018.aggregate(Avg('time_tracked'))
    avg_timetk = round(query['time_tracked__avg'], 2)
