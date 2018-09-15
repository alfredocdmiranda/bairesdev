from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^companies/$', views.CompanyList.as_view(), name='companies_list'),
    url(r'^reviews/$', views.ReviewList.as_view(), name='reviews_list'),
    url(r'^reviews/(?P<pk>[0-9]+)/$', views.ReviewDetails.as_view(), name='reviews_detail'),
]