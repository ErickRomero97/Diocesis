from django.conf.urls import url
from . import views

app_name = 'principal'

urlpatterns = [
	url(r'^$', views.index, name = 'index'),

	url(r'^empleado/$', views.empleado, name = 'empleado'),
	url(r'^empleado/guardar/$', views.empleado_guardar, name='empleado_guardar'),
	url(r'^empleado/desactivar/$', views.empleado_desactivar, name='empleado_desactivar'),
	url(r'^empleado/(?P<pk>\d+)/editar/$', views.empleado_editar, name='empleado_editar'),
	url(r'^empleado/editar_guardar/$', views.empleado_editar_guardar, name='empleado_editar_guardar'),

	url(r'^estudio/$', views.estudio, name = 'estudio'),
	url(r'^estudio/guardar/$', views.estudio_guardar, name='estudio_guardar'),
	url(r'^estudio/eliminar/$', views.estudio_eliminar, name='estudio_eliminar'),
	url(r'^estudio/(?P<pk>\d+)/editar/$', views.estudio_editar, name='estudio_editar'),
	url(r'^estudio/editar_guardar/$', views.estudio_editar_guardar, name='estudio_editar_guardar'),

	url(r'^obispo/$', views.obispo, name = 'obispo'),
	url(r'^obispo/(?P<pk>\d+)/ver/$', views.obispo_ver, name='obispo_ver'),
	url(r'^obispo/guardar/$', views.obispo_guardar, name='obispo_guardar'),
	url(r'^obispo/(?P<pk>\d+)/$', views.obispo_editar, name='obispo_editar'),
	url(r'^obispo/editar_guardar/$', views.obispo_editar_guardar, name='obispo_editar_guardar'),
	url(r'^obispo/desactivar/$', views.obispo_desactivar, name = 'obispo_desactivar'),

	url(r'^parroquia/$', views.parroquia, name = 'parroquia'),
	url(r'^parroquia/(?P<pk>\d+)/ver/$', views.parroquia_ver, name='parroquia_ver'),
	url(r'^parroquia/guardar/$', views.parroquia_guardar, name='parroquia_guardar'),
	url(r'^parroquia/(?P<pk>\d+)/$', views.parroquia_editar, name='parroquia_editar'),
	url(r'^parroquia/editar_guardar/(?P<pk>\d+)/$', views.parroquia_editar_guardar, name='parroquia_editar_guardar'),
	url(r'^parroquia/desactivar/(?P<pk>\d+)/$', views.parroquia_desactivar, name = 'parroquia_desactivar'),

	url(r'^parroquia_admin/$', views.parroquia_admin, name = 'parroquia_admin'),
	url(r'^parroquia_admin/guardar/$', views.parroquia_admin_guardar, name='parroquia_admin_guardar'),
	url(r'^parroquia_admin/desactivar/$', views.parroquia_admin_desactivar, name='parroquia_admin_desactivar'),
	url(r'^parroquia_admin/(?P<pk>\d+)/editar/$', views.parroquia_admin_editar, name='parroquia_admin_editar'),
	url(r'^parroquia_admin/editar_guardar/$', views.parroquia_admin_editar_guardar, name='parroquia_admin_editar_guardar'),

	url(r'^pastoral/$', views.pastoral, name = 'pastoral'),
	url(r'^pastoral/guardar/$', views.pastoral_guardar, name='pastoral_guardar'),
	url(r'^pastoral/(?P<pk>\d+)/$', views.pastoral_editar, name='pastoral_editar'),
	url(r'^pastoral/editar_guardar/$', views.pastoral_editar_guardar, name='pastoral_editar_guardar'),
	url(r'^pastoral/desactivar/$', views.pastoral_desactivar, name = 'pastoral_desactivar'),

	url(r'^sacerdote/$', views.sacerdote, name = 'sacerdote'),
	url(r'^sacerdote/(?P<pk>\d+)/ver/$', views.sacerdote_ver, name='sacerdote_ver'),
	url(r'^sacerdote/(?P<pk>\d+)/$', views.sacerdote_editar, name='sacerdote_editar'),
	url(r'^sacerdote/editar_guardar/(?P<pk>\d+)/$', views.sacerdote_editar_guardar, name='sacerdote_editar_guardar'),
	url(r'^sacerdote/desactivar/(?P<pk>\d+)/$', views.sacerdote_desactivar, name = 'sacerdote_desactivar'),


	url(r'^usuario/$', views.usuario, name = 'usuario'),
	url(r'^usuarios/guardar/$', views.usuarios_guardar, name='usuarios_guardar'),
	url(r'^usuarios/desactivar/$', views.usuarios_desactivar, name='usuarios_desactivar'),
	url(r'^usuarios/(?P<pk>\d+)/editar/$', views.usuarios_editar, name='usuarios_editar'),
	url(r'^usuarios/editar_guardar/$', views.usuario_editar_guardar, name='usuario_editar_guardar'),


	

	

	





	url(r'^homilia/$', views.homilia, name = 'homilia'),
	url(r'^nueva-homilia/$', views.nueva_homilia, name = 'nueva_homilia'),
	url(r'^detalle-homilia/(?P<id>\d+)/$', views.detalle_homilia, name = 'detalle_homilia'),
	url(r'^eliminar-homilia/(?P<id>\d+)/$', views.eliminar_homilia, name = 'eliminar_homilia'),
	url(r'^editar-homilia/$', views.editar_homilia, name = 'editar_homilia'),
	url(r'^obtener-homilia/$', views.obtener_homilia, name = 'obtener_homilia'),
	url(r'^homilia-mes/$', views.homiliasXMes, name = 'homilia_mes'),



	

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