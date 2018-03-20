from django.urls import path, re_path
from .views import IncomesList

urlpatterns = [
    path('', IncomesList.as_view(template_name='income_list'),
         name='incomes'),
]
