from django.forms import ModelForm
from django import forms
from .models import *

class PublicacionForm(ModelForm):
	class Meta:
		model = Publicacion
		fields = ('nombre', 'contenido', 'imagen', )
		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Titulo',
				'autofocus': 'autofocus',
				'id': 'nombre'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control',
				'placeholder': 'Contenido',
				'id': 'contenido'
				}),
			'imagen': forms.FileInput(attrs={
				'class': 'form-control',
				'id': 'imagen'
				})
		}

class PublicacionForm_Editar(ModelForm):
	class Meta:
		model = Publicacion
		fields = ('nombre', 'contenido', 'imagen', )
		widgets = {
			'nombre': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Titulo',
				'autofocus': 'autofocus'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control',
				'placeholder': 'Contenido'
				}),
			'imagen': forms.FileInput(attrs={
				'class': 'form-control'
				})
		}

class HomiliaForm(ModelForm):
	class Meta:
		model = Homilia
		fields = ('titulo', 'parroquia', 'fecha', 'hora', 'contenido', )
		widgets = {
			'titulo': forms.TextInput(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus',
				'id': 'titulo'
				}),
			'parroquia': forms.Select(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus',
				'id': 'parroquia'
				}),
			'fecha': forms.DateInput(attrs={
				'class': 'form-control',
				'placeholder': 'YY-MM-DD',
				'id': 'fecha'
				}),
			'hora': forms.TimeInput(attrs={
				'class': 'form-control',
				'placeholder': 'H-M-S',
				'id': 'hora'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control',
				'id': 'contenido'
				})
		}

class HomiliaForm_Editar(ModelForm):
	class Meta:
		model = Homilia
		fields = ('titulo', 'parroquia', 'fecha', 'hora', 'contenido', )
		widgets = {
			'titulo': forms.TextInput(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus'
				}),
			'parroquia': forms.Select(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus'
				}),
			'fecha': forms.DateInput(attrs={
				'class': 'form-control',
				'placeholder': 'YY-MM-DD'
				}),
			'hora': forms.TimeInput(attrs={
				'class': 'form-control',
				'placeholder': 'H-M-S'
				}),
			'contenido': forms.Textarea(attrs={
				'class': 'form-control'
				})
		}

class AlbumForm(ModelForm):
	class Meta:
		model = Album
		fields = ('nombre_album', )
		widgets = {
			'nombre_album': forms.TextInput(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus',
				'id': 'nombre'
				})
		}

class ImagenForm(ModelForm):
	class Meta:
		model = Album
		fields = ('imagen', )
		widgets = {
			'imagen': forms.FileInput(attrs={
				'class': 'form-control',
				'autofocus': 'autofocus'
				})
		}


#form Obispo
class ObispoForm(ModelForm):
	class Meta:
		model = Empleado
		fields = '__all__'
		widgets = {
			'fecha_nac': forms.DateInput(attrs={
				'type': 'date'}),
			'fecha_ord': forms.DateInput(attrs={
				'type': 'date'}),
			'telefono': forms.TextInput(attrs={
				'placeholder': '9999-9999'})
			
		}

#form Empleado
class EmpleadoForm(ModelForm):
	class Meta:
		model = Empleado
		fields = '__all__'
		widgets = {
			'fecha_nac': forms.DateInput(attrs={
				'type': 'date'}),
			'fecha_ord': forms.DateInput(attrs={
				'type': 'date'}),
			'telefono': forms.TextInput(attrs={
				'placeholder': '9999-9999'})
			
		}

#form Parroquia
class ParroquiaForm(ModelForm):
	class Meta:
		model = Parroquia
		fields = '__all__'
		widgets = {
			'telefono': forms.TextInput(attrs={
				'placeholder': '9999-9999'})
			
		}


#form Pastoral
class PastoralForm(ModelForm):
	class Meta:
		model = Pastoral
		fields = '__all__'
		# widgets = {
		# 	'fecha_nac': forms.DateInput(attrs={
		# 		'type': 'date'}),
		# 	'fecha_ord': forms.DateInput(attrs={
		# 		'type': 'date'})
			
		# }

#form User_Editar
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','is_staff','is_superuser',)
		widgets={
			'username':forms.TextInput(attrs={
				'readonly':True
				}),
			'is_staff':forms.CheckboxInput(attrs={
				'autofocus':'autofocus'
				})
		}

#form Empleado_Editar
class Empleado_EditarForm(ModelForm):
	class Meta:
		model = Empleado
		fields = '__all__'
		widgets = {
			'fecha_nac': forms.DateInput(attrs={
				'type': 'date'}),
			'fecha_ord': forms.DateInput(attrs={
				'type': 'date'}),
			'user': forms.HiddenInput(),
			'telefono': forms.TextInput(attrs={
				'placeholder': '9999-9999'})
			
		}


#form Estudio
class EstudioForm(ModelForm):
	class Meta:
		model = Estudio
		fields = '__all__'








