from rest_framework import serializers
from .models import Solicitudes, Consultas

#Creo el serializer para las solicitudes
class SolicitudesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitudes
        fields = '__all__'

#Creo el serializar para las consultas
class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = '__all__'