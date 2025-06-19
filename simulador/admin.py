from django.contrib import admin
# myapp/admin.py
from django.contrib import admin
from .models import Consultas, Solicitudes
from django.contrib.auth.models import User

admin.site.register([Consultas, Solicitudes, User])
