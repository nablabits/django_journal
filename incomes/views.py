from django.views.generic import ListView
from django.shortcuts import render
from .models import Income, Hour, Customer
from datetime import date
from django.db.models import Sum


class IncomesList(ListView):
    """The default view, an object list ordered by date."""

    model = Income
    queryset = Income.objects.order_by('-date')


def MainView(request):
    """Display several queries to get a more complex view based on tabs."""
    utils = ViewUtils()

    df, details = [], []
    this_month = date.today().month
    for month in range(1, this_month):
        data_month = utils.MonthSummary(month)
        data_by_customer = utils.MonthDropDown(month)
        df.append(data_month)
        details.append(month, data_by_customer)

    last5 = utils.last5

    dict4view = {'df': df,
                 # 'detail': detail,
                 'last5': last5}

    return render(request, 'incomes/complex.html', dict4view)


class ViewUtils(object):
    """Useful queries to use on the views."""

    incomes = Income.objects.filter
    hours = Hour.objects.filter
    last5 = Income.objects.order_by('date').reverse()[:5]

    def MonthSummary(self, month):
        """Create a list with all the values for a single month.

        This list shows the name of the month (str), the hours spent (rouded
        float), the incomes (rounded float) & the ratio (rounded float).
        """
        incomes = self.incomes(date__month=month).aggregate(Sum('cash'))
        hours = self.hours(month=month).aggregate(Sum('dedication'))

        incomes = round(incomes['cash__sum'], 2)
        hours = hours['dedication__sum']
        if hours == 0 or hours is None:
            hours = 0
            ratio = 'NaN'
        else:
            hours = round(hours)
            ratio = round(incomes / hours, 2)

        month_name = date(2018, month, 1).strftime('%B')

        data = (month_name, incomes, hours, ratio)
        return data

    def MonthDropDown(self, month):
        """Show the month's breakdown when row is clicked.

        Continue here.
        """
        incomes = self.incomes(date__month=month)
        hours = self.hours(month=month)
        customers = Customer.objects.all()
        result = []
        for customer in customers:
            income = incomes.filter(who=customer.id).aggregate(Sum('cash'))
            hour = hours.filter(who=customer.id).aggregate(Sum('dedication'))
            data = (customer.name, income, hour)
            result.append(data)
            month_name = date(2018, month, 1).strftime('%B')

        return (result)
