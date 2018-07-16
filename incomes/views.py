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
    cash_incomes = Income.objects.all().aggregate(Sum('cash'))
    tip_incomes = Income.objects.all().aggregate(Sum('tip'))
    total_incomes = cash_incomes['cash__sum'] + tip_incomes['tip__sum']
    total_hours = Hour.objects.all().aggregate(Sum('dedication'))
    total_hours = total_hours['dedication__sum']
    total_ratio = round(total_incomes/ total_hours, 2)

    df, details = [], []
    this_month = date.today().month + 1
    for month in range(1, this_month):
        data_month = utils.MonthSummary(month)
        data_by_customer = utils.MonthDropDown(month)
        df.append(data_month)
        for row in data_by_customer:
            if row is None:
                pass
            else:
                details.append(row)

    last5 = utils.last5

    dict4view = {'df': df,
                 'details': details,
                 'last5': last5,
                 'total_hours': total_hours,
                 'total_incomes': total_incomes,
                 'total_ratio': total_ratio,
                 }

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
        tips = self.incomes(date__month=month).aggregate(Sum('tip'))
        hours = self.hours(month=month).aggregate(Sum('dedication'))

        month_name = date(2018, month, 1).strftime('%B')
        incomes, tips = incomes['cash__sum'], tips['tip__sum']
        hours = hours['dedication__sum']

        if not tips:
            tips = 0
        if not incomes:
            incomes = 0

        total_incomes = round(incomes + tips, 2)

        if hours == 0 or hours is None:
            hours = 0
            ratio = 'NaN'
        else:
            ratio = round(total_incomes / hours, 2)

        data = (month_name, total_incomes, hours, ratio)
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
            tips = incomes.filter(who=customer.id).aggregate(Sum('tip'))
            hour = hours.filter(who=customer.id).aggregate(Sum('dedication'))

            month_name = date(2018, month, 1).strftime('%B')
            income, tips = income['cash__sum'], tips['tip__sum']
            hour = hour['dedication__sum']

            if not tips:
                tips = 0
            if not income:
                income = 0
            if not hour:
                data = None
            else:
                total_income = income + tips
                ratio = round(total_income / hour, 2)
                data = (month_name, customer.name, total_income, hour, ratio)
            result.append(data)
        return result
