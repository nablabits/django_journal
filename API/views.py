from weekly.models import Weekly
from incomes.models import Income, Hour, Customer
from rest_framework import viewsets
from .serializers import HoursSerializer, CustomerSerializer
from .serializers import WeeklySerializer, IncomesSerializer


class WeeklyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Weekly.objects.all().order_by('-published_date')
    serializer_class = WeeklySerializer


class HoursViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Hour.objects.all()
    serializer_class = HoursSerializer


class IncomesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Income.objects.all().order_by('-date')
    serializer_class = IncomesSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-date')
    serializer_class = CustomerSerializer
