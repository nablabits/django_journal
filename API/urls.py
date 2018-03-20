from django.urls import path, re_path, include
from . import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Django API')

router = routers.DefaultRouter()
router.register(r'weekly', views.WeeklyViewSet)
router.register(r'incomes', views.IncomesViewSet)
router.register(r'customer', views.CustomerViewSet)
router.register(r'hours', views.HoursViewSet)


urlpatterns = [
    # API weekly view
    re_path(r'^', include(router.urls)),
    re_path(r'^schema/$', schema_view),
]
