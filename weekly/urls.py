from django.urls import path, re_path, include
from . import views


urlpatterns = [
    # the list of all weeks
    path('', views.week_log, name='main'),

    # edit current week
    re_path(r'^(?P<pk>[0-9]+)/edit/$', views.week_edit, name='week_edit'),

    # Add new week
    path('new/', views.week_new, name='week_new'),
]
