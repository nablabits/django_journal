from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Weekly
from .forms import PostForm
from django.db.models import Avg
from .avgfn import Year2017, Year2018


def week_log(request):
    """Show the quick view."""

    # Extract all the entries on db and sort by date
    weekly_list = Weekly.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')

    # 2017 averages
    weeks2017 = Weekly.objects.filter(
        week_started__year=2017).order_by('-published_date')
    query = weeks2017.aggregate(Avg('week_rate'))
    avg_rate = round(query['week_rate__avg'], 2)
    query = weeks2017.aggregate(Avg('stuff_sleeping_time'))
    avg_sleep = round(query['stuff_sleeping_time__avg'], 2)
    query = weeks2017.aggregate(Avg('time_tracked'))
    avg_timetk = round(query['time_tracked__avg'], 2)

    # 2018 averages
    weeks2018 = Weekly.objects.filter(
        week_started__year=2018).order_by('-published_date')
    query = weeks2018.aggregate(Avg('week_rate'))
    avg_rate_2018 = round(query['week_rate__avg'], 2)
    query = weeks2018.aggregate(Avg('stuff_sleeping_time'))
    avg_sleep_2018 = round(query['stuff_sleeping_time__avg'], 2)
    query = weeks2018.aggregate(Avg('time_tracked'))
    avg_timetk_2018 = round(query['time_tracked__avg'], 2)


    # the dictionary we'll use in the view
    dict_4_view = {'weekly_list': weekly_list,
                   'avg_rate': avg_rate,
                   'avg_sleep': avg_sleep,
                   'avg_timetk': avg_timetk,
                   'avg_rate_2018': avg_rate_2018,
                   'avg_sleep_2018': avg_sleep_2018,
                   'avg_timetk_2018': avg_timetk_2018,
                   'weeks2017': weeks2017,
                   'weeks2018': weeks2018,
                   }

    # render the page using the correct template
    return render(request, 'weekly/content.html', dict_4_view)


def week_new(request):
    """Create a new blank week entry."""
    if request.method == "POST":
        """ When coming from edit view, save the changes (if they are valid)
        and jump to weekly list"""
        form = PostForm(request.POST)

        if form.is_valid():
            week = form.save(commit=False)
            week.published_date = timezone.now()
            week.save()
            return redirect('week_edit', pk=week.pk)

    else:
        """ We come from anywhere else, so open an empty form"""
        form = PostForm()
    return render(request, 'weekly/weekly_edit.html',
                  {'form': form})


def week_edit(request, pk):
    """Edit an already created entry."""
    week = get_object_or_404(Weekly, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=week)
        if form.is_valid():
            form.save()
    else:
        form = PostForm(instance=week)
    return render(request, 'weekly/weekly_edit.html',
                  {'form': form})
