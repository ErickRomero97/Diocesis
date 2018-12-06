# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.defaultfilters import timesince, linebreaks

def index(request):
	if request.user.id:
		empleado = Empleado.objects.get(pk = request.user.id)
		publicacionForm = PublicacionForm(initial={'empleado': empleado})
	else:
		publicacionForm = PublicacionForm()

	for field in publicacionForm.fields:
		publicacionForm.fields[field].widget.attrs['class']='form-control'


	form = AuthenticationForm()
	form.fields['username'].widget.attrs['class'] = 'form-control'
	form.fields['username'].widget.attrs['autofocus'] = 'True'
	form.fields['password'].widget.attrs['class'] = 'form-control'

	publicaciones = Publicacion.objects.all().order_by('-fecha_pub')[:3]

	context = {
		'publicaciones': publicaciones,
		'form': form,
		'publicacionForm': publicacionForm,
	}
	return render(request, 'index.html', context)


#________________________________Vistas del Administrador del Parroquias___________________________

def parroquia_admin(request):
	empleado=Empleado.objects.filter(estado_obispo= False, estado_sacerdote=True,estado=True)
	lista=[]
	for s in empleado:
		if not Parroquia.objects.filter(empleado=s).exists():
			lista.append(int(s.id))

	form= ParroquiaForm()
	form.fields['empleado'].queryset= Empleado.objects.filter(id__in=lista)
	form.fields['empleado'].label= 'Seleccioné el Sacerdote'
	form.fields['municipio'].label= 'Seleccioné el Municipio'
	form.fields['pastoral'].label= 'Seleccioné las Pastorales'
	form.fields['descripcion'].label= 'Descripción de la Parroquia'

	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	parroquia= Parroquia.objects.all()
	activo = []
	for e in parroquia:
		if e.estado:
			activo.append('si')
		else:
			activo.append('no')
	data = {
		'parroquia': zip(parroquia, activo),
		'form':form
	}
	return render(request, 'parroquia_admin.html',data )


@login_required()
def parroquia_admin_guardar(request):
	if request.method == 'POST':
		form = ParroquiaForm(data=request.POST,files=request.FILES)

		if form.is_valid():
			p =form.save()

			parroquia='''
				<tr>
					<td>%s</td>
					<td>%s</td>
					<td>%s</td>
					<td><span id="estado-%s">%s</span></td>
					<td>
						<div class="btn-group">
						 	<button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>
							</button>
							<ul class="dropdown-menu">
								<a  style="margin-left:30px; "
								    class="btn btn-info" href=""><span class="glyphicon glyphicon-refresh"></span> Actualizar</a>
								<button class="btn btn-danger btn-Aparroquia"
										data-id="%s"
										data-url=""
										style="margin-left:30px; margin-top:5px">Desactivar</button>		
							</ul>
						</div>
					</td>
					<td>%s %s</td>
				</tr>
			'''% (p.nombre,p.telefono,p.direccion,p.id,p.estado,p.id,p.empleado.nombre,p.empleado.apellido)
			return JsonResponse({'response':parroquia})
		else:
			return render(request, 'parroquia_admin.html',{'form': form})


@login_required()
def parroquia_admin_desactivar(request):
	id = request.GET.get('id')
	u = Parroquia.objects.get(pk=id)
	d = Parroquia.objects.filter(pk=id,estado=True)

	if d:
		u.estado= False
		u.save()
		action='Activar'
		valor='False'
	else:
		u.estado= True
		u.save()
		action='Desactivar'
		valor='True'
	return JsonResponse({'action':action,'valor':valor})


@login_required
def parroquia_admin_editar(request, pk):
	p= Parroquia.objects.get(pk=int(pk))
	form = ParroquiaForm(instance=p)
	form.fields['empleado'].label= 'Seleccioné el Sacerdote'
	form.fields['municipio'].label= 'Seleccioné el Municipio'
	form.fields['pastoral'].label= 'Seleccioné las Pastorales'
	form.fields['descripcion'].label= 'Descripción de la Parroquia'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	parroquia= Parroquia.objects.all()
	activo = []
	for e in parroquia:
		if e.estado:
			activo.append('si')
		else:
			activo.append('no')
	
	data ={
		'form':form,
		'pk':pk,
		'abrir':True,
		'parroquia': zip(parroquia, activo)
	}

	return render(request, 'parroquia_admin.html',data )


@login_required
def parroquia_admin_editar_guardar(request):
	pa= Parroquia.objects.get(pk=int(request.POST['id']))
	form = ParroquiaForm(instance=pa, data=request.POST,files=request.FILES)
	if form.is_valid():
		pa= form.save(commit=False)
		pa.save()
		form.save_m2m()

	return HttpResponseRedirect(reverse('principal:parroquia_admin'))



#_____________________________________Vistas de las Parroquias____________________________________

def parroquia(request):
	empleado=Empleado.objects.filter(estado_obispo= False, estado_sacerdote=True,estado=True)
	lista=[]
	for s in empleado:
		if not Parroquia.objects.filter(empleado=s).exists():
			lista.append(int(s.id))

	form= ParroquiaForm()
	form.fields['empleado'].queryset= Empleado.objects.filter(id__in=lista)
	form.fields['empleado'].label= 'Seleccioné el Sacerdote'
	form.fields['municipio'].label= 'Seleccioné el Municipio'
	form.fields['pastoral'].label= 'Seleccioné las Pastorales'
	form.fields['descripcion'].label= 'Descripción de la Parroquia'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	parroquia= Parroquia.objects.filter(estado=True)
	data = {
		'parroquia': parroquia,
		'form':form
	}
	return render(request, 'parroquia.html',data )


@login_required
def parroquia_ver(request,pk):
	parroquia = Parroquia.objects.get(pk=pk)
	data={
		'parroquia':parroquia
	}
	return render(request,'parroquia_ver.html',data)


@login_required()
def parroquia_guardar(request):
	if request.method == 'POST':
		form = ParroquiaForm(request.POST,request.FILES)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('principal:parroquia'))


@login_required
def parroquia_editar(request, pk):
	parroquia= Parroquia.objects.get(pk=int(pk))
	form = ParroquiaForm(instance=parroquia)
	form.fields['empleado'].label= 'Seleccioné el Sacerdote'
	form.fields['municipio'].label= 'Seleccioné el Municipio'
	form.fields['pastoral'].label= 'Seleccioné las Pastorales'
	form.fields['descripcion'].label= 'Descripción de la Parroquia'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'form':form,
		'pk':pk,
		'abrir':True,
		'parroquia':parroquia
	}

	return render(request, 'parroquia_ver.html',data )


@login_required
def parroquia_editar_guardar(request,pk):
	pa= Parroquia.objects.get(pk=int(request.POST['id']))
	form = ParroquiaForm(instance=pa, data=request.POST,files=request.FILES)
	if form.is_valid():
		pa= form.save(commit=False)
		pa.save()
		form.save_m2m()

	return HttpResponseRedirect(reverse('principal:parroquia_ver',args=(pk,)))


@login_required
def parroquia_desactivar(request, pk):
	parroquia = Parroquia.objects.get(pk=pk)
	parroquia.estado=False
	parroquia.save()
	return HttpResponseRedirect(reverse('principal:parroquia'))


#__________________________________________Vistas de las Pastorales_________________________________

def pastoral(request):
	pastoral= Pastoral.objects.all()
	form= PastoralForm()
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	form.fields['nombre'].label= 'Seleccioné el Nombre de Pastoral'
	data = {
		'pastoral': pastoral,
		'form':form
	}
	return render(request, 'pastoral.html',data )


@login_required()
def pastoral_guardar(request):
	if request.method == 'POST':
		form = PastoralForm(request.POST,request.FILES)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('principal:pastoral'))


@login_required
def pastoral_editar(request, pk):
	pastoral= Pastoral.objects.all()
	past= Pastoral.objects.get(pk=int(pk))
	form = PastoralForm(instance=past)
	form.fields['nombre'].label= 'Seleccioné el Nombre de Pastoral'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'past':past,
		'form':form,
		'pk':pk,
		'abrir':True,
		'pastoral':pastoral
	}

	return render(request, 'pastoral.html',data )


@login_required
def pastoral_editar_guardar(request):
	past= Pastoral.objects.get(pk=int(request.POST['id']))
	form = PastoralForm(instance=past, data=request.POST,files=request.FILES)
	if form.is_valid():
		past= form.save(commit=False)
		past.save()

	return HttpResponseRedirect(reverse('principal:pastoral'))


@login_required
def pastoral_desactivar(request):
	id = request.GET.get('id')
	p = Pastoral.objects.get(pk=int(id))
	p.delete()
	return JsonResponse({'response':'desactivado'})

#____________________________________________________Vistas del Sacerdote_________________________________

def sacerdote(request):
	parroquia= Parroquia.objects.filter(estado=True)
	data = {
		'parroquia': parroquia
	}
	return render(request, 'sacerdote.html',data )


@login_required
def sacerdote_ver(request,pk):
	empleado = Empleado.objects.get(pk=pk)
	data={
		'empleado':empleado
	}
	return render(request,'sacerdote_ver.html',data)


@login_required
def sacerdote_editar(request, pk):
	empleado= Empleado.objects.get(pk=int(pk))
	form = EmpleadoForm(instance=empleado)
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'form':form,
		'pk':pk,
		'abrir':True,
		'empleado':empleado
	}

	return render(request, 'sacerdote_ver.html',data )


@login_required
def sacerdote_editar_guardar(request,pk):
	emp= Empleado.objects.get(pk=int(request.POST['id']))
	form = EmpleadoForm(instance=emp, data=request.POST,files=request.FILES)
	if form.is_valid():
		emp= form.save(commit=False)
		emp.save()
		form.save_m2m()

	return HttpResponseRedirect(reverse('principal:sacerdote_ver',args=(pk,)))


@login_required
def sacerdote_desactivar(request, pk):
	empleado = Empleado.objects.get(pk=pk)
	parroquia = Parroquia.objects.get(empleado=empleado)
	parroquia.estado=False
	parroquia.save()
	empleado.estado = False
	empleado.save()
	return HttpResponseRedirect(reverse('principal:sacerdote'))


#________________________________________________vistas del obispo____________________________________
def obispo(request):
	usuarios = User.objects.all()
	lista=[]
	for s in usuarios:
		if not Empleado.objects.filter(user=s).exists():
			lista.append(int(s.id))
	form= ObispoForm()
	form.fields['fecha_ord'].label= 'Fecha de Ordenación'
	form.fields['direccion'].label= 'Dirección del Obispo'
	form.fields['biografia'].label= 'Biografía del Obispo'
	form.fields['cargo'].label= 'Seleccioné el Cargo'
	form.fields['user'].label= 'Seleccioné el Usuario'
	form.fields['estudios'].label= 'Seleccioné los Estudios del Obispo'
	form.fields['user'].queryset= User.objects.filter(id__in=lista)

	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	if Empleado.objects.filter(estado_obispo= True).exists():
		empleado = Empleado.objects.get(estado_obispo= True, estado=True)
		estado= False
	else :
		estado= True
		empleado= "No hay Obispo Actual"
		

	data = {
		'empleado': empleado,
		'form': form,
		'estado':estado
	}
	return render(request, 'obispo.html',data )


@login_required()
def obispo_guardar(request):
	if request.method == 'POST':
		form = ObispoForm(request.POST,request.FILES)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('principal:obispo'))

		
		# if form.is_valid():
		# 	o= form.save()
		# 	listadoEstudios= o.estudios.all()
		# 	obispo='''
		# 	<div class="col-md-3" id="guyimg">
		# 		<img src="%s" alt="...">
		# 	</div>
		# 	<div class="bio col-md-8" style="margin-left: 90px;">
		# 		<h1>%s %s</h1>
		# 		<hr>
		# 		<p>%s</p>
		# 		<h3>Estudios</h3>
		# 		<table class="table table-striped">
		# 			<thead>
		# 				<tr>
		# 					<th>#</th>
		# 					<th>NOMBRE</th>
		# 					<th>LUGAR</th>
		# 					<th>PERIODO</th>
		# 				</tr>
		# 			</thead>
		# 			<tbody id="add_empleado">
		# 				%s
		# 			</tbody>
		# 		</table>
		# 	</div>																																																																																																																																																											
		# 	'''% (o.imagen.url,o.nombre,o.apellido,o.biografia,"".join([
		# 		'''
		# 			<tr>
		# 				<td>%s</td>
		# 				<td>%s</td>
		# 				<td>%s</td>
		# 				<td>%s</td>
		# 			</tr>
		# 		'''.format(e.id,e.nombre,e.lugar,e.periodo)
		# 		for e in listadoEstudios ]))
		# 	return JsonResponse({'response':obispo})
		# else:
		# 	return render(request, 'obispo.html',{'form': form})


@login_required
def obispo_editar(request, pk):
	if Empleado.objects.filter(estado_obispo= True).exists():
		empleado = Empleado.objects.get(estado_obispo= True, estado=True)
		estado= False
	else :
		estado= True
		empleado= "No hay Obispo Actual"
	emp= Empleado.objects.get(pk=int(pk))
	form = ObispoForm(instance=emp)
	form.fields['fecha_ord'].label= 'Fecha de Ordenación'
	form.fields['direccion'].label= 'Dirección del Obispo'
	form.fields['biografia'].label= 'Biografía del Obispo'
	form.fields['cargo'].label= 'Seleccioné el Cargo'
	form.fields['user'].label= 'Seleccioné el Usuario'
	form.fields['estudios'].label= 'Seleccioné los Estudios del Obispo'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'emp':emp,
		'form':form,
		'pk':pk,
		'abrir':True,
		'empleado':empleado,
		'estado':estado
	}

	return render(request, 'obispo.html',data )


@login_required
def obispo_editar_guardar(request):
	emp= Empleado.objects.get(pk=int(request.POST['id']))
	form = ObispoForm(instance=emp, data=request.POST,files=request.FILES)
	if form.is_valid():
		emp= form.save(commit=False)
		emp.save()
		form.save_m2m()

	return HttpResponseRedirect(reverse('principal:obispo'))


@login_required
def obispo_ver(request,pk):
	empleado = Empleado.objects.get(pk=pk)
	data={
		'empleado':empleado
	}
	return render(request,'obispo_ver.html',data)


@login_required()
def obispo_desactivar(request, pk):
	e = Empleado.objects.get(pk=pk)
	e.estado_obispo= False
	e.save()
	return HttpResponseRedirect(reverse('principal:obispo'))


# @login_required
# def obispo_desactivar(request):
# 	id = request.GET.get('id')
# 	e = Empleado.objects.get(pk=id)
# 	e.estado_obispo= False
# 	e.save()
# 	return JsonResponse({'response':'desactivado'})



#____________________________________________Vistas de los Estudios_________________________________
@login_required()
def estudio(request):
	estudio = Estudio.objects.all()
	form =EstudioForm()
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	data = {
		'estudio':estudio,
		'form':form
	}
	return render(request,'estudio.html',data)


@login_required()
def estudio_guardar(request):
	if request.method == 'POST':
		form = EstudioForm(data=request.POST)

		if form.is_valid():
			e =form.save()

			estudio='''
				<tr id="d_estudio-%s">
					<td>%s</td>
					<td>%s</td>
					<td>%s</td>
					<td>%s</td>
					<td>
						<div class="btn-group">
							<button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
									<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>
							</button>
							<ul class="dropdown-menu">
					 	 		<a  style="margin-left:30px; "
									class="btn btn-info" href=""><span class="glyphicon glyphicon-refresh"></span> Actualizar</a>
								<button class="btn btn-danger btn-destudio"
										data-id="%s"
										data-url=""
										style="margin-left:30px; margin-top:5px"><span class="glyphicon glyphicon-remove"></span> Eliminar</button>
						    </ul>
						</div>
					</td>
				</tr>
			'''% (e.id,e.id,e.nombre,e.lugar,e.periodo,e.id)
			return JsonResponse({'response':estudio})
		else:
			return render(request, 'estudio.html',{'form': form})


@login_required()
def estudio_eliminar(request):
	id = request.GET.get('id')
	e = Estudio.objects.get(pk=id)
	e.delete()
	return JsonResponse({'response':'eliminado'})


@login_required()
def estudio_editar(request,pk):
	estudio = Estudio.objects.all()
	e= Estudio.objects.get(pk=pk)
	form = EstudioForm(instance=e)
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'estudio':estudio,
		'e':e,
		'form':form,
		'pk':pk,
		'abrir':True
	}

	return render(request,'estudio.html',data)


@login_required()
def estudio_editar_guardar(request):
	e= Estudio.objects.get(pk=int(request.POST['id']))
	form = EstudioForm(instance=e, data=request.POST)
	if form.is_valid():
		e= form.save(commit=False)
		e.save()

	return HttpResponseRedirect(reverse('principal:estudio'))



#_______________________________________________Vistas del Empleado_________________________________
@login_required()
def empleado(request):
	usuarios = User.objects.all()
	lista=[]
	for s in usuarios:
		if not Empleado.objects.filter(user=s).exists():
			lista.append(int(s.id))
	form =EmpleadoForm()
	form.fields['user'].queryset= User.objects.filter(id__in=lista)
	empleado = Empleado.objects.all()
	
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	activo = []
	for e in empleado:
		if e.estado:
			activo.append('si')
		else:
			activo.append('no')

	data = {
		'empleado': zip(empleado, activo),
		'form':form
	}
	return render(request,'empleado.html',data)


@login_required()
def empleado_guardar(request):
	if request.method == 'POST':
		form = EmpleadoForm(data=request.POST,files=request.FILES)

		if form.is_valid():
			e =form.save()

			empleado='''
			<tr>
				<td>%s</td>
				<td>%s %s</td>
				<td>%s</td>
				<td>%s</td>
				<td><span id="estado-%s">%s</span></td>
				<td>%s</td>
				<td>
					<div class="btn-group">
						<button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>
						</button>
						<ul class="dropdown-menu">
							<a  style="margin-left:30px; "
								class="btn btn-info" href=""><span class="glyphicon glyphicon-refresh"></span> Actualizar</a>
							<button class="btn btn-danger btn-user"
								data-id="%s"
								data-url=""
								style="margin-left:30px; margin-top:5px">Desactivar</button>			
						</ul>
					</div>
				</td>
				<td>%s</td>
			</tr>
			'''% (e.numero_identidad,e.nombre,e.apellido,e.telefono,e.direccion,e.id,e.estado,e.correo,e.id,e.cargo)
			return JsonResponse({'response':empleado})
		else:
			return render(request, 'empleado.html',{'form': form})


@login_required()
def empleado_desactivar(request):
	id = request.GET.get('id')
	u = Empleado.objects.get(pk=id)
	d = Empleado.objects.filter(pk=id,estado=True)

	if d:
		u.estado= False
		u.save()
		action='Activar'
		valor='False'
	else:
		u.estado= True
		u.save()
		action='Desactivar'
		valor='True'
	return JsonResponse({'action':action,'valor':valor})


@login_required()
def empleado_editar(request,pk):
	emp= Empleado.objects.get(pk=pk)
	form = Empleado_EditarForm(instance=emp)
	empleado = Empleado.objects.all()
	
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	activo = []
	for e in empleado:
		if e.estado:
			activo.append('si')
		else:
			activo.append('no')
	data ={
		'empleado': zip(empleado, activo),
		'emp':emp,
		'form':form,
		'pk':pk,
		'abrir':True
	}

	return render(request,'empleado.html',data)


@login_required()
def empleado_editar_guardar(request):
	emp= Empleado.objects.get(pk=int(request.POST['id']))
	form = Empleado_EditarForm(instance=emp, data=request.POST,files=request.FILES)
	if form.is_valid():
		emp= form.save(commit=False)
		emp.save()
		form.save_m2m()


	return HttpResponseRedirect(reverse('principal:empleado'))

#_______________________________________________Vistas del Usuario_________________________________
@login_required()
def usuario(request):
	usuario = User.objects.all()
	form =UserCreationForm()
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	activo = []
	for u in usuario:
		if u.is_staff:
			activo.append('staff')
		elif u.is_active:
			activo.append('si')
		else:
			activo.append('no')

	data = {
		'usuario': zip(usuario, activo),
		'form':form
	}
	return render(request,'usuario.html',data)


@login_required()
def usuarios_guardar(request):
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			u =form.save()

			usu='''
			<tr>
				<td>%s</td>
				<td>%s</td>
				<td>%s %s</td>
				<td>%s</td>
				<td><span id="estado-%s">%s</span></td>
				<td>%s</td>
				<td>
					<div class="btn-group">
						<button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							<span class="glyphicon glyphicon-cog"></span> <span class="caret"></span>
						</button>
						<ul class="dropdown-menu">
						</ul>
					</div>
				</td>
				<td>%s</td>
			</tr>'''% (u.id,u.username,u.first_name,u.last_name,u.is_superuser,u.id,u.is_active,u.date_joined,u.last_login)
			return JsonResponse({'response':usu})
		else:
			return render(request, 'usuario.html',{'form': form})


@login_required()
def usuarios_desactivar(request):
	id = request.GET.get('id')
	u = User.objects.get(pk=id)
	d = User.objects.filter(pk=id,is_active=True)

	if d:
		u.is_active= False
		u.save()
		action='Activar'
		valor='False'
	else:
		u.is_active= True
		u.save()
		action='Desactivar'
		valor='True'
	return JsonResponse({'action':action,'valor':valor})


@login_required()
def usuarios_editar(request,pk):
	usuario = User.objects.all()
	activo = []
	for u in usuario:
		if u.is_staff:
			activo.append('staff')
		elif u.is_active:
			activo.append('si')
		else:
			activo.append('no')
	user= User.objects.get(pk=pk)
	form = UserForm(instance=user)
	form.fields['is_superuser'].label= 'Super Usuario del Sistema'
	form.fields['is_staff'].label= 'Administrador del Sistema'
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'
	data ={
		'usuario': zip(usuario, activo),
		'user':user,
		'form':form,
		'pk':pk,
		'abrir':True
	}

	return render(request,'usuario.html',data)


@login_required()
def usuario_editar_guardar(request):
	user= User.objects.get(pk=int(request.POST['id']))
	form = UserForm(instance=user, data=request.POST)
	if form.is_valid():
		user= form.save(commit=False)
		user.save()


	return HttpResponseRedirect(reverse('principal:usuario'))

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
	if request.method == 'POST':
		form = PublicacionForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('principal:index'))

@login_required
def editar_publicacion(request, id):
	publicacion = Publicacion.objects.get(pk = id)
	publicacionForm_Editar = PublicacionForm_Editar(instance=publicacion)

	if request.user.id:
		empleado = Empleado.objects.get(pk = request.user.id)
		publicacionForm = PublicacionForm(initial={'empleado': empleado})
	else:
		publicacionForm = PublicacionForm()

	for field in publicacionForm_Editar.fields:
		publicacionForm_Editar.fields[field].widget.attrs['class']='form-control'

	for field in publicacionForm.fields:
		publicacionForm.fields[field].widget.attrs['class']='form-control'

	form = AuthenticationForm()
	form.fields['username'].widget.attrs['class'] = 'form-control'
	form.fields['username'].widget.attrs['autofocus'] = 'True'
	form.fields['password'].widget.attrs['class'] = 'form-control'

	publicaciones = Publicacion.objects.all().order_by('-fecha_pub')[:3]

	context = {
		'publicaciones': publicaciones,
		'form': form,
		'publicacionForm': publicacionForm,
		'editarForm': publicacionForm_Editar,
		'abrir': True,
		'pk': id
	}
	return render(request, 'index.html', context)

@login_required
def editar_guardar_publicacion(request):
	publicacion = Publicacion.objects.get(pk = int(request.POST['id']))
	publicacionForm_Editar = PublicacionForm_Editar(instance=publicacion, data=request.POST, files=request.FILES)
	if publicacionForm_Editar.is_valid():
		publicacion = publicacionForm_Editar.save(commit=False)
		publicacionForm_Editar.save()

	return HttpResponseRedirect(reverse('principal:index'))

@login_required
def eliminar_publicacion(request, id):
	publicacion = Publicacion.objects.get(pk = id)
	publicacion.delete()

	return HttpResponseRedirect(reverse('principal:index'))


def homilia(request):
	if request.user.id:
		empleado = Empleado.objects.get(user = request.user.id)
		homiliaForm = HomiliaForm(initial = {'empleado': empleado})
	else:
		homiliaForm = HomiliaForm()

	homilias = Homilia.objects.all().order_by('fecha')
	for field in homiliaForm.fields:
		homiliaForm.fields[field].widget.attrs['class']='form-control'

	ctx = {
		'homiliaForm': homiliaForm
	}
	return render(request, 'homilia.html', ctx)

def detalle_homilia(request, id):
	homilia = Homilia.objects.get(pk = id)

	ctx = {
		'homilia': homilia
	}

	return render(request, 'detalleHomilia.html', ctx)

@login_required
def editar_homilia(request, pk):
	homilia = Homilia.objects.get(pk = pk)
	homiliaFormEditar = HomiliaForm(instance = homilia)
	
	if request.user.id:
		empleado = Empleado.objects.get(user = request.user.id)
		homiliaForm = HomiliaForm(initial = {'empleado': empleado})
	else:
		homiliaForm = HomiliaForm()

	for field in homiliaForm.fields:
		homiliaForm.fields[field].widget.attrs['class']='form-control'

	for field in homiliaFormEditar.fields:
		homiliaFormEditar.fields[field].widget.attrs['class']='form-control'

	ctx = {
		'homiliaFormEditar': homiliaFormEditar,
		'homiliaForm': homiliaForm,
		'abrir': True,
		'pk': pk
	}
	return render(request, 'homilia.html', ctx)

@login_required
def editar_guardar_homilia(request):
	homilia = Homilia.objects.get(pk = int(request.POST['id']))
	homiliaForm = HomiliaForm(instance=homilia, data=request.POST)
	if homiliaForm.is_valid():
		homilia = homiliaForm.save(commit=False)
		homiliaForm.save()

	return HttpResponseRedirect(reverse('principal:homilia'))


def homiliasXMes(request):
	id = request.GET['id']
	homilias = Homilia.objects.filter(fecha__month = id)
	homiliasMes = []
	botones = ''
	listBotones = []
	mensaje = '''
				<div class="alert alert-danger" role="alert">
					<p>
						No hay homil&iacute;as Disponibles.
					</p>
				</div>
			  '''
	
	for h in homilias:
		if request.user.is_active:
			botones = '''
						<a href="/principal/editar-homilia/{}/" class="btn btn-info">Editar <span class="glyphicon glyphicon-pencil"></span></a>
						<a href="" data-href="/principal/eliminar-homilia/{}/" class="btn btn-danger" data-toggle="modal" data-target="#confirm-delete">Eliminar <span class="glyphicon glyphicon-remove"></span></a>						
					  ''' .format(h.id, h.id)

		formato = '''
					<tr>
						<td>{}</td>
						<td>{}</td>
						<td>{}</td>
						<td>{}</td>
						<td style="text-align: center">
							<a href="/principal/detalle-homilia/{}/" class="btn btn-warning">Ver m&aacute;s <span class="glyphicon glyphicon-search"></span></a>
							{}
						</td>
					</tr> 
				''' .format(h.titulo, h.fecha, h.hora, h.parroquia, h.id, botones)
		homiliasMes.append(formato)
		mensaje = ''

	return JsonResponse({'format': homiliasMes, 'msj': mensaje})

@login_required
def nueva_homilia(request):
	if request.method == 'POST':
		form = HomiliaForm(request.POST)

		if form.is_valid():
			form.save()
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

def pastoral_diocesis(request):
	pastorales = Pastoral_Diocesi.objects.all()
	pastoralForm = Pastoral_DiocesisForm()

	for field in pastoralForm.fields:
		pastoralForm.fields[field].widget.attrs['class']='form-control'

	ctx = {
		'pastorales': pastorales,
		'pastoralForm': pastoralForm
	}
	return render(request, 'pastorales_diocesis.html', ctx)


@login_required
def agregar_pastoral_diocesis(request):
	if request.method == 'POST':
		form = Pastoral_DiocesisForm(data=request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('principal:pastoral_diocesis'))

@login_required
def eliminar_pastoral_diocesis(request, id):
	pastoral = Pastoral_Diocesi.objects.get(pk = id)
	pastorales_parroquia = Pastoral.objects.filter(nombre = pastoral)

	pastorales_parroquia.delete()

	pastoral.delete()

	return HttpResponseRedirect(reverse('principal:pastoral_diocesis'))

@login_required
def editar_pastoral_diocesis(request, id):
	pastoral = Pastoral_Diocesi.objects.get(pk = id)

	formPastoral = Pastoral_DiocesisForm(instance = pastoral)

	pastorales = Pastoral_Diocesi.objects.all()
	pastoralForm = Pastoral_DiocesisForm()

	for field in formPastoral.fields:
		formPastoral.fields[field].widget.attrs['class']='form-control'

	for field in pastoralForm.fields:
		pastoralForm.fields[field].widget.attrs['class']='form-control'

	ctx = {
		'pastorales': pastorales,
		'pastoralForm': pastoralForm,
		'editarPastoralForm': formPastoral,
		'abrir': True,
		'pk': id
	}

	return render(request, 'pastorales_diocesis.html', ctx)

@login_required
def pastoral_diocesis_editar_guardar(request):
	pastoral = Pastoral_Diocesi.objects.get(pk = request.POST['id'])

	formPastoral = Pastoral_DiocesisForm(instance = pastoral, data=request.POST)

	if formPastoral.is_valid():
		pastoral = formPastoral.save(commit=False)
		formPastoral.save()

	return HttpResponseRedirect(reverse('principal:pastoral_diocesis'))



def diocesis_datos(request):
	datos = Diocesi.objects.all()
	

	ctx = {
		'datos': datos
	}

	return render(request, 'diocesis.html', ctx)

@login_required
def editar_diocesis(request, id):
	diocesis = Diocesi.objects.get(pk = id)

	form = Diocesis_Form(instance = diocesis)

	datos = Diocesi.objects.all()
	
	for field in form.fields:
		form.fields[field].widget.attrs['class']='form-control'

	ctx = {
		'datos': datos,
		'formDiocesis': form,
		'abrir': True,
		'pk': id
	}

	return render(request, 'diocesis.html', ctx)

@login_required
def editar_guardar_diocesis(request):
	diocesis = Diocesi.objects.get(pk = request.POST['id'])

	form = Diocesis_Form(instance = diocesis, data=request.POST, files=request.FILES)

	if form.is_valid():
		diocesis = form.save(commit=False)
		form.save()

	return HttpResponseRedirect(reverse('principal:diocesis_datos'))


def contacto(request):
	datos = Diocesi.objects.all()

	ctx = {
		'datos': datos
	}

	return render(request, 'contactanos.html', ctx)


def send_email(request):	
    if request.method == 'POST':
    	datos = Diocesi.objects.get(pk = 1)

    	nombres = request.POST['nombre']
    	telefono = request.POST['phone']
    	email = request.POST['email']
    	subject = 'Consulta'
    	content = request.POST['mensaje']

    	mensaje = '''
			De: {} 
			Email: {}
			Telefono: {}

			
			Mensaje: 
			{}
    	'''.format(nombres, email, telefono, content)

       
        send_mail(
            subject,
            mensaje,
            email, #FROM
            [datos.email]
        )

	return HttpResponseRedirect(reverse('principal:contacto'))
 






