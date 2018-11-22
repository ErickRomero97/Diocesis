from django.forms import ModelForm
from django import forms
from .models import Publicacion

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