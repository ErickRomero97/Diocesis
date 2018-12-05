from django.forms import ModelForm
from django import forms
from .models import *

class PublicacionForm(ModelForm):
	class Meta:
		model = Publicacion
		fields = ('__all__')
		widgets = {
			'nombre': forms.TextInput(attrs={
				'placeholder': 'Titulo',
				'autofocus': 'autofocus'
				}),
			'empleado': forms.TextInput(attrs={
				'type': 'hidden'
				}),
			'contenido': forms.Textarea(attrs={
				'placeholder': 'Contenido'
				})
		}

class PublicacionForm_Editar(ModelForm):
	class Meta:
		model = Publicacion
		fields = ('nombre', 'contenido', 'imagen')

class HomiliaForm(ModelForm):
	class Meta:
		model = Homilia
		fields = '__all__'
		widgets = {
			'empleado': forms.TextInput(attrs={
				'type': 'hidden'
				}),
			'fecha': forms.DateInput(attrs={
				'type': 'date'
				}),
			'hora': forms.TimeInput(attrs={
				'type': 'time'
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
				'type': 'date'
				}),
			'hora': forms.TimeInput(attrs={
				'class': 'form-control',
				'type': 'date'
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

#form Pastoral_Diocesis
class Pastoral_DiocesisForm(ModelForm):
	class Meta:
		model = Pastoral_Diocesi
		fields = '__all__'

#form Diocessis
class Diocesis_Form(ModelForm):
	class Meta:
		model = Diocesi
		fields = '__all__'
		widgets = {
			'empleado': forms.TextInput(attrs={
				'type': 'hidden'
				}),
		}







