from django.conf.urls import url
from . import views

app_name = 'principal'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^obispo$', views.obispo, name = 'obispo'),
	url(r'^sacerdotes$', views.sacerdote, name = 'sacerdote'),
]