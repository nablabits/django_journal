from django.views.generic import ListView
from django.shortcuts import render
from .models import Income, Hour
from datetime import date
from django.db.models import Sum


class IncomesList(ListView):
    """The default view, an object list ordered by date."""

    model = Income
    queryset = Income.objects.order_by('-date')


def MainView(request):
    """Display several queries to get a more complex view."""
    def month_str(month):
        """Create a list with all the values for a single month."""
        incomes_list = Income.objects.filter(date__month=month)
        incomes = incomes_list.aggregate(Sum('cash'))

        hours_list = Hour.objects.filter(month=month)
        hours = hours_list.aggregate(Sum('dedication'))

        incomes = incomes['cash__sum']
        hours = hours['dedication__sum']
        if hours == 0 or hours is None:
            ratio = 'NaN'
        else:
            ratio = incomes / hours

        data = (month, incomes, hours, ratio)
        return data

    last5 = Income.objects.order_by('date').reverse()[:5]

    df = []
    this_month = date.today().month
    for month in range(1, this_month):
        data = month_str(month)
        df.append(data)

    dict4view = {'df': df,
                 'last5': last5}

    return render(request, 'incomes/complex.html', dict4view)
