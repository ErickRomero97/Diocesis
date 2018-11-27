# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Publicacion, Empleado, Homilia, Parroquia, Album, Imagen
from .forms import PublicacionForm, PublicacionForm_Editar, HomiliaForm, HomiliaForm_Editar, AlbumForm, ImagenForm
from django.contrib.auth.decorators import login_required

def index(request):
	publicacionForm = PublicacionForm()
	editarForm = PublicacionForm_Editar()	
	form = AuthenticationForm()
	form.fields['username'].widget.attrs['class'] = 'form-control'
	form.fields['password'].widget.attrs['class'] = 'form-control'
	publicaciones = Publicacion.objects.all().order_by('-fecha_pub')[:3]
	context = {
		'publicaciones': publicaciones,
		'form': form,
		'publicacionForm': publicacionForm,
		'editarForm': editarForm
	}
	return render(request, 'index.html', context)

def obispo(request):
	return render(request, 'obispo.html', )

def sacerdote(request):
	return render(request, 'sacerdote.html', )

def publicaciones(request):
	# template = loader.get_template('publicaciones.html')
	editarForm = PublicacionForm_Editar()
	#_inicializar_items()
	publicaciones = Publicacion.objects.all().order_by('-fecha_pub')

	paginator = Paginator(publicaciones, 3)
	page = request.GET.get('page')

	try:
	    items = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    items = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    items= paginator.page(paginator.num_pages)

	context = {
	    'meta_description': '',
	    'meta_keywords': '',
	    'publicaciones':items,
	    'editarForm': editarForm
	}

	return render(request, 'publicaciones.html', context)

def publicacion(request, id):
	editarForm = PublicacionForm_Editar()	
	publicacion = Publicacion.objects.get(pk = id)
	context = {
		'publicacion': publicacion,
		'editarForm': editarForm
	}

	return render(request, 'publicacion.html', context)

def log_in(request):
	publicacionForm = PublicacionForm()
	editarForm = PublicacionForm_Editar()
	form = AuthenticationForm()
	form.fields['username'].widget.attrs['class'] = 'form-control'
	form.fields['password'].widget.attrs['class'] = 'form-control'
	publicaciones = Publicacion.objects.all()[:3]
	context = {
		'publicaciones': publicaciones,
		'form': form,
		'publicacionForm': publicacionForm,
		'editarForm': editarForm
	}
	
	if request.method == 'POST':
		form = AuthenticationForm(data = request.POST)

		if form.is_valid():
			u = request.POST['username']
			p = request.POST['password']

			user = authenticate(username = u, password = p)

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('principal:index'))
				else:
					return render(request, 'index.html', context)
			else:
				return render(request, 'index.html', context)
		else:
			return render(request, 'index.html', context)
	else:
		return HttpResponse('Utilice el metodo POST')

def log_out(request):
	logout(request)
	publicacionForm = PublicacionForm()
	editarForm = PublicacionForm_Editar()	
	form = AuthenticationForm()
	form.fields['username'].widget.attrs['class'] = 'form-control'
	form.fields['password'].widget.attrs['class'] = 'form-control'
	publicaciones = Publicacion.objects.all()[:3]
	context = {
		'publicaciones': publicaciones,
		'form': form,
		'publicacionForm': publicacionForm,
		'editarForm': editarForm
	}

	return render(request, 'index.html', context)

@login_required
def nueva_publicacion(request):
	empleado = Empleado.objects.get(user = request.user.id)
	publicacion = Publicacion()
	publicacion.nombre = request.POST['nombre']
	publicacion.contenido = request.POST['contenido']
	publicacion.empleado = Empleado(empleado.id)
	publicacion.imagen = request.FILES['imagen']
	publicacion.save()

	return HttpResponseRedirect(reverse('principal:index'))

@login_required
def obtener_publicacion(request):
	id = request.GET['idPub']
	publicacion = Publicacion.objects.get(pk = id)

	return JsonResponse({'nombre': publicacion.nombre, 'contenido': publicacion.contenido, 'empleado': publicacion.empleado.id, 'fecha': publicacion.fecha_pub})

@login_required
def editar_publicacion(request):
	id = request.POST['id_pub']
	empleado = Empleado.objects.get(pk = request.POST['empleado'])
	publicacion = Publicacion(pk = id)
	publicacion.nombre = request.POST['nombre']
	publicacion.contenido = request.POST['contenido']

	publicacion.imagen = request.FILES['imagen']

	publicacion.empleado = Empleado(empleado.id)
	publicacion.fecha_pub = request.POST['fecha']

	publicacion.save()

	return HttpResponseRedirect(reverse('principal:index'))

@login_required
def eliminar_publicacion(request, id):
	publicacion = Publicacion.objects.get(pk = id)
	publicacion.delete()

	return HttpResponseRedirect(reverse('principal:index'))

def contacto(request):
	return render(request, 'contactanos.html', )

def homilia(request):
	homilias = Homilia.objects.all().order_by('fecha')
	homiliaForm = HomiliaForm()
	homiliaForm_Editar = HomiliaForm_Editar()

	ctx = {
		'homilias': homilias,
		'homiliaForm': homiliaForm,
		'homiliaForm_Editar': homiliaForm_Editar
	}
	return render(request, 'homilia.html', ctx)

def detalle_homilia(request, id):
	homilia = Homilia.objects.get(pk = id)

	ctx = {
		'homilia': homilia
	}

	return render(request, 'detalleHomilia.html', ctx)

@login_required
def obtener_homilia(request):
	id = request.GET['id']

	homilia = Homilia.objects.get(pk = id)
	ctx = {
		'titulo': homilia.titulo,
		'parroquia': homilia.parroquia.id,
		'fecha': homilia.fecha,
		'hora': homilia.hora,
		'empleado': homilia.empleado.id,
		'contenido': homilia.contenido
	}
	return JsonResponse(ctx)

@login_required
def editar_homilia(request):
	id = request.POST['id_homilia']
	homilia = Homilia.objects.get(pk = id)
	empleado = Empleado.objects.get(pk = request.POST['empleado'])
	parroquia = Parroquia.objects.get(pk = request.POST['parroquia'])

	homilia.titulo = request.POST['titulo']
	homilia.parroquia = Parroquia(parroquia.id)
	homilia.fecha = request.POST['fecha']
	homilia.hora = request.POST['hora']
	homilia.contenido = request.POST['contenido']
	homilia.empleado = Empleado(empleado.id)
	homilia.save()

	return HttpResponseRedirect(reverse('principal:homilia'))

def homiliasXMes(request):
	id = request.GET['id']
	homilias = Homilia.objects.filter(fecha__month = id)
	homiliasMes = []
	botones = ''
	mensaje = 'No hay homilías disponibles.'
	if request.user.is_active:
		for ho in homilias:
			botones = '''
						<a href="" class="btn btn-info btnEditarHomilia" data-toggle="modal" data-target="#editarHomilia" data-id="{}" data-url="../obtener-homilia/">Editar <span class="glyphicon glyphicon-pencil"></span></a>
						<a href="" data-href="../eliminar-homilia/{}/" class="btn btn-danger" data-toggle="modal" data-target="#confirm-delete">Eliminar <span class="glyphicon glyphicon-remove"></span></a>						
					  ''' .format(ho.id, ho.id)

	for h in homilias:
		formato = '''
					<tr>
						<td>{}</td>
						<td>{}</td>
						<td>{}</td>
						<td>{}</td>
						<td style="text-align: center">
							<a href="../detalle-homilia/{}/" class="btn btn-warning">Ver m&aacute;s <span class="glyphicon glyphicon-search"></span></a>
							{}
						</td>
					</tr> 
				''' .format(h.titulo, h.fecha, h.hora, h.parroquia, h.id, botones)
		homiliasMes.append(formato)
		mensaje = ''

	return JsonResponse({'format': homiliasMes, 'msj': mensaje})

@login_required
def nueva_homilia(request):
	homilia = Homilia()
	empleado = Empleado.objects.get(user = request.user.id)

	homilia.titulo = request.POST['titulo']
	homilia.parroquia = Parroquia(request.POST['parroquia'])
	homilia.fecha = request.POST['fecha']
	homilia.hora = request.POST['hora']
	homilia.empleado = Empleado(empleado.id)
	homilia.contenido = request.POST['contenido']
	homilia.save()

	return HttpResponseRedirect(reverse('principal:homilia'))

@login_required
def eliminar_homilia(request, id):
	homilia = Homilia.objects.get(pk = id)
	homilia.delete()

	return HttpResponseRedirect(reverse('principal:homilia'))

def galeria(request):
	albums = Album.objects.all()
	formAlbum = AlbumForm()

	ctx = {
		'albums': albums,
		'formAlbum': formAlbum
	}

	return render(request, 'galeria.html', ctx)


def detalle_album(request, id):
	album = Album.objects.get(pk = id)
	imgForm = ImagenForm()

	ctx = {
		'album': album,
		'imgForm': imgForm
	}

	return render(request, 'detalleAlbum.html', ctx)

@login_required
def nuevo_album(request):
	album = Album()
	album.nombre_album = request.POST['nombre_album']
	album.save()

	return HttpResponseRedirect(reverse('principal:galeria'))

@login_required
def eliminar_album(request, id):
	album = Album.objects.get(pk = id)
	album.delete()

	return HttpResponseRedirect(reverse('principal:galeria'))

@login_required
def agregar_imagen(request):
	imagen = Imagen()
	imagen.imagen = request.FILES['imagen']
	imagen.save()

	idAlbum = request.POST['album']
	album = Album.objects.get(pk = idAlbum)
	album.imagen.add(imagen)

	return HttpResponseRedirect(reverse('principal:detalle_album', args=(idAlbum,)))
