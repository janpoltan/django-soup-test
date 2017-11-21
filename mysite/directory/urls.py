from django.conf.urls import url
from directory import views

urlpatterns = [
    url(r'^home/$', views.index),
    url(r'^scrape/$', views.scrape),
]
