from django.urls import path
from . import views

urlpatterns = [
    path('', views.dispatcher, name='root'),
]
