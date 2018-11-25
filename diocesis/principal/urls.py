from django.conf.urls import url
from . import views

app_name = 'principal'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^obispo/$', views.obispo, name = 'obispo'),
	url(r'^sacerdotes/$', views.sacerdote, name = 'sacerdote'),
	url(r'^contacto/$', views.contacto, name = 'contacto'),
	url(r'^publicaciones/$', views.publicaciones, name = 'publicaciones'),
	url(r'^publicacion/(?P<id>\d+)/$', views.publicacion, name = 'publicacion'),
	url(r'^login/$', views.log_in, name = 'login'),
	url(r'^logout/$', views.log_out, name = 'logout'),
	url(r'^nueva-publicacion/$', views.nueva_publicacion, name = 'nueva_publicacion'),
	url(r'^obtener-publicacion/$', views.obtener_publicacion, name = 'obtener_publicacion'),
	url(r'^editar-publicacion/$', views.editar_publicacion, name = 'editar_publicacion'),
	url(r'^eliminar-publicacion/(?P<id>\d+)/$', views.eliminar_publicacion, name = 'eliminar_publicacion')
]