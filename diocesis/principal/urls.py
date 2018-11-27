from django.conf.urls import url
from . import views

app_name = 'principal'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^obispo/$', views.obispo, name = 'obispo'),
	url(r'^homilia/$', views.homilia, name = 'homilia'),
	url(r'^nueva-homilia/$', views.nueva_homilia, name = 'nueva_homilia'),
	url(r'^detalle-homilia/(?P<id>\d+)/$', views.detalle_homilia, name = 'detalle_homilia'),
	url(r'^eliminar-homilia/(?P<id>\d+)/$', views.eliminar_homilia, name = 'eliminar_homilia'),
	url(r'^editar-homilia/$', views.editar_homilia, name = 'editar_homilia'),
	url(r'^obtener-homilia/$', views.obtener_homilia, name = 'obtener_homilia'),
	url(r'^homilia-mes/$', views.homiliasXMes, name = 'homilia_mes'),
	url(r'^sacerdotes/$', views.sacerdote, name = 'sacerdote'),
	url(r'^contacto/$', views.contacto, name = 'contacto'),
	url(r'^publicaciones/$', views.publicaciones, name = 'publicaciones'),
	url(r'^publicacion/(?P<id>\d+)/$', views.publicacion, name = 'publicacion'),
	url(r'^login/$', views.log_in, name = 'login'),
	url(r'^logout/$', views.log_out, name = 'logout'),
	url(r'^nueva-publicacion/$', views.nueva_publicacion, name = 'nueva_publicacion'),
	url(r'^obtener-publicacion/$', views.obtener_publicacion, name = 'obtener_publicacion'),
	url(r'^editar-publicacion/$', views.editar_publicacion, name = 'editar_publicacion'),
	url(r'^eliminar-publicacion/(?P<id>\d+)/$', views.eliminar_publicacion, name = 'eliminar_publicacion'),
	url(r'^galeria/$', views.galeria, name = 'galeria'),
	url(r'^galeria/detalle-album/(?P<id>\d+)/$', views.detalle_album, name = 'detalle_album'),
	url(r'^galeria/nuevo-album/$', views.nuevo_album, name = 'nuevo_album'),
	url(r'^galeria/eliminar-album/(?P<id>\d+)/$', views.eliminar_album, name = 'eliminar_album'),
	url(r'^galeria/agregar-imagen/$', views.agregar_imagen, name = 'agregar_imagen')
]