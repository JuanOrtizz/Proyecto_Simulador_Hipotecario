from django.contrib import admin
from .models import Consultas, Solicitudes

admin.site.register([Consultas, Solicitudes])