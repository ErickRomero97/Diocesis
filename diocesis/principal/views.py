# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
	return render(request, 'index.html', )

def obispo(request):
	return render(request, 'obispo.html', )

def sacerdote(request):
	return render(request, 'sacerdote.html', )

def publicaciones(request):
	return render(request, 'publicaciones.html', )

