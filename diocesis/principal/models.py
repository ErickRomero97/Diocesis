# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.

#Modelo Cargo
@python_2_unicode_compatible
class  Cargo(models.Model):
	cargo = models.CharField(max_length=20)
	def __str__(self):
		return self.cargo

#Modelo Municipio
@python_2_unicode_compatible
class  Municipio(models.Model):
	municipio = models.CharField(max_length=30)
	def __str__(self):
		return self.municipio

#Modelo Depto
@python_2_unicode_compatible
class  Depto(models.Model):
	depto = models.CharField(max_length=30)
	municipio = models.ForeignKey(Municipio)
	def __str__(self):
		return self.depto


#Modelo de Empleados
@python_2_unicode_compatible
class Empleado(models.Model):
	SEXOS = (
		('1', 'Masculino'),
		('2', 'Femenino')
	)
	numero_identidad = models.CharField(max_length=15,verbose_name='Numero de Identidad')
	nombre =models.CharField(max_length=30)
	apellido =models.CharField(max_length=30)
	fecha_nac =  models.DateField(verbose_name='Fecha de Nacimiento')
	fecha_ord =  models.DateField(verbose_name='Fecha de Ordenacion',null=True,blank=True)
	telefono = models.CharField(max_length=20)
	direccion = models.TextField()
	biografia = models.TextField()
	correo = models.EmailField()
	estado_obispo= models.BooleanField(default=False)
	imagen = models.ImageField(upload_to = 'empleado')
	sexo = models.CharField(max_length=10, choices=SEXOS)
	cargo = models.ForeignKey(Cargo)
	user = models.OneToOneField(User)

	def __str__(self):
		return "{} - {} {}" .format(self.numero_identidad,self.nombre, self.apellido)

#Modelo de Publicaciones
@python_2_unicode_compatible
class Publicacion(models.Model):
	nombre= models.CharField(max_length=100)
	contenido = models.TextField()
	empleado =  models.ForeignKey(Empleado)
	fecha_pub = models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Publicacion')
	imagen = models.ImageField(upload_to='publicaciones')

	class Meta:
		verbose_name_plural='Publicaciones'
	def __str__(self):
		return "{} {} {}" .format(self.empleado,self.nombre,self.fecha_pub)



#Modelo de Pastorales
@python_2_unicode_compatible
class  Pastoral(models.Model):
	nombre = models.CharField(max_length=30)
	encargado =  models.CharField(max_length=30)
	horarios = models.CharField(max_length=30)
	eslogan=models.CharField(max_length=30)
	imagen = models.ImageField(upload_to='pastorales')

	class Meta:
		verbose_name_plural='Pastorales'
	def __str__(self):
		return "{}" .format(self.nombre)


#Modelo de Parroquia
@python_2_unicode_compatible
class Parroquia(models.Model):
	nombre = models.CharField(max_length=40)
	descripcion= models.TextField()
	telefono = models.CharField(max_length=20)
	direccion = models.TextField()
	imagen= models.ImageField(upload_to = 'parroquia')
	empleado= models.OneToOneField(Empleado)
	pastoral=models.ManyToManyField(Pastoral)
	municipio=models.ForeignKey(Municipio)
	def __str__(self):
		return "{} ,{}" .format(self.nombre,self.municipio)

#Modelo de Homilia
@python_2_unicode_compatible
class  Homilia(models.Model):
	contenido = models.TextField()
	empleado =  models.ForeignKey(Empleado)
	hora = models.TimeField()
	fecha = models.DateField()
	parroquia=models.ForeignKey(Parroquia)
	def __str__(self):
		return "{} {}-{}" .format(self.empleado,self.hora,self.fecha)


#Modelo de Diocesis
@python_2_unicode_compatible
class  Diocesi(models.Model):
	nombre = models.CharField(max_length=30)
	direccion =  models.TextField()
	historia =  models.TextField()
	imagen = models.ImageField(upload_to='diocesis')
	parroquia=models.ManyToManyField(Parroquia)
	empleado=models.ForeignKey(Empleado)
	pastoral=models.ManyToManyField(Pastoral)

	def __str__(self):
		return "{} {}" .format(self.nombre,self.empleado)









