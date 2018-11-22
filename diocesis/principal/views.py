# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Publicacion, Empleado
from .forms import PublicacionForm, PublicacionForm_Editar

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


def nueva_publicacion(request):
	empleado = Empleado.objects.get(user = request.user.id)
	publicacion = Publicacion()
	publicacion.nombre = request.POST['nombre']
	publicacion.contenido = request.POST['contenido']
	publicacion.empleado = Empleado(empleado.id)
	publicacion.imagen = request.FILES['imagen']
	publicacion.save()

	return HttpResponseRedirect(reverse('principal:index'))

def obtener_publicacion(request):
	id = request.GET['idPub']
	publicacion = Publicacion.objects.get(pk = id)



	return JsonResponse({'nombre': publicacion.nombre, 'contenido': publicacion.contenido, 'empleado': publicacion.empleado.id, 'fecha': publicacion.fecha_pub})

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

def eliminar_publicacion(request, id):
	publicacion = Publicacion.objects.get(pk = id)
	publicacion.delete()

	return HttpResponseRedirect(reverse('principal:index'))