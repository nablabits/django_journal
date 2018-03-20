from django.views.generic import ListView
from .models import Income


class IncomesList(ListView):
    model = Income
    queryset = Income.objects.order_by('-date')
