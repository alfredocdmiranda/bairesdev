from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()


urlpatterns = [
    url(r'^api/v1', include(router_v1.urls))
]